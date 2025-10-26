from flask import Flask, jsonify, request
from flask_cors import CORS
from pytrends.request import TrendReq
from datetime import datetime, timedelta
import os

app = Flask(__name__)
CORS(app)

def get_trending_searches(country_code, timeframe_days):
    """
    Get trending searches for a specific country
    country_code: 'KR' for Korea, 'JP' for Japan
    timeframe_days: 1, 7, or 30 for daily, weekly, or monthly trends
    """
    try:
        pytrends = TrendReq(hl='ko' if country_code == 'KR' else 'ja', tz=540)

        # Get trending searches for the country
        trending_searches_df = pytrends.trending_searches(pn=country_code.lower())

        # Convert to list and limit to top 20
        trends = trending_searches_df[0].head(20).tolist()

        return trends
    except Exception as e:
        print(f"Error getting trends for {country_code}: {e}")
        return []

@app.route('/api/trends', methods=['GET'])
def get_trends():
    """Get trending searches for Korea and Japan"""
    try:
        # Get timeframe parameter (default to 1 day)
        timeframe = request.args.get('timeframe', '1')
        timeframe_days = int(timeframe)

        # Validate timeframe
        if timeframe_days not in [1, 7, 30]:
            return jsonify({'error': 'Invalid timeframe. Must be 1, 7, or 30'}), 400

        # Get trends for Korea and Japan
        kr_trends = get_trending_searches('KR', timeframe_days)
        jp_trends = get_trending_searches('JP', timeframe_days)

        # Ensure both lists have the same length
        max_length = max(len(kr_trends), len(jp_trends))
        kr_trends.extend([''] * (max_length - len(kr_trends)))
        jp_trends.extend([''] * (max_length - len(jp_trends)))

        return jsonify({
            'korea': kr_trends,
            'japan': jp_trends,
            'timeframe': timeframe_days,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
