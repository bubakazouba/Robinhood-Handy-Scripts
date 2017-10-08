from Robinhood import Robinhood
import getpass
import collections
import ast

def getRobinhoodTrades(username, password, debug=False):
	logged_in = False
	robinhood = Robinhood();

	# login to Robinhood
	while not logged_in:
	    if username == "":
	        print("Robinhood username:")
	        try: input = raw_input
	        except NameError: pass
	        username = input()
	    if password == "":
	        password = getpass.getpass()

	    logged_in = robinhood.login(username=username, password=password)
	    if logged_in == False:
	        password = ""
	        print ("Invalid username or password.  Try again.\n")

	trades = []
	trade_count = 0
	queued_count = 0

	# fetch order history and related metadata from the Robinhood API
	orders = robinhood.get_endpoint('orders')

	# load a debug file
	# raw_json = open('debug.txt','rU').read()
	# orders = ast.literal_eval(raw_json)

	# store debug 
	if debug:
	    # save the CSV
	    try:
	        with open("debug.txt", "w+") as outfile:
	            outfile.write(str(orders))
	            print("Debug infomation written to debug.txt")
	    except IOError:
	        print('Oops.  Unable to write file to debug.txt')

	# do/while for pagination

	#pagination
	paginated = True
	page = 0

	#cache instruments
	cached_instruments = {} #{instrument:symbol}

	while paginated:
	    for i, order in enumerate(orders['results']):
	        executions = order['executions']
	        if len(executions) > 0:
	            trade_count += 1
	            # Iterate over all the different executions
	            for execution in executions:
	                # Get the Symbol of the order
	                trades.append({})
	                trades[-1]['symbol'] = cached_instruments.get(order['instrument'], robinhood.get_custom_endpoint(order['instrument'])['symbol'])
	                cached_instruments[order['instrument']] = trades[-1]['symbol']

	                # Get all the key,value from the order
	                for key, value in enumerate(order):
	                    if value != "executions":
	                        trades[-1][value] = order[value]

	                # Get specific values from the execution of the order
	                trades[-1]['timestamp'] = execution['timestamp']
	                trades[-1]['quantity'] = execution['quantity']
	                trades[-1]['price'] = execution['price']
	        # If the state is queued, we keep this to let the user know they are pending orders
	        elif order['state'] == "queued":
	            queued_count += 1

	    # paginate, if out of ORDERS paginate is OVER
	    if orders['next'] is not None:
	        page = page + 1
	        #get the next order, a page is essentially one order
	        orders = robinhood.get_custom_endpoint(str(orders['next']))
	    else:
	        paginated = False

	#for i in trades:
	#     print trades[i]
	#     print "-------"    
	#trades stores ALL relevant information

	# check we have trade data to export
	if trade_count > 0 or queued_count > 0:
	    print("%d queued trade%s and %d executed trade%s found in your account." % (queued_count, "s"[queued_count==1:], trade_count, "s"[trade_count==1:]))
	    # print str(queued_count) + " queded trade(s) and " + str(trade_count) + " executed trade(s) found in your account."
	else:
	    print("No trade history found in your account.")
	    quit()

	# parse float keys	
	floatKeys = ["price","fees","quantity"]
	for trade in trades:
	    for key in floatKeys:
	        try:
				trade[key] = round(float(trade[key]),2)
	        except:
	            continue

	return trades