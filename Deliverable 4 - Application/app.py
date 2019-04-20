1. Find [Min Stock Price] By [State] on [Date(2016-01-07)] submit
2. Find [Max Stock Price] and [Mind Stock Price] for [Industry] submit
3. Find Highest Stock Price on [Date] submit


from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import matplotlib
import os

PORT = 5000
HOST = '0.0.0.0'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("POSTGRES_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

if os.environ.get("POSTGRES_URI") is None:
	print("ERROR: Environment Variable not set..")
	exit(0)

db = SQLAlchemy(app)
db.init_app(app)


@app.route('/')
def main():
    return render_template("main.html")

@app.route('/query', methods=['POST'])
def querypage():
    result = request.form
    return render_template("query.html", result = result)

if __name__ == '__main__':
	print("running Stock Ticker webserver..")
	app.run(port=PORT, host=HOST, debug=True)