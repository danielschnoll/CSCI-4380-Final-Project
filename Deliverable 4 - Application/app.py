from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.datastructures import ImmutableMultiDict
from query import *
import os

PORT = 5000
HOST = '0.0.0.0'

app = Flask(__name__)

@app.route('/')
def main():
    return render_template("main.html")

# Pull information from the request form, execue query based on
# which submit button was entered
@app.route('/query', methods=['POST'])
def querypage():
    result = request.form
    result = result.to_dict(flat=False)
    try:
        print(result['submit1'])
        submitVals = list(result.values())
        stocks = minStockByState(submitVals[1][0], submitVals[0][0], submitVals[2][0])
        return render_template("query.html", result = stocks, btn="1")
    except:
        try:
            print(result['submit2'])
            submitVals = list(result.values())
            record = findMaxMinForIndustry(submitVals[0][0])
            return render_template("secondquery.html", result = record, btn="2")
        except:
            try:
                print(result['submit3'])
                submitVals = list(result.values())
                record = highestStockPriceByDate(submitVals[0][0])
                return render_template("query.html", result=record, btn="3")
            except:
                try:
                    print(result['submit4'])
                    submitVals = list(result.values())
                    record = investmentInfo(submitVals[0][0], submitVals[1][0])
                    return render_template("fourthquery.html", type= submitVals[0][0], name=submitVals[1][0], result = record, btn="4")
                except:
                    try: 
                        print(result['submit5'])
                        submitVals = list(result.values())
                        CandleStick(submitVals[0][0])
                        return render_template("fifthquery.html", name=submitVals[0][0], btn="5")
                    except:
                        raise

if __name__ == '__main__':
	print("running Stock Ticker webserver..")
	app.run(port=PORT, host=HOST, debug=True)