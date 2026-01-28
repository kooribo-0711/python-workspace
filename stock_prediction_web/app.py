# app.py - 주가 예측 웹서버
from flask import Flask, render_template, jsonify, request
from datetime import datetime, timedelta
import requests
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import warnings
warnings.filterwarnings('ignore')

app = Flask(__name__)

# 전역 변수
scaler = MinMaxScaler(feature_range=(0, 1))

# ============================================
# 메인 페이지
# ============================================
@app.route('/')
def index():
    """메인 페이지"""
    return render_template('index.html')


# ============================================
# 암호화폐 가격 API
# ============================================
@app.route('/api/crypto-prices')
def get_crypto_prices():
    """암호화폐 가격 가져오기"""
    try:
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {
            'ids': 'bitcoin,ethereum,ripple,cardano,solana,dogecoin',
            'vs_currencies': 'usd,krw',
            'include_24hr_change': 'true'
        }
        
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        
        return jsonify({
            'success': True,
            'data': data,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        
    except Exception as error:
        return jsonify({
            'success': False,
            'error': str(error)
        })


# ============================================
# 암호화폐 차트 API
# ============================================
@app.route('/api/crypto-chart/<coin_id>')
def get_crypto_chart(coin_id):
    """암호화폐 차트 데이터"""
    try:
        url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
        params = {
            'vs_currency': 'usd',
            'days': '7'
        }
        
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        
        prices = data.get('prices', [])
        times = []
        values = []
        
        for price_data in prices:
            timestamp = price_data[0] / 1000
            time_str = datetime.fromtimestamp(timestamp).strftime('%m/%d %H시')
            times.append(time_str)
            values.append(price_data[1])
        
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
# 주가 예측 API - 메인 기능
# ============================================
@app.route('/api/predict-stock', methods=['POST'])
def predict_stock():
    """주가 예측 수행"""
    try:
        data = request.get_json()
        stock_name = data.get('stock_name', '삼성전자')
        days_ahead = int(data.get('days_ahead', 1))
        
        # 샘플 데이터 생성 (실제로는 DB나 API에서 가져옴)
        historical_data = generate_sample_stock_data(stock_name)
        
        # 예측 수행
        prediction_result = perform_prediction(historical_data, days_ahead)
        
        return jsonify({
            'success': True,
            'stock_name': stock_name,
            'prediction': prediction_result,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        
    except Exception as error:
        return jsonify({
            'success': False,
            'error': str(error)
        })


# ============================================
# 주가 데이터 생성 함수
# ============================================
def generate_sample_stock_data(stock_name):
    """샘플 주가 데이터 생성"""
    np.random.seed(42)
    
    # 최근 3년 데이터
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365*3)
    date_range = pd.date_range(start=start_date, end=end_date, freq='D')
    
    # 주식별 기본 가격 설정
    stock_configs = {
        '삼성전자': {'base': 60000, 'trend': 20000, 'volatility': 2000},
        'SK하이닉스': {'base': 100000, 'trend': 30000, 'volatility': 3000},
        '네이버': {'base': 200000, 'trend': 50000, 'volatility': 5000},
        '카카오': {'base': 50000, 'trend': 15000, 'volatility': 2500},
    }
    
    config = stock_configs.get(stock_name, stock_configs['삼성전자'])
    
    # 가격 생성
    base_price = config['base']
    trend = np.linspace(0, config['trend'], len(date_range))
    seasonality = config['volatility'] * np.sin(np.linspace(0, 6*np.pi, len(date_range)))
    noise = np.random.normal(0, config['volatility'], len(date_range)).cumsum()
    
    prices = base_price + trend + seasonality + noise
    prices = np.maximum(prices, base_price * 0.5)
    
    df = pd.DataFrame({'Close': prices}, index=date_range)
    
    return df


# ============================================
# 예측 수행 함수
# ============================================
def perform_prediction(df, days_ahead):
    """실제 예측 로직"""
    
    # 데이터 정규화
    scaled_data = scaler.fit_transform(df[['Close']])
    
    # 간단한 이동평균 + 추세 예측
    seq_length = 60
    last_sequence = scaled_data[-seq_length:]
    
    predictions = []
    confidence_intervals = []
    
    for day in range(days_ahead):
        # 이동평균 계산
        recent = last_sequence[-20:].flatten()
        ma = np.mean(recent)
        
        # 추세 계산
        if len(recent) >= 10:
            trend = (recent[-1] - recent[-10]) / 10
        else:
            trend = 0
        
        # 예측값
        pred_scaled = ma + trend * 3
        pred_scaled = np.clip(pred_scaled, 0, 1)  # 0-1 범위 유지
        
        # 역정규화
        pred_price = scaler.inverse_transform([[pred_scaled]])[0][0]
        
        # 신뢰구간 (±5%)
        confidence = pred_price * 0.05
        
        predictions.append({
            'day': day + 1,
            'date': (datetime.now() + timedelta(days=day+1)).strftime('%Y-%m-%d'),
            'price': float(pred_price),
            'lower_bound': float(pred_price - confidence),
            'upper_bound': float(pred_price + confidence)
        })
        
        # 다음 예측을 위해 시퀀스 업데이트
        last_sequence = np.append(last_sequence[1:], [[pred_scaled]], axis=0)
    
    # 현재 가격과 비교
    current_price = float(df['Close'].iloc[-1])
    final_price = predictions[-1]['price']
    change = final_price - current_price
    change_pct = (change / current_price) * 100
    
    # 통계 정보
    recent_30_days = df['Close'].tail(30)
    stats = {
        'current_price': float(current_price),
        'predicted_price': float(final_price),
        'change': float(change),
        'change_percent': float(change_pct),
        'avg_30days': float(recent_30_days.mean()),
        'max_30days': float(recent_30_days.max()),
        'min_30days': float(recent_30_days.min()),
        'volatility': float(recent_30_days.std())
    }
    
    # 차트 데이터 (최근 30일)
    recent_data = df.tail(30)
    chart_data = {
        'dates': [d.strftime('%m/%d') for d in recent_data.index],
        'prices': [float(p) for p in recent_data['Close'].values]
    }
    
    return {
        'predictions': predictions,
        'statistics': stats,
        'chart_data': chart_data
    }


# ============================================
# 주가 히스토리 API
# ============================================
@app.route('/api/stock-history/<stock_name>')
def get_stock_history(stock_name):
    """주가 이력 데이터"""
    try:
        df = generate_sample_stock_data(stock_name)
        
        # 최근 90일 데이터
        recent_data = df.tail(90)
        
        history = {
            'dates': [d.strftime('%Y-%m-%d') for d in recent_data.index],
            'prices': [float(p) for p in recent_data['Close'].values]
        }
        
        # 통계
        stats = {
            'current': float(df['Close'].iloc[-1]),
            'high_90d': float(recent_data['Close'].max()),
            'low_90d': float(recent_data['Close'].min()),
            'avg_90d': float(recent_data['Close'].mean()),
            'change_90d': float(((df['Close'].iloc[-1] - recent_data['Close'].iloc[0]) / recent_data['Close'].iloc[0]) * 100)
        }
        
        return jsonify({
            'success': True,
            'stock_name': stock_name,
            'history': history,
            'statistics': stats,
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
    print("=" * 60)
    print("🚀 주가 예측 웹서버 시작!")
    print("=" * 60)
    print("👉 브라우저에서 http://localhost:5000 접속하세요")
    print("📊 제공 기능:")
    print("   - 암호화폐 실시간 가격")
    print("   - 주가 예측 (AI 기반)")
    print("   - 차트 분석")
    print("=" * 60)
    app.run(debug=True, host='0.0.0.0', port=5000)