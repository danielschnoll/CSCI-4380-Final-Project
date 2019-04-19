import psycopg2
import psycopg2.extras
import csv
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def setUp():
	connection_string_inner = "host='localhost' dbname='postgres' port='5432'"
	conn_temp = psycopg2.connect(connection_string_inner, cursor_factory=psycopg2.extras.DictCursor)
	conn_temp.autocommit = True
	conn_temp.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
	with conn_temp.cursor() as cursor:
		cursor.execute("DROP DATABASE IF EXISTS stocks")
		cursor.execute("CREATE DATABASE stocks")
		cursor.execute("DROP USER IF EXISTS stocks")
		cursor.execute("CREATE USER stocks WITH PASSWORD 'stocks'")
		cursor.execute("GRANT ALL PRIVILEGES ON DATABASE stocks TO stocks")
		cursor.execute("ALTER USER stocks SET search_path = stocks")
	connection_string = "host='localhost' dbname='stocks' user='stocks' password='stocks' port='5432'"

	conn_main = psycopg2.connect(connection_string, cursor_factory=psycopg2.extras.DictCursor)
	cur = conn_main.cursor()
	cur.execute("DROP SCHEMA IF EXISTS testing CASCADE");
	cur.execute("CREATE SCHEMA stocks")
	cur.execute("""
		CREATE TABLE securities(
			Ticker text PRIMARY KEY,
			Security text,
			SECFilings text,
			GICSSector text,
			GICSSubIndustry text,
			Address text,
			DateAdded text,
			CIK integer
		)
	""")
	conn_main.commit()
	cur.execute("""
		CREATE TABLE prices(
			date_ DATE,
			symbol varchar(5) REFERENCES securities(Ticker),
			open Numeric(10,6),
			close Numeric(10,6),
			low Numeric(10,6),
			high Numeric(10,6),
			volume Numeric(10,1),
			PRIMARY KEY (symbol, date_)
		) 
	""")
	conn_main.commit()
	cur.execute("""
		CREATE TABLE fundamentals(
			symbol varchar(5) REFERENCES securities(Ticker),
			ending_ DATE,
			payable Numeric(13,1),
			receivable Numeric(13, 1),
			add_inc_expense Numeric(13, 1),
			roe Numeric(5, 1),
			capital_expenditure Numeric(13, 1),
			capital_surplus Numeric(13, 1),
			cash_ratio Numeric(5, 1),
			cash_equity Numeric(13, 1),
			inventory_changes Numeric(11, 1),
			common_stock Numeric(13, 1),
			cost_of_revenue Numeric(13, 1),
			current_ratio Numeric(5, 1),
			deferred_asset_charges Numeric(13, 1),
			deferred_liability_charges Numeric(13, 1),
			depreciation Numeric(13, 1),
			earnings_before_interest_and_tax Numeric(13, 1),
			earnings_before_tax Numeric(13, 1),
			PRIMARY KEY (symbol, ending_)
		)
	""")
	conn_main.commit()
	with open('securities.csv', 'r') as f:
		reader = csv.reader(f)
		next(reader)  # Skip the header row.
		for row in reader:
			cur.execute(
				"INSERT INTO securities VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",row
			)
	conn_main.commit()
	with open('prices.csv', 'r') as f:
		reader = csv.reader(f)
		next(reader)
		for row in reader:
			cur.execute(
				"INSERT INTO prices VALUES (%s, %s, %s, %s, %s, %s, %s)",
				row
			)
	conn_main.commit()
	with open('fundamentals.csv', 'r') as f:
		reader = csv.reader(f)
		next(reader)

		for row in reader:
			row = [None if i == '' else i for i in row]
			cur.execute(
				"INSERT INTO fundamentals VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
				row[1:20]
			)
	conn_main.commit()
setUp()