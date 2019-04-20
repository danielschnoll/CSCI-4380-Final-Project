import psycopg2
import unittest
import matplotlib
from mpl_finance import candlestick_ohlc
from matplotlib import pyplot as plt
from matplotlib import ticker as ticker
import datetime as datetime
from matplotlib import dates as mdates

connection_string = "host='localhost' dbname='stocks' user='stocks' password='stocks'"
conn = psycopg2.connect(connection_string)

def minStockByState(state, minAmount, date):
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT prices.symbol, prices.date_, prices.close, securities.Address, securities.Security FROM securities, prices WHERE securities.Ticker = prices.symbol;")
    records = cursor.fetchall()
    stocks=[]

    for r in records:
        if state.lower() in r[3].lower() and str(r[1]) == date and float(r[2]) >= float(minAmount):
            stocks.append( (r[0], r[4], str(r[2])) )
    return stocks

def highestStockPriceByDate(date):
    cursor = conn.cursor()
    sql = """
        SELECT DISTINCT securities.Ticker, securities.Security, prices.high
        FROM securities, prices 
        WHERE prices.high = 
            (select max(high) from prices 
            WHERE prices.date_ = '{}')
        AND securities.Ticker = prices.symbol;
    """.format(date)
    cursor.execute(sql)
    records = cursor.fetchall()

    secondsql = """
        SELECT DISTINCT securities.Ticker, securities.Security, prices.high
        FROM securities, prices 
        WHERE prices.high = 
            (select min(high) from prices 
            WHERE prices.date_ = '{}')
        AND securities.Ticker = prices.symbol;
    """.format(date)
    cursor.execute(secondsql)
    allRec = cursor.fetchall()
    return records+allRec

def findMaxMinForIndustry(industry):
	cursor = conn.cursor()
	sql = """
		SELECT  min(p.open), max(p.open) from prices as p
		JOIN securities s on p.symbol = s.ticker
		where s.gicssector = '%s'
	"""
	cursor.execute(sql %(industry))
	records = cursor.fetchone()
	return records

def investmentInfo(financeInfo, stockTicker):
    cursor = conn.cursor()
    val = "earnings_before_tax"
    if(financeInfo == "Capital Expenditure"):
        val = "capital_expenditure"
    elif(financeInfo == "Common Stock"):
        val = "common_stock"
    elif(financeInfo == "Current Ratio"):
        val = "current_ratio"
    else:
        val = "earnings_before_tax"
    
    sql = """
        SELECT fundamentals.%s
        FROM fundamentals
        WHERE fundamentals.symbol = '%s';
    """
    cursor.execute(sql %(val, stockTicker))
    records = cursor.fetchone()
    return records

'''
WORKS WITH APC, CCL
'''
def CandleStick(ticker):
	cursor = conn.cursor()
	sql = """ SELECT * FROM prices where symbol = '%s' """
	cursor.execute(sql % (ticker))
	records = cursor.fetchall()
	dates = []
	_open = []
	_high = []
	_low = []
	_close = []
	for i in records:
		dates.append(i[0])
		_open.append(i[2])
		_high.append(i[5])
		_low.append(i[4])
		_close.append(i[3])
	#print(records)
	fig, ax = plt.subplots()
	#ax.xaxis.set_minor_locator(alldays)
	#ax.xaxis.set_major_formatter(weekFormatter)
	candlestick_ohlc(ax, zip(mdates.date2num(dates),_open, _high, _low, _close), width=0.60)
	plt.show()

if __name__ == '__main__':
    # print minStockByState("CA", "100", '2016-01-06')
    # print(highestStockPriceByDate('2016-01-07'))
    print(investmentInfo("Common Stock", "AAPL"))
    # print (CandleStick("AAPL"))
    print("ran query")
