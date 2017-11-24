# Robinhood handy scripts


### Description
#### A collection of Python scripts to export your [Robinhood](https://www.robinhood.com) trades to a:

* .csv file (In a nice, Google Finance friendly format).
* consolidated trades that you can put in an excel or a google sheet to analyze your trades
* pinescript that you can paste to your TradingView account to see your trades in the chart.

#### Other scripts:
* get all your current positions
* get price for a ticker

### Inital setup:
`pip install -r requirements.txt`

### Quick start:
* edit `start.sh` with your robinhood username and password
* `chmod +x start.sh`

	| script to run | command to use | cmd to use with ticker |
	| ------------- | -------------- | ------------------------------------- |
	| `consolidate_transactions_into_trades.py` | `./start.sh sheets` | N/A |
	| `generate_pine_script.py` | `./start.sh pine` | `./start.sh pine "--symbol AAPL"` |
	| `get_current_positions` | `./start.sh positions` | N/A |
	| `get_current_positions` | N/A | `./start.sh price "--symbol AAPL"` |
* see below for an explanation of what each script does


### Scripts:
#### google\_finance\_export.py:	
`python gf-export.py --username '<username>' --password '<password>' --export-to 'file|clipboard' (--file-name '<filename>')`

#### what it does:
* Basically exports a csv of your robinhood trades to either a file or your clipboard.
    
* Meant to be uploaded and viewed in google finance.

--

### consolidate\_transactions\_into\_trades.py:
`python consolidate_transactions_into_trades.py --username '<username>' --password '<password>' --export-to 'file|clipboard' (--file-name '<filename>')`

#### what it does:
* Conslidatation of trades work by grouping all of the trades that are in the same position into one trade.

* So if you adjust your position by adding more to it or selling some, it will still be considered the same position until you completely exit.

* As you can see, it is not entirely accurate and can result in some weird numbers if you have had a position for a very long time and you keep adding and selling shares from it.

* Note: Does not work for shorting (Robinhood doesnt support it now anyways).

* You can paste the output of this script into this [sheet.](https://docs.google.com/spreadsheets/d/1Wf5O2SgrdhL-7T4OeYMpCWMbZ5SoPeWuQ2STkEqcsDY) (create a copy first. **File --> Create a copy**) and you will get a neat colored spreadsheet like this:

	![Trades](https://i.imgur.com/0IBWdEf.png)

--

### generate\_pine\_script.py
`python generate_pine_script.py --username '<username>' --password '<password>' --export-to 'file|clipboard' (--file-name '<filename>')`

#### what it does:
* Generates a pinescript that you can copy and paste to your tradingview account to see all your trades embedded in the chart in the form of green and red arrows (for buy and sell respecitvely).

	![TradingView](https://i.imgur.com/uAVoFPB.png)

--

### get\_current\_positions.py
`python get_current_positions.py --username "<username>" --password '<password>' --export-to 'clipboard'`

#### what it does:
* gets current position in a format like this:

	```
	DPZ    8x$176.06    $176.55    +0.28%    +$3.94
	ACIA    45x$38.45    $39.02    +1.46%    +$25.65
	QCOM    35x$66.46    $68.13    +2.46%    +$58.60
	NFLX    8x$194.83    $196.32    +0.76%    +$11.93
	BAC    60x$26.43    $26.66    +0.87%    +$13.86
	AAPL    16x$173.45    $174.96    +0.86%    +$24.16
	V    14x$111.50    $110.82    -0.61%    -$9.52
	```

--

### get\_price.py
`python get_price.py --username "<username>" --password '<password>' --symbol "<ticker>" --export-to 'clipboard'`

#### what it does:
* gets you the price for a specific ticker
* 

--------
--------

### Installation
#### Windows
All you need to do on windows is download and install the latest version of python (2.7.X or 3.X, probably 3.X as you may run in to fewer issues) [here](https://www.python.org/downloads/).  Make sure that when you're installing, select the option to include python in your windows path (it will be a check box before you start the installation).  After that, double click the .bat file.  This will run both of the commands listed below.  It's important to read .bat files in particular, as they have potential to be extremely malicious.  Try editing the run.bat file in your favorite text editor and confirm it is only running those two commands. I've also included some useful comments, in case you need help understanding what's going on!

If you run in to issues during this process, please check out the troubleshooting readme called "troubleshooting.md".  I've tried to include as many obvious fixes as possible, but if I missed something please contact me and I'll add it to the list.  

#### Linux/maybe osx
Someone actually wrote a nice article showing how to run this [here](http://ask.xmodulo.com/export-robinhood-transaction-data.html).
