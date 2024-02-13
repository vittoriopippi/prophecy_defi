from flask import Flask, render_template, redirect, jsonify, abort, request
from jinja2 import TemplateNotFound
import requests
from datetime import datetime
from keys import COINMARKETCAP_KEY, MAIL_CONFIG
import yfinance as yf
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json
from email.message import EmailMessage
from google_send_email import gmail_send_message

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<path:page>')
def render_static(page):
    # Render the requested HTML file
    page = page.replace('.html', '')
    if page == 'index':
        return redirect('/')
    try:
        return render_template(f'{page}.html')
    except TemplateNotFound:
        abort(404)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404
    
@app.route('/thank-you', methods=['GET', 'POST'])
def send_email():
    if request.method == 'POST':
        message = EmailMessage()

        message.set_content(json.dumps(request.form, indent=4))

        message["To"] = MAIL_CONFIG['MAIL_USERNAME']
        message["From"] = MAIL_CONFIG['MAIL_USERNAME']
        message["Subject"] = "New form submission from prophecydefi.com"

        gmail_send_message(message)

        with open('forms.txt', 'a') as f:
            f.write(message.as_string() + '\n')

        return render_template('thank-you.html')
    else:
        return redirect('/')

@app.route('/api/general_info', methods=['GET'])
def general_info():
    url = 'https://pro-api.coinmarketcap.com/v1/global-metrics/quotes/latest'
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': COINMARKETCAP_KEY,
    }
    response = requests.get(url, headers=headers)
    data = response.json()

    total_market_cap = data['data']['quote']['USD']['total_market_cap']
    defi_market_cap = data['data']['defi_volume_24h']
    bitcoin_dominance = data['data']['btc_dominance']
    daily_volume = data['data']['quote']['USD']['total_volume_24h']

    response = {
        "total_market_cap": f"${total_market_cap / (10 ** 12):.02f}T",
        "daily_volume": f"${daily_volume / (10 ** 9):.02f}B",
        "defi_market_cap": f"${defi_market_cap / (10 ** 9):.02f}B",
        "bitcoin_dominance": f"{bitcoin_dominance:.02f}%",
    }
    return jsonify(response)

@app.route('/api/crypto/<path:symbol>', methods=['GET'])
def get_crypto(symbol):
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
        'convert': 'USD'
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': COINMARKETCAP_KEY,
    }

    response = requests.get(url, headers=headers, params=parameters)
    data = response.json()

    crypto_data = {currency['symbol']: currency for currency in data['data']}
    if symbol not in crypto_data:
        return jsonify({"price": 'N/A', "volume": 'N/A', "market_cap": 'N/A', "circulation_supply": 'N/A'}) # TODO: Return 404
    
    price = crypto_data[symbol]['quote']['USD']['price']
    volume = crypto_data[symbol]['quote']['USD']['volume_24h']
    market_cap = crypto_data[symbol]['quote']['USD']['market_cap']
    circulation_supply = crypto_data[symbol]['circulating_supply']

    response = {
        "price": f"${price:,.02f}",
        "volume": f"${volume:,.02f}",
        "market_cap": f"${market_cap:,.02f}",
        "circulation_supply": f"{circulation_supply:,.02f}",
    }
    return jsonify(response)

@app.route('/api/miner/<path:symbol>', methods=['GET'])
def get_miner(symbol):
    data = yf.Ticker(symbol)
    info = data.info

    response = {
        "previous_close": f"${info['previousClose']:.02f}",
        "volume": f"${info['volume']:,.0f}",
        "market_cap": f"${info['marketCap']:,.0f}",
        "current_price": f"${info['currentPrice']:.02f}",
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=False, port=5001)
