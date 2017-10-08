from GetRobinhoodTrades import getRobinhoodTrades
import argparse
import Exporter

exporter = Exporter.Exporter("trades")

parser = argparse.ArgumentParser(description='Export Robinhood trades to a CSV file')
parser.add_argument('--debug', action='store_true', help='store raw JSON output to debug.json')
parser.add_argument('--username', required=True, help='your Robinhood username')
parser.add_argument('--password', required=True, help='your Robinhood password')
exporter.addArgumentsToParser(parser)
args = parser.parse_args()

username = args.username
password = args.password
exporter.parseArguments(args)

trades = getRobinhoodTrades(username, password, args.debug)

# CSV headers
# filter out keys we dont need, also change names of keys

desired_keys_mappings = {
    "price": "Purchase price per share",
    "timestamp": "Date purchased",
    "fees": "Commission",
    "quantity": "Shares",
    "symbol": "Symbol",
    "side": "Transaction type"
}
desired_keys = sorted(desired_keys_mappings.keys())
keys = [desired_keys_mappings[key] for key in sorted(trades[0].keys()) if key in desired_keys]

csv = ""
csv += ",".join(keys)
csv += "\n"

# CSV rows
csvb = []

for trade in trades:
    line = ','.join([str(trade[key]) for key in desired_keys])
    csvb.append(line)

#google finance seems to prefer dates in ascending order, so we must reverse the given order
csv += '\n'.join(reversed(csvb))

exporter.exportText(csv)