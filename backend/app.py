from flask import Flask, jsonify, request
from flask_cors import CORS
from pytrends.request import TrendReq
from datetime import datetime, timedelta
import os

app = Flask(__name__)
CORS(app)

# 캐시 저장소 (배포 환경에서는 Redis 등 사용 권장)
cache = {}
CACHE_DURATION = timedelta(minutes=10)  # 10분간 캐시 유지

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

        # 캐시 키 생성
        cache_key = f"trends_{timeframe_days}"

        # 캐시 확인
        if cache_key in cache:
            cached_data, cached_time = cache[cache_key]
            if datetime.now() - cached_time < CACHE_DURATION:
                print(f"Returning cached data for timeframe {timeframe_days}")
                cached_data['cached'] = True
                return jsonify(cached_data)

        # 캐시가 없거나 만료된 경우 새로운 데이터 가져오기
        print(f"Fetching fresh data for timeframe {timeframe_days}")
        kr_trends = get_trending_searches('KR', timeframe_days)
        jp_trends = get_trending_searches('JP', timeframe_days)

        # Ensure both lists have the same length
        max_length = max(len(kr_trends), len(jp_trends))
        kr_trends.extend([''] * (max_length - len(kr_trends)))
        jp_trends.extend([''] * (max_length - len(jp_trends)))

        data = {
            'korea': kr_trends,
            'japan': jp_trends,
            'timeframe': timeframe_days,
            'timestamp': datetime.now().isoformat(),
            'cached': False
        }

        # 캐시에 저장
        cache[cache_key] = (data, datetime.now())

        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
