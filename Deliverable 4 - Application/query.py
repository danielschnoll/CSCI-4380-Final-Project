import psycopg2
import unittest

connection_string = "host='localhost' dbname='stocks' user='stocks' password='stocks'"
conn = psycopg2.connect(connection_string)
cursor = conn.cursor()

cursor.execute("SELECT * FROM prices")
records = cursor.fetchone()
print records
