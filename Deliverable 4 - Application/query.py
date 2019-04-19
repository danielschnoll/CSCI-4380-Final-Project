import psycopg2
import unittest

connection_string = "host='localhost' dbname='stocks' user='stocks' password='stocks'"
conn = psycopg2.connect(connection_string)
cursor = conn.cursor()

def minStockByState(state, minAmount, date):
    cursor.execute("SELECT DISTINCT prices.symbol, prices.date_, prices.close, securities.Address, securities.Security FROM securities, prices WHERE securities.Ticker = prices.symbol;")
    records = cursor.fetchall()
    stocks=[]

    for r in records:
        if state.lower() in r[3].lower() and str(r[1]) == date and str(r[2]) >= minAmount:
            stocks.append( (r[0], r[4], str(r[2])) )
    print stocks


if __name__ == '__main__':
    minStockByState("CA", "20", '2016-01-06')
