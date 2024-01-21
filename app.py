from flask import Flask
from flask_cors import CORS
from Resources.Stocks import stocks

app = Flask(__name__)
CORS(app)
app.register_blueprint(stocks)


if __name__ == "__main__":
    app.run(debug=True, port=4020)