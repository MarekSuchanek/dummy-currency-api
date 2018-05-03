import datetime
import flask
import hashlib
import random

app = flask.Flask(__name__)

api_token = "token " + hashlib.sha1(b'MI-AFP').hexdigest()
base_rates = {
    "USD": {"EUR": 0.834900163, "CZK": 21.2743325,
            "GBP": 0.735600257, "CNY": 6.36780438},
    "EUR": {"USD": 1.197748, "CZK": 25.4812892,
            "GBP": 0.881063737, "CNY": 7.62702496},
    "CZK": {"USD": 0.047005, "EUR": 0.0392444821,
            "GBP": 0.0345768901, "CNY": 0.299318645},
    "GBP": {"USD": 1.359434, "EUR": 1.13499167,
            "CZK": 28.921051, "CNY": 8.65660978},
    "CNY": {"USD": 0.15704, "EUR": 0.131112722,
            "CZK": 3.34092118, "GBP": 0.115518664},
}


@app.route('/')
def index():
    return flask.render_template('index.html')


@app.route('/currencies')
def currencies():
    print(flask.request.headers.get('Authorization', ''))
    print(api_token)
    if flask.request.headers.get('Authorization', '') != api_token:
        flask.abort(401)
    return flask.jsonify(
        [
            {"code": "USD", "name": "U.S. Dollar", "sign": "$"},
            {"code": "EUR", "name": "Euro", "sign": "€"},
            {"code": "CZK", "name": "Czech Koruna", "sign": "Kč"},
            {"code": "GBP", "name": "Pound Sterling", "sign": "£"},
            {"code": "CNY", "name": "Chinese Yuan Renminbi", "sign": "¥"}
        ]
    )


def recalc_rates(currency):
    return {
        c: v + v * ((random.random()-0.5))/50
        for c, v in base_rates[currency].items()
    }


@app.route('/exchange-rates/<currency>')
def rates(currency):
    if not flask.request.headers.get('Authorization', '') == api_token:
        flask.abort(401)
    if currency not in base_rates:
        flask.abort(400)
    return flask.jsonify(
        {
            "base": currency,
            "timestamp": str(datetime.datetime.utcnow()),
            "rates": recalc_rates(currency)
        }
    )
