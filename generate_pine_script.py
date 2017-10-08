import argparse
from datetime import datetime
from GetRobinhoodTrades import getRobinhoodTrades
import Exporter

def parseTrades(trades):
    parsedTrades = []
    for trade in trades:
        try:
            timestamp = trade["timestamp"]
            timestamp = timestamp[:timestamp.find('.')] # remove everything after seconds (including timezone)
            date = datetime.strptime(timestamp, DATE_FORMAT)
            parsedTrades.append({
                "year": date.year,
                "month": date.month,
                "day": date.day,
                "hour": date.hour,
                "minute": date.minute,
                "price": trade["price"],
                "quantity": trade["quantity"],
                "symbol": trade["symbol"],
                "side": trade["side"],
            })
        except:
            continue
    return parsedTrades

def consolidateTradesBySymbol(trades):
    symbols = list(set([trade["symbol"] for trade in trades]))
    tradesBySymbol = [] # [{"symbol":..,"buyTrades":..,"sellTrades":..}]
    for symbol in symbols:
        tradesFilteredBySymbol = [trade for trade in trades if trade["symbol"] == symbol]    
        tradesBySymbol.append({
            "symbol": symbol,
            "buyTrades": [trade for trade in tradesFilteredBySymbol if trade["side"] == "buy"],
            "sellTrades": [trade for trade in tradesFilteredBySymbol if trade["side"] == "sell"]
        })
    return tradesBySymbol

def getTradesCondition(symbol, dates):
    tickeridcondition = "tickerid == 'BATS:%s'" % symbol
    datesCondition = " or ".join(["check(timestamp(%d,%d,%d,%d,%d))" % (date['year'], date['month'], date['day'], date['hour'], date['minute']) for date in dates])
    return "%s and (%s)" % (tickeridcondition, datesCondition)

def getPlotShapeFunction(trade):
    return """plotshape(%s, style=shape.%s,  location=location.%s, color=%s, text="%s", size="%s")""" % (trade["condition"], trade["shape"], trade["location"], trade["color"], "", "size.normal")

def getBGColorFunction(trade):
    return """bgcolor(%s ? %s : na, transp=40)""" % (trade["condition"], trade["color"])

def getSourceCode(trades):
    sourceCode = '''
//@version=3
study("My Trades", overlay=true)
check(t) =>
    a = isintraday and year == year(t) and month == month(t) and dayofmonth == dayofmonth(t) and hour == hour(t) and minute >= floor(minute(t)/interval) * interval and minute < ceil(minute(t)/interval) * interval
    b = isdaily and year == year(t) and month == month(t) and dayofmonth >= floor(dayofmonth(t)/interval) * interval and dayofmonth <= ceil(dayofmonth(t)/interval) * interval
    a or b
'''
    for trade in trades:
        symbol = trade["symbol"]
        buyTradesCondition = getTradesCondition(trade["symbol"], trade["buyTrades"])
        sellTradesCondition = getTradesCondition(trade["symbol"], trade["sellTrades"])
        # change this to a class
        buy = {"condition": buyTradesCondition, "shape": "triangleup", "location": "belowbar", "color": "green", "text": ""}
        sell = {"condition": sellTradesCondition, "shape": "triangledown", "location": "abovebar", "color": "red", "text": ""}
        sourceCode += "\n" + "\n".join([getPlotShapeFunction(trade) for trade in [buy, sell] if len(trade["condition"]) >  0])
        # sourceCode += "\n" + "\n".join([getBGColorFunction(trade) for trade in [buy, sell]])
    return sourceCode

#############################################################################################
#############################################################################################
######################################END FUNCTIONS##########################################
#############################################################################################
#############################################################################################

DATE_FORMAT = '%Y-%m-%dT%H:%M:%S'
TRADING_VIEW_OPTION = "tradingview"
exporter = Exporter.Exporter("pinescript code")

parser = argparse.ArgumentParser(description='Generate pinescript to chart your robinhood trades on tradingview.')
parser.add_argument('--debug', action='store_true', help='store raw JSON output to debug.json')
parser.add_argument('--username', required=True, help='your Robinhood username')
parser.add_argument('--password', required=True, help='your Robinhood password')
exporter.addArgumentsToParser(parser)
args = parser.parse_args()

username = args.username
password = args.password
exporter.parseArguments(args)

######## done with parsing ###############


trades = getRobinhoodTrades(username, password, args.debug)

parsedTrades = parseTrades(trades)

tradesBySymbol = consolidateTradesBySymbol(parsedTrades)

sourceCode = getSourceCode(tradesBySymbol)

exporter.exportText(sourceCode)