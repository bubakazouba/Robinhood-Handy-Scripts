
import getpass
import json
import requests
import urllib
import sys
try:     
    from urllib.request import urlretrieve  #py3 
except ImportError:
    from urllib import urlretrieve  # py2

class Robinhood:

    endpoints = {
            "login": "https://api.robinhood.com/api-token-auth/",
            "investment_profile": "https://api.robinhood.com/user/investment_profile/",
            "accounts":"https://api.robinhood.com/accounts/",
            "ach_iav_auth":"https://api.robinhood.com/ach/iav/auth/",
            "ach_relationships":"https://api.robinhood.com/ach/relationships/",
            "ach_transfers":"https://api.robinhood.com/ach/transfers/",
            "applications":"https://api.robinhood.com/applications/",
            "dividends":"https://api.robinhood.com/dividends/",
            "edocuments":"https://api.robinhood.com/documents/",
            "instruments":"https://api.robinhood.com/instruments/",
            "margin_upgrades":"https://api.robinhood.com/margin/upgrades/",
            "markets":"https://api.robinhood.com/markets/",
            "notifications":"https://api.robinhood.com/notifications/",
            "orders":"https://api.robinhood.com/orders/",
            "password_reset":"https://api.robinhood.com/password_reset/request/",
            "portfolios":"https://api.robinhood.com/portfolios/",
            "positions":"https://api.robinhood.com/positions/",
            "quotes":"https://api.robinhood.com/quotes/",
            "historicals":"https://api.robinhood.com/quotes/historicals/",
            "document_requests":"https://api.robinhood.com/upload/document_requests/",
            "user":"https://api.robinhood.com/user/",
            "watchlists":"https://api.robinhood.com/watchlists/",
            "news":"https://api.robinhood.com/midlands/news/"
    }

    session = None

    username = None

    password = None

    headers = None

    auth_token = None


    ##############################
    #Logging in and initializing
    ##############################

    def __init__(self):
        self.session = requests.session()
        if sys.version_info[0] < 3: #py2
	        self.session.proxies = urllib.getproxies()
        else: #py3
            self.session.proxies = urllib.request.getproxies()

        self.headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "en;q=1, fr;q=0.9, de;q=0.8, ja;q=0.7, nl;q=0.6, it;q=0.5",
            "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
            "X-Robinhood-API-Version": "1.0.0",
            "Connection": "keep-alive",
            "User-Agent": "Robinhood/823 (iPhone; iOS 7.1.2; Scale/2.00)"
        }
        self.session.headers = self.headers

    def login_prompt(self):
        """Prompts user for username and password and calls login()."""
        username = raw_input("Username: ")
        password = getpass.getpass()
        return self.login(username=username, password=password)

    def login(self, username, password):
        self.username = username
        self.password = password
        #data = urllib.urlencode({"password" : self.password, "username" : self.username})
        if sys.version_info[0] < 3: #py2
            data = urllib.urlencode({"password" : self.password, "username" : self.username})
        else: #py3
            data = urllib.parse.urlencode({"password" : self.password, "username" : self.username})
        res = self.session.post(self.endpoints['login'], data=data)
        res = res.json()
        if 'token' in res:
             self.auth_token = res['token']
             print('Login successfully')
        elif 'mfa_type' in res:  # When MFA is turned on
             if sys.version_info[0] < 3:
                 mfa_code = raw_input("MFA code: ").strip()
             else:
                 mfa_code = input("MFA code: ").strip()
	
             if sys.version_info[0] < 3:
                 data = urllib.urlencode({"password" : self.password, "username" : self.username, 'mfa_code': mfa_code})
             else:
                 data = urllib.parse.urlencode({"password" : self.password, "username" : self.username, 'mfa_code': mfa_code})
             res_mfa = self.session.post(self.endpoints['login'], data=data)
             res_mfa = res_mfa.json()
             if 'token' in res_mfa:
                 self.auth_token = res_mfa['token']
                 print('Login successfully')
             else:
                 print('Login Failed')
                 return False
        else:
            print('Login Failed')
            return False
        self.headers['Authorization'] = 'Token '+self.auth_token
        return True

    ##############################
    #GET DATA 
    ##############################

    def get_endpoint(self, endpoint=None):
        res = self.session.get(self.endpoints[endpoint])
        return json.loads(res.content.decode('utf-8'))

    def get_custom_endpoint(self, endpoint=None):
        res = self.session.get(endpoint)
        return json.loads(res.content.decode('utf-8'))

    def investment_profile(self):
        self.session.get(self.endpoints['investment_profile'])

    def instruments(self, stock=None):
        res = self.session.get(self.endpoints['instruments'], params={'query':stock.upper()})
        res = res.json()
        return res['results']

    def quote_data(self, stock=None):
        #Prompt for stock if not entered
        if stock is None:
            stock = raw_input("Symbol: ");
        url = str(self.endpoints['quotes']) + str(stock) + "/"
        #Check for validity of symbol
        try:
            if sys.version_info[0] < 3: #py2
                res = json.loads((urllib.urlopen(url)).read().decode('utf-8'));
            else: #py3
                res = json.loads((urllib.request.urlopen(url)).read().decode('utf-8'));
            if len(res) > 0:
                return res;
            else:
                raise NameError("Invalid Symbol: " + stock);
        except (ValueError):
            raise NameError("Invalid Symbol: " + stock);

    def get_quote(self, stock=None):
        data = self.quote_data(stock)
        return data["symbol"]

    def get_historical_quotes(self,symbol,interval,span,bounds='regular'):
        # Valid combination
        # interval = 5minute | 10minute + span = day, week
        # interval = day + span = year
        # interval = week
        # bounds can be 'regular' for regular hours or 'extended' for extended hours
        res = self.session.get(self.endpoints['historicals'], params={'symbols':','.join(symbol).upper(), 'interval':interval, 'span':span, 'bounds':bounds})
        return res.json()
        
    def get_news(self, symbol):
        return self.session.get(self.endpoints['news']+symbol.upper()+"/").json()
        

    def print_quote(self, stock=None):
        data = self.quote_data(stock)
        print(data["symbol"] + ": $" + data["last_trade_price"]);

    def print_quotes(self, stocks):
        for i in range(len(stocks)):
            self.print_quote(stocks[i]);

    def ask_price(self, stock=None):
        return self.quote_data(stock)['ask_price'];

    def ask_size(self, stock=None):
        return self.quote_data(stock)['ask_size'];

    def bid_price(self, stock=None):
        return self.quote_data(stock)['bid_price'];

    def bid_size(self, stock=None):
        return self.quote_data(stock)['bid_size'];

    def last_trade_price(self, stock=None):
        return self.quote_data(stock)['last_trade_price'];

    def previous_close(self, stock=None):
        return self.quote_data(stock)['previous_close'];

    def previous_close_date(self, stock=None):
        return self.quote_data(stock)['previous_close_date'];

    def adjusted_previous_close(self, stock=None):
        return self.quote_data(stock)['adjusted_previous_close'];

    def symbol(self, stock=None):
        return self.quote_data(stock)['symbol'];

    def last_updated_at(self, stock=None):
        return self.quote_data(stock)['updated_at'];
    
    def get_account(self):
        res = self.session.get(self.endpoints['accounts'])
        res = res.json()
        return res['results'][0]
        
    def get_url(self,url):
        return self.session.get(url).json()

    ##############################
    # PORTFOLIOS DATA
    ##############################

    def portfolios(self):
        """Returns the user's portfolio data."""
        return self.session.get(self.endpoints['portfolios']).json()['results'][0]

    def adjusted_equity_previous_close(self):
        return float(self.portfolios()['adjusted_equity_previous_close'])

    def equity(self):
        return float(self.portfolios()['equity'])

    def equity_previous_close(self):
        return float(self.portfolios()['equity_previous_close'])

    def excess_margin(self):
        return float(self.portfolios()['excess_margin'])

    def extended_hours_equity(self):
        return float(self.portfolios()['extended_hours_equity'])

    def extended_hours_market_value(self):
        return float(self.portfolios()['extended_hours_market_value'])

    def last_core_equity(self):
        return float(self.portfolios()['last_core_equity'])

    def last_core_market_value(self):
        return float(self.portfolios()['last_core_market_value'])

    def market_value(self):
        return float(self.portfolios()['market_value'])
        
    def order_history(self):
        return self.session.get(self.endpoints['orders']).json()
        
    def dividends(self):
        return self.session.get(self.endpoints['dividends']).json()

    ##############################
    # POSITIONS DATA
    ##############################

    def positions(self):
        """Returns the user's positions data."""
        return self.session.get(self.endpoints['positions']).json()

    def securities_owned(self):
        """
        Returns a list of symbols of securities of which there are more
        than zero shares in user's portfolio.
        """
        positions = self.positions()
        securities = []
        for position in positions['results']:
            quantity = float(position['quantity'])
            if quantity > 0:
                securities.append(self.session.get(position['instrument']).json()['symbol'])
        return securities

    ##############################
    #PLACE ORDER
    ##############################

    def place_order(self, instrument, quantity=1, bid_price = None, transaction=None):
        if bid_price == None:
            bid_price = self.quote_data(instrument['symbol'])['bid_price']
        data = 'account=%s&instrument=%s&price=%f&quantity=%d&side=%s&symbol=%s&time_in_force=gfd&trigger=immediate&type=market' % (
            self.get_account()['url'],
            urllib.unquote(instrument['url']),
            float(bid_price),
            quantity,
            transaction,
            instrument['symbol']
        ) 
        res = self.session.post(self.endpoints['orders'], data=data)
        return res

    def place_buy_order(self, instrument, quantity, bid_price=None):
        transaction = "buy"
        return self.place_order(instrument, quantity, bid_price, transaction)

    def place_sell_order(self, instrument, quantity, bid_price=None):
        transaction = "sell"
        return self.place_order(instrument, quantity, bid_price, transaction)
