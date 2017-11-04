import Exporter
import argparse
from Robinhood import Robinhood

def get_price(symbol):
	symbol = symbol.upper()
	robinhood = Robinhood()
	robinhood.login(username=username, password=password)

	current_price = float(robinhood.quote_data(symbol)['last_trade_price'])
	current_price_str = "$%.2f" % current_price

        print symbol
        x = robinhood.quote_data(symbol)['last_extended_hours_trade_price']
	if x is None:
		return current_price_str

	extended_price = float(x)
	extended_price_str = "$%.2f" % extended_price

	return current_price_str + "," + extended_price_str

exporter = Exporter.Exporter("positions")

parser = argparse.ArgumentParser(description='Generate pinescript to chart your robinhood trades on tradingview.')
parser.add_argument('--debug', action='store_true', help='store raw JSON output to debug.json')
parser.add_argument('--username', required=True, help='your Robinhood username')
parser.add_argument('--password', required=True, help='your Robinhood password')
parser.add_argument('--symbol',   required=True, help='specific ticker symbol you want (this feature allows you to see the last 64 transactions on the specified symbol)')
exporter.addArgumentsToParser(parser)
args = parser.parse_args()

username = args.username
password = args.password
exporter.parseArguments(args)

exporter.exportText(get_price(args.symbol))
