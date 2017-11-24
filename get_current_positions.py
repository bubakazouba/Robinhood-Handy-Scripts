import Exporter
import argparse
from Robinhood import Robinhood

def get_positions(robinhood):
	positions = robinhood.positions()['results']
	results = []
	for position in positions:
		buy_price = float(position['average_buy_price'])
		instrument = position['instrument']
		quantity = int(float(position['quantity']))
		if quantity == 0:
			continue
		symbol = robinhood.get_custom_endpoint(instrument)['symbol']
		current_price = float(robinhood.quote_data(symbol)['last_trade_price'])
		price_move = (current_price - buy_price) * quantity
		
		percentage_move = (current_price - buy_price)/current_price
		percentage_move_str = ("%+.2f" % (percentage_move * 100)) + "%"
		price_move_str = ("+" if price_move >= 0 else "-") + "$%.2f" % abs(price_move)
		buy_price_str = "$%.2f" % buy_price
		current_price_str = "$%.2f" % current_price
		quantity_str = str(quantity)
		results.append((symbol, quantity_str+'x'+buy_price_str, current_price_str, percentage_move_str, price_move_str))

	return results

exporter = Exporter.Exporter("positions")

parser = argparse.ArgumentParser(description='Generate pinescript to chart your robinhood trades on tradingview.')
parser.add_argument('--debug', action='store_true', help='store raw JSON output to debug.json')
parser.add_argument('--username', required=True, help='your Robinhood username')
parser.add_argument('--password', required=True, help='your Robinhood password')
exporter.addArgumentsToParser(parser)
args = parser.parse_args()

username = args.username
password = args.password
exporter.parseArguments(args)

robinhood = Robinhood()
robinhood.login(username=username, password=password)

results = get_positions(robinhood)
positionsText = '\n'.join(['    '.join(result) for result in results])

exporter.exportText(positionsText)
