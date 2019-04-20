import psycopg2
import unittest

connection_string = "host='localhost' dbname='stocks' user='stocks' password='stocks'"
conn = psycopg2.connect(connection_string)

def minStockByState(state, minAmount, date):
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT prices.symbol, prices.date_, prices.close, securities.Address, securities.Security FROM securities, prices WHERE securities.Ticker = prices.symbol;")
    records = cursor.fetchall()
    stocks=[]

    for r in records:
        if state.lower() in r[3].lower() and str(r[1]) == date and str(r[2]) >= minAmount:
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
    return records

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


if __name__ == '__main__':
    # minStockByState("CA", "20", '2016-01-06')
    print(highestStockPriceByDate('2016-01-07'))
