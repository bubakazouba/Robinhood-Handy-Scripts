from Robinhood import Robinhood
import pickle
import os.path

def getRobinhoodTrades(username, password, debug=False):
    robinhood = Robinhood()

    logged_in = robinhood.login(username=username, password=password)
    if logged_in == False:
        print("Invalid username or password.  Try again.\n")
        return None

    trades = []
    cached_instruments = {} #{instrument:symbol}
    robinhood_cache = {}
    last_page_url = None

    if os.path.isfile("robinhood_cache"):
        robinhood_cache = pickle.load(open("robinhood_cache", "rb"))
        # last_page_url = robinhood_cache['last_page_url']
        print last_page_url
        cached_instruments = robinhood_cache['instruments']
        # trades = robinhood_cache['trades']
    
    if not os.path.isfile("robinhood_cache") or last_page_url is None:
        # fetch order history and related metadata from the Robinhood API
        orders = robinhood.get_endpoint('orders')
    else:
        orders = robinhood.get_custom_endpoint(last_page_url)

    # do/while for pagination

    #pagination
    paginated = True
    page = 0
    length_of_trades_at_last_page = len(trades)
    while paginated:
        for i, order in enumerate(orders['results']):
            executions = order['executions']
            if len(executions) > 0:
                # Iterate over all the different executions
                for execution in executions:
                    # Get the Symbol of the order
                    trades.append({})
                    if not cached_instruments.has_key(order['instrument']):
                        cached_instruments[order['instrument']] = robinhood.get_custom_endpoint(order['instrument'])['symbol']

                    trades[-1]['symbol'] = cached_instruments[order['instrument']]

                    # Get all the key,value from the order
                    for key, value in enumerate(order):
                        if value != "executions":
                            trades[-1][value] = order[value]

                    # Get specific values from the execution of the order
                    trades[-1]['timestamp'] = execution['timestamp']
                    trades[-1]['quantity'] = execution['quantity']
                    trades[-1]['price'] = execution['price']
            elif order['state'] == "queued":
                pass

        if orders['next'] is not None:
            page = page + 1
            #get the next order, a page is essentially one order
            if debug:
               print (str(page) + "," + orders['next'])
            last_page_url = orders['next']
            length_of_trades_at_last_page = len(trades)
            orders = robinhood.get_custom_endpoint(orders['next'])
            
        else:
            paginated = False

    robinhood_cache['last_page_url'] = last_page_url
    robinhood_cache['instruments'] = cached_instruments
    robinhood_cache['trades'] = trades[:length_of_trades_at_last_page] # dont include trades of the last page, because they will be queried for again
    pickle.dump(robinhood_cache, open("robinhood_cache", "wb"))

    # check we have trade data to export
    if len(trades) > 0:
        print("%d executed trades found in your account." % len(trades))
    else:
        print("No trade history found in your account.")
        quit()

    # parse float keys    
    float_keys = ["price","fees","quantity"]
    for trade in trades:
        for key in float_keys:
            try:
                trade[key] = round(float(trade[key]),2)
            except:
                continue

    return trades