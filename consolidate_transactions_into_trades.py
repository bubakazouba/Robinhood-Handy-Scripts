import csv, re, datetime

class Position(object):
    def __init__(self):
        self.total_in = None
        self.total_out = None
        self.ticker_symbol = None
        self.total_number_of_shares = None
        self.remaining_number_of_shares = None
        self.open_date = None
        self.close_date = None

    def format_date(self, date):
        match = re.match("(\d{4})-(\d{2})-(\d{2})",date)
        yyyy = match.group(1)
        mm = match.group(2)
        dd = match.group(3)
        return "%s/%s/%s" % (mm, dd, yyyy)

    def print_position(self):
        cost_open = self.total_in / self.total_number_of_shares
        if self.total_out is not None:
            cost_close = self.total_out / self.total_number_of_shares
            profit = (self.total_out - self.total_in)
            profit_percentage = ("%.2f" % (100 * profit / self.total_in)) + "%"

            print("\t".join([self.ticker_symbol , self.format_date(self.open_date) , "B" , str(cost_open) , str(self.total_number_of_shares) , str(self.total_in) , str(cost_close) , str(self.total_out) , str(profit), profit_percentage, self.format_date(self.close_date)]))

        else:
            print("\t".join([self.ticker_symbol , self.format_date(self.open_date) , "B" , str(cost_open) , str(self.total_number_of_shares) , str(self.total_in) , "" , "" , "", "", ""]))


current_positions = {}
closed_positions = []

file = open('robinhood.csv', 'rb')
reader = csv.reader(file)

all_rows = []
isHeaderRow = 1
for row in reader:
    if isHeaderRow == 1:
        headerRow = row
        isHeaderRow = 0
        continue

    all_rows.append(row)

all_rows.sort(key=lambda row: datetime.datetime.strptime(row[headerRow.index('Date purchased')][:row[headerRow.index('Date purchased')].find(".")], '%Y-%m-%dT%H:%M:%S'))

for row in all_rows:
    current_transaction_type = row[headerRow.index('Transaction type')]
    current_ticker_symbol = row[headerRow.index('Symbol')]
    current_number_of_shares = float(row[headerRow.index('Shares')])
    current_date = row[headerRow.index('Date purchased')]

    if current_transaction_type == 'buy':
        current_open_price = float(row[headerRow.index('Purchase price per share')])

        if current_positions.has_key(current_ticker_symbol):
            current_positions[current_ticker_symbol].total_in += current_number_of_shares * current_open_price
            current_positions[current_ticker_symbol].total_number_of_shares += current_number_of_shares
            current_positions[current_ticker_symbol].remaining_number_of_shares += current_number_of_shares
        else:
            current_positions[current_ticker_symbol] = Position()
            current_positions[current_ticker_symbol].total_in = current_number_of_shares * current_open_price
            current_positions[current_ticker_symbol].ticker_symbol = current_ticker_symbol
            current_positions[current_ticker_symbol].total_number_of_shares = current_number_of_shares
            current_positions[current_ticker_symbol].remaining_number_of_shares = current_number_of_shares
            current_positions[current_ticker_symbol].open_date = current_date

    elif current_transaction_type == 'sell':
        if not current_positions.has_key(current_ticker_symbol):
            # print "ERROR", current_ticker_symbol
            continue # error: just skip it

        current_close_price = float(row[headerRow.index('Purchase price per share')])

        if current_positions[current_ticker_symbol].total_out == None:
            current_positions[current_ticker_symbol].total_out = current_number_of_shares * current_close_price
        else:
            current_positions[current_ticker_symbol].total_out += current_number_of_shares * current_close_price

        current_positions[current_ticker_symbol].remaining_number_of_shares -= current_number_of_shares

        if current_positions[current_ticker_symbol].remaining_number_of_shares == 0:
            current_positions[current_ticker_symbol].close_date = current_date
            closed_positions.append(current_positions[current_ticker_symbol])
            del current_positions[current_ticker_symbol]

print("\t".join(["Symbol", "Open Date", "Side" , "Cost Open/Share" , "# Shares" , "total in" , "Cost Close/Share" , "Total Out" , "Profit", "Profit %", "Close Date"]))
closed_positions.sort(key=lambda x: datetime.datetime.strptime(x.open_date[:x.open_date.find(".")], '%Y-%m-%dT%H:%M:%S'))

for closed_position in closed_positions:
    closed_position.print_position()


for current_ticker_symbol in current_positions.keys():
    current_positions[current_ticker_symbol].print_position()

 
file.close()


