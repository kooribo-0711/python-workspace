# app.py - Flask 서버 메인 파일
# 이 파일은 웹서버를 실행하고 암호화폐 데이터를 가져오는 역할을 합니다

from flask import Flask, render_template, jsonify
from datetime import datetime
import requests

# Flask 앱 만들기
app = Flask(__name__)

# ============================================
# 메인 페이지
# ============================================
@app.route('/')
def index():
    """메인 페이지를 보여줍니다"""
    return render_template('index.html')


# ============================================
# API 1: 암호화폐 가격 가져오기
# ============================================
@app.route('/api/crypto-prices')
def get_crypto_prices():
    """
    주요 암호화폐의 현재 가격을 가져옵니다
    CoinGecko API 사용 (무료, API 키 불필요)
    """
    try:
        # CoinGecko API 주소
        url = "https://api.coingecko.com/api/v3/simple/price"
        
        # 어떤 코인의 가격을 가져올지 설정
        params = {
            'ids': 'bitcoin,ethereum,ripple,cardano,solana,dogecoin',
            'vs_currencies': 'usd,krw',  # 달러, 원화
            'include_24hr_change': 'true'  # 24시간 변동률 포함
        }
        
        # API에 요청 보내기
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        
        # 결과 반환
        return jsonify({
            'success': True,
            'data': data,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        
    except Exception as error:
        # 에러가 발생하면 에러 메시지 반환
        return jsonify({
            'success': False,
            'error': str(error)
        })


# ============================================
# API 2: 차트 데이터 가져오기
# coingecko 사이트에서 수집한 차트 데이터를 제공
# coingecko 사이트에 가입되어있어야 하고 id를 보유한 사람만 차트 데이터를 가져올 수 있다.
# 외부 사이트에서 제공하는 API는 언제 유료로 바뀌거나 서비스가 종료될 지 모르기 때문에
# API 주소의 코드를 전체적으로 확보할 수 있을 때 사용하는 것이 가장 안전 (오픈소스)
# ============================================
@app.route('/api/crypto-chart/<coin_id>')
def get_crypto_chart(coin_id):
    """
    특정 코인의 차트 데이터를 가져옵니다 (최근 7일)
    예: /api/crypto-chart/bitcoin
    """
    try:
        # CoinGecko 차트 API
        url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
        
        # 최근 7일 데이터 요청
        params = {
            'vs_currency': 'usd',
            'days': '7'
        }
        
        # API 호출
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        
        # 데이터 정리하기
        prices = data.get('prices', [])
        
        # 시간과 가격을 분리
        times = []
        values = []
        
        for price_data in prices:
            # 타임스탬프를 읽기 쉬운 시간으로 변환
            timestamp = price_data[0] / 1000  # 밀리초를 초로 변환
            time_str = datetime.fromtimestamp(timestamp).strftime('%m/%d %H시')
            times.append(time_str)
            
            # 가격 값
            values.append(price_data[1])
        
        # 결과 반환
        return jsonify({
            'success': True,
            'coin': coin_id,
            'times': times,
            'prices': values,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        
    except Exception as error:
        return jsonify({
            'success': False,
            'error': str(error)
        })


# ============================================
# API 3: 트렌딩 코인 (인기 급상승)
# ============================================
@app.route('/api/trending')
def get_trending():
    """지금 가장 인기있는 코인들을 가져옵니다"""
    try:
        url = "https://api.coingecko.com/api/v3/search/trending"
        response = requests.get(url, timeout=10)
        data = response.json()
        
        # 트렌딩 코인 리스트 만들기
        trending_list = []
        
        for coin in data.get('coins', [])[:10]:  # 상위 10개만
            coin_info = coin.get('item', {})
            trending_list.append({
                'name': coin_info.get('name'),
                'symbol': coin_info.get('symbol'),
                'rank': coin_info.get('market_cap_rank'),
                'image': coin_info.get('thumb')
            })
        
        return jsonify({
            'success': True,
            'trending': trending_list,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        
    except Exception as error:
        return jsonify({
            'success': False,
            'error': str(error)
        })


# ============================================
# 서버 실행
# ============================================
if __name__ == '__main__':
    print("🚀 서버 시작!")
    print("👉 브라우저에서 http://localhost:5000 접속하세요")
    app.run(debug=True, host='0.0.0.0', port=5000)