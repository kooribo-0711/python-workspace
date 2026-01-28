# 📈 AI 주가 예측 대시보드

주가를 예측하고 암호화폐 실시간 정보를 제공하는 웹 대시보드입니다.

## 🚀 주요 기능

### 1. 주가 예측 (AI 기반)
- 삼성전자, SK하이닉스, 네이버, 카카오 등 주요 종목 지원
- 1일~30일 후 주가 예측
- 95% 신뢰구간 제공
- 과거 데이터와 예측 차트 시각화
- 통계 분석 (30일 평균, 최고가, 최저가, 변동성)

### 2. 암호화폐 실시간 정보
- 비트코인, 이더리움, 리플 등 주요 코인 실시간 가격
- 24시간 변동률 표시
- 최근 7일 가격 차트

## 📦 설치 방법

### 1. 필요한 패키지 설치
```bash
pip install -r requirements.txt
```

또는 개별 설치:
```bash
pip install Flask requests numpy pandas scikit-learn
```

### 2. 서버 실행
```bash
python app.py
```

### 3. 브라우저 접속
```
http://localhost:5000
```

## 📁 파일 구조

```
stock_prediction_web/
│
├── app.py                 # Flask 서버 (주가 예측 API)
├── requirements.txt       # 필요한 패키지 목록
├── README.md             # 사용 설명서
│
├── templates/
│   └── index.html        # 메인 HTML 페이지
│
└── static/
    ├── style.css         # 스타일시트
    └── script.js         # JavaScript 기능
```

## 🎯 사용 방법

### 주가 예측
1. **주가 예측** 탭 선택
2. 종목 선택 (삼성전자, SK하이닉스 등)
3. 예측 기간 선택 (1일~30일)
4. **예측 시작** 버튼 클릭
5. 결과 확인:
   - 현재 주가 vs 예측 주가
   - 예상 변동 및 변동률
   - 95% 신뢰구간
   - 차트 및 통계 분석

### 암호화폐 정보
1. **암호화폐** 탭 선택
2. 자동으로 실시간 가격 표시
3. 코인 선택 후 **차트 보기** 클릭
4. 최근 7일 가격 추이 확인

## 🔧 API 엔드포인트

### 주가 예측 API
```
POST /api/predict-stock
Body: {
  "stock_name": "삼성전자",
  "days_ahead": 7
}
```

### 주가 히스토리 API
```
GET /api/stock-history/<stock_name>
예: /api/stock-history/삼성전자
```

### 암호화폐 가격 API
```
GET /api/crypto-prices
```

### 암호화폐 차트 API
```
GET /api/crypto-chart/<coin_id>
예: /api/crypto-chart/bitcoin
```

## 📊 예측 알고리즘

- **데이터**: 최근 3년 일일 주가 데이터
- **방법**: 시계열 분석 (이동평균 + 추세 분석)
- **시퀀스 길이**: 60일
- **신뢰구간**: 95% (예측가 ± 5%)

## ⚠️ 주의사항

1. **교육 목적**: 이 시스템은 교육 및 데모 목적으로 제작되었습니다.
2. **투자 주의**: 실제 투자 결정에 사용하지 마세요.
3. **데이터 한계**: 샘플 데이터를 사용하며 실제 주가와 다릅니다.
4. **전문가 상담**: 실제 투자는 전문가와 상담하세요.

## 🛠️ 커스터마이징

### 새로운 종목 추가
`app.py`의 `stock_configs`에 추가:
```python
stock_configs = {
    '새종목': {'base': 100000, 'trend': 20000, 'volatility': 3000},
}
```

### 예측 기간 변경
`index.html`의 `daysSelect`에 옵션 추가:
```html
<option value="60">60일 후</option>
```

### 차트 스타일 변경
`style.css`에서 색상 및 디자인 수정 가능

## 📝 라이선스

이 프로젝트는 교육 목적으로 자유롭게 사용 가능합니다.

## 🤝 기여

버그 리포트 및 개선 제안을 환영합니다!

## 📞 문의

질문이나 문제가 있으면 이슈를 등록해주세요.