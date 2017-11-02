import argparse
from datetime import datetime
from GetRobinhoodTrades import getRobinhoodTrades
import Exporter

DATE_FORMAT = '%Y-%m-%dT%H:%M:%S'

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
                "timestamp": trade["timestamp"]})
        except Exception as e:
            print e
            continue
    return parsedTrades

def consolidateTradesBySymbol(trades):
    symbols = list(set([trade["symbol"] for trade in trades]))
    tradesBySymbol = [] # [{"symbol":..,"buyTrades":..,"sellTrades":..}]
    for symbol in symbols:
        tradesFilteredBySymbol = [trade for trade in trades if trade["symbol"] == symbol]
        tradesBySymbol.append({
            "symbol": symbol,
            "trades": tradesFilteredBySymbol
        })
    return tradesBySymbol

def getTradesCondition(symbol, dates):
    if len(dates) == 0:
        return ""
    tickeridcondition = "tickerid == 'BATS:%s'" % symbol
    datesCondition = " or ".join(["check(timestamp(%d,%d,%d,%d,%d))" % (date['year'], date['month'], date['day'], date['hour'], date['minute']) for date in dates])
    return "%s and (%s)" % (tickeridcondition, datesCondition)

def getPlotShapeFunction(trade):
    return """plotshape(%s, style=shape.%s,  location=location.%s, color=%s, text="%s", size=%s)""" % (trade["condition"], trade["shape"], trade["location"], trade["color"], trade["text"], "size.normal")

def getBGColorFunction(trade):
    return """bgcolor(%s ? %s : na, transp=40)""" % (trade["condition"], trade["color"])

def getSourceCode(tradesBySymbol, symbol):
    symbol = symbol.upper() # case insensitive
    sourceCode = '''
//@version=3
study("'''+symbol+'''", overlay=true)
hoursMinutesBar = hour*60 + minute
END_OF_DAY = 16*60
hoursMinutesLastBar = END_OF_DAY - interval
isLastBar = hoursMinutesBar == hoursMinutesLastBar
check(t) =>
    hoursMinutesT = hour(t)*60 + minute(t)
    year == year(t) and month == month(t) and dayofmonth == dayofmonth(t) and (isdaily or isintraday and ((hoursMinutesBar >= hoursMinutesT - interval and hoursMinutesBar < hoursMinutesT) or (isLastBar and hoursMinutesT >= END_OF_DAY)))
'''
    if symbol is not None:
        tradesFilteredBySymbol = [elem["trades"] for elem in tradesBySymbol if elem["symbol"].upper() == symbol][0] # they are grouped by symbol, so we need the first and only element
        tradesFilteredBySymbol.sort(key=lambda row: datetime.strptime(row['timestamp'][:row['timestamp'].find(".")], DATE_FORMAT))
        tradesFilteredBySymbol = tradesFilteredBySymbol[-64:] # take last 64 trades

        style_mapping = {
            "buy": {
                "shape": "triangleup",
                "location": "belowbar",
                "color": "green",
            },
            "sell": {
                "shape": "triangledown",
                "location": "abovebar",
                "color": "red"
            }
        }

        allTrades = [
            {
                "condition": getTradesCondition(symbol, [trade]),
                "shape": style_mapping[trade["side"]]["shape"],
                "location": style_mapping[trade["side"]]["location"],
                "color": style_mapping[trade["side"]]["color"],
                "text": "%s\\n$%s\\n$%s" % (str(int(trade["quantity"])), str(float(trade["price"])), str(float(trade["quantity"])*float(trade["price"])))
            } for trade in tradesFilteredBySymbol]

        sourceCode += "\n" + "\n".join([getPlotShapeFunction(trade) for trade in allTrades])

    else:
        for elem in tradesBySymbol:
            symbol = elem["symbol"]
            trades = elem["trades"]
            buyTradesCondition = getTradesCondition(symbol, [trade for trade in trades if trade["side"] == "buy"])
            sellTradesCondition = getTradesCondition(symbol, [trade for trade in trades if trade["side"] == "sell"])
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

TRADING_VIEW_OPTION = "tradingview"
exporter = Exporter.Exporter("pinescript code")

parser = argparse.ArgumentParser(description='Generate pinescript to chart your robinhood trades on tradingview.')
parser.add_argument('--debug', action='store_true', help='store raw JSON output to debug.json')
parser.add_argument('--username', required=True, help='your Robinhood username')
parser.add_argument('--password', required=True, help='your Robinhood password')
parser.add_argument('--symbol', help='specific ticker symbol you want (this feature allows you to see the last 64 transactions on the specified symbol)')

exporter.addArgumentsToParser(parser)
args = parser.parse_args()

username = args.username
password = args.password
exporter.parseArguments(args)

######## done with parsing ###############


trades = getRobinhoodTrades(username, password, args.debug)

parsedTrades = parseTrades(trades)

tradesBySymbol = consolidateTradesBySymbol(parsedTrades)

sourceCode = getSourceCode(tradesBySymbol, args.symbol)

exporter.exportText(sourceCode)