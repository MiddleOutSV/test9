from flask import Flask, jsonify, request
from flask_cors import CORS
import yfinance as yf
from datetime import datetime, timedelta
import pycountry

app = Flask(__name__)
CORS(app)

# Map exchanges to country codes for flags
EXCHANGE_TO_COUNTRY = {
    'NMS': 'US',  # NASDAQ
    'NYQ': 'US',  # NYSE
    'PCX': 'US',  # NYSE Arca
    'BTS': 'US',  # BATS
    'NGM': 'US',  # NASDAQ Global Market
    'NCM': 'US',  # NASDAQ Capital Market
    'ASE': 'US',  # NYSE American
    'LSE': 'GB',  # London Stock Exchange
    'TSE': 'JP',  # Tokyo Stock Exchange
    'HKG': 'HK',  # Hong Kong
    'FRA': 'DE',  # Frankfurt
    'EPA': 'FR',  # Euronext Paris
    'TOR': 'CA',  # Toronto
}

def get_period_for_timeframe(timeframe):
    """Convert timeframe to yfinance period"""
    periods = {
        '1W': '1mo',  # Need more data to calculate 1 week
        '1M': '3mo',
        '6M': '1y',
        '1Y': '2y'
    }
    return periods.get(timeframe, '1y')

def calculate_returns(ticker_symbol, timeframe):
    """Calculate returns for the given timeframe"""
    try:
        ticker = yf.Ticker(ticker_symbol)
        period = get_period_for_timeframe(timeframe)
        hist = ticker.history(period=period)

        if hist.empty:
            return None

        # Determine how many days back to look
        days_map = {
            '1W': 7,
            '1M': 30,
            '6M': 180,
            '1Y': 365
        }
        days_back = days_map.get(timeframe, 365)

        # Get the price from days_back ago and current price
        if len(hist) < days_back:
            days_back = len(hist) - 1

        if days_back < 1:
            return None

        start_price = hist['Close'].iloc[-days_back]
        current_price = hist['Close'].iloc[-1]

        returns = ((current_price - start_price) / start_price) * 100
        return round(returns, 2)
    except Exception as e:
        print(f"Error calculating returns for {ticker_symbol}: {e}")
        return None

@app.route('/api/ticker/<symbol>', methods=['GET'])
def get_ticker_info(symbol):
    """Get ticker information including company name, exchange, and returns"""
    try:
        timeframe = request.args.get('timeframe', '1M')
        ticker = yf.Ticker(symbol.upper())
        info = ticker.info

        # Get basic info
        company_name = info.get('longName') or info.get('shortName') or symbol
        exchange = info.get('exchange', 'NMS')
        country_code = EXCHANGE_TO_COUNTRY.get(exchange, 'US')

        # Calculate returns
        returns = calculate_returns(symbol.upper(), timeframe)

        return jsonify({
            'symbol': symbol.upper(),
            'name': company_name,
            'exchange': exchange,
            'countryCode': country_code,
            'returns': returns,
            'timeframe': timeframe
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
