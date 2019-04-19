from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

PORT = 5000
HOST = '0.0.0.0'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("POSTGRES_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app)

if os.environ.get("POSTGRES_URI") is None:
	print("ERROR: Environment Variable not set..")
	exit(0)

db = SQLAlchemy(app)
db.init_app(app)


@app.route('/')
def main():
    return "Hello"

if __name__ == '__main__':
	print("running Stock Ticker webserver..")
	app.run(port=PORT, host=HOST, debug=True)