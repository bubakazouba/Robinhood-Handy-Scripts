# Robinhood for Google Finance


### Description
A collection of Python scripts to export your [Robinhood](https://www.robinhood.com) trades to a:

* .csv file .csv file (In a nice, Google Finance friendly format).
* consolidated trades that you can put in an excel or a google sheet to analyze your trades
* pinescript that you can paste to your TradingView account to see your trades in the chart.

Credit:

* [Robinhood library by Rohan Pai](https://github.com/Jamonek/Robinhood)
* [Robinhood to CSV by Josh Fraser](https://github.com/joshfraser).
* 
Works on Python 2.7+ and 3.5+

### Configuration:
    pip install -r requirements.txt

### Scripts:
#### google\_finance\_export.py:	
   `python gf-export.py --username '<username>' --password '<password>' --export-to 'file|clipboard' (--file-name '<filename>')`

Basically exports a csv of your robinhood trades to either a file or your clipboard.
    
Meant to be uploaded and viewed in google finance.

#### consolidate\_transactions\_into\_trades.py:
  	`python consolidate_transactions_into_trades.py --username '<username>' --password '<password>' --export-to 'file|clipboard' (--file-name '<filename>')`

Conslidatation of trades work by grouping all of the trades that are in the same position into one trade.

So if you adjust your position by adding more to it or selling some, it will still be considered the same position until you completely exit.

As you can see, it is not entirely accurate and can result in some weird numbers if you have had a position for a very long time and you keep adding and selling shares from it.

Does not work for shorting (robinhood doesnt support it now anyways).

### generate\_pine\_script.py
  	`python generate_pine_script.py --username '<username>' --password '<password>' --export-to 'file|clipboard' (--file-name '<filename>')`
  	
Generates a pinescript that you can copy and paste to your tradingview account to see all your trades embedded in the chart in the form of green and red arrows (for buy and sell respecitvely).



### Installation
#### Windows
All you need to do on windows is download and install the latest version of python (2.7.X or 3.X, probably 3.X as you may run in to fewer issues) [here](https://www.python.org/downloads/).  Make sure that when you're installing, select the option to include python in your windows path (it will be a check box before you start the installation).  After that, double click the .bat file.  This will run both of the commands listed below.  It's important to read .bat files in particular, as they have potential to be extremely malicious.  Try editing the run.bat file in your favorite text editor and confirm it is only running those two commands. I've also included some useful comments, in case you need help understanding what's going on!

If you run in to issues during this process, please check out the troubleshooting readme called "troubleshooting.md".  I've tried to include as many obvious fixes as possible, but if I missed something please contact me and I'll add it to the list.  

#### Linux/maybe osx
Someone actually wrote a nice article showing how to run this [here](http://ask.xmodulo.com/export-robinhood-transaction-data.html).
