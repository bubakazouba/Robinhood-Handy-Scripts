import re, argparse
from datetime import datetime
from Position import Position
from GetRobinhoodTrades import getRobinhoodTrades
import Exporter

DATE_FORMAT = '%Y-%m-%dT%H:%M:%S'

def consolidateTrades(trades):
    trades.sort(key=lambda row: datetime.strptime(row['timestamp'][:row['timestamp'].find(".")], DATE_FORMAT))

    current_positions = {}
    closed_positions = []

    for trade in trades:
        current_side = trade['side']
        current_symbol = trade['symbol']
        current_quantity = float(trade['quantity'])
        current_date = trade['timestamp']

        if current_side == 'buy':
            current_open_price = float(trade['price'])

            if current_positions.has_key(current_symbol):
                current_positions[current_symbol].total_in += current_quantity * current_open_price
                current_positions[current_symbol].total_number_of_shares += current_quantity
                current_positions[current_symbol].remaining_number_of_shares += current_quantity
            else:
                current_positions[current_symbol] = Position()
                current_positions[current_symbol].total_in = current_quantity * current_open_price
                current_positions[current_symbol].ticker_symbol = current_symbol
                current_positions[current_symbol].total_number_of_shares = current_quantity
                current_positions[current_symbol].remaining_number_of_shares = current_quantity
                current_positions[current_symbol].open_date = current_date

        elif current_side == 'sell':
            if not current_positions.has_key(current_symbol):
                print "ERROR at symbol: '%s'. Skipping.." % current_symbol
                continue # error: just skip it

            current_close_price = float(trade['price'])

            if current_positions[current_symbol].total_out == None:
                current_positions[current_symbol].total_out = current_quantity * current_close_price
            else:
                current_positions[current_symbol].total_out += current_quantity * current_close_price

            current_positions[current_symbol].remaining_number_of_shares -= current_quantity

            if current_positions[current_symbol].remaining_number_of_shares == 0:
                current_positions[current_symbol].close_date = current_date
                closed_positions.append(current_positions[current_symbol])
                del current_positions[current_symbol]

    current_positions = [current_positions[symbol] for symbol in current_positions.keys()]

    return closed_positions, current_positions

#############################################################################################
#############################################################################################
######################################END FUNCTIONS##########################################
#############################################################################################
#############################################################################################
exporter = Exporter.Exporter("trades")

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

closed_positions, current_positions = consolidateTrades(trades)
# sort by time
closed_positions.sort(key=lambda x: datetime.strptime(x.close_date[:x.close_date.find(".")], '%Y-%m-%dT%H:%M:%S'))
current_positions.sort(key=lambda x: datetime.strptime(x.open_date[:x.open_date.find(".")], '%Y-%m-%dT%H:%M:%S'))

# print header row
consolidated_trades = "\t".join(["Symbol", "Open Date", "Side" , "Cost Open/Share" , "# Shares" , "total in" , "Cost Close/Share" , "Total Out" , "Profit", "Profit %", "Close Date"])
consolidated_trades += '\n'
consolidated_trades += '\n'.join([position.to_string() for position in closed_positions])
consolidated_trades += '\n'
consolidated_trades += '\n'.join([position.to_string() for position in current_positions])

exporter.exportText(consolidated_trades)
