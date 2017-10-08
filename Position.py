import re

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

    def to_string(self):
        cost_open = self.total_in / self.total_number_of_shares
        if self.close_date is not None:
            cost_close = self.total_out / self.total_number_of_shares
            profit = (self.total_out - self.total_in)
            profit_percentage = ("%.2f" % (100 * profit / self.total_in)) + "%"

            return "\t".join([self.ticker_symbol , self.format_date(self.open_date) , "B" , str(cost_open) , str(self.total_number_of_shares) , str(self.total_in) , str(cost_close) , str(self.total_out) , str(profit), profit_percentage, self.format_date(self.close_date)])

        else:
            return "\t".join([self.ticker_symbol , self.format_date(self.open_date) , "B" , str(cost_open) , str(self.total_number_of_shares) , str(self.total_in) , "" , "" , "", "", ""])