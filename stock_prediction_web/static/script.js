// script.js - 주가 예측 대시보드 기능

// ============================================
// 전역 변수
// ============================================
let stockChart = null;
let cryptoChart = null;

// ============================================
// 시간 업데이트
// ============================================
function updateCurrentTime() {
    const now = new Date();
    const timeString = now.toLocaleTimeString('ko-KR');
    document.getElementById('currentTime').textContent = timeString;
}

setInterval(updateCurrentTime, 1000);
updateCurrentTime();

// ============================================
// 탭 전환
// ============================================
function switchTab(tab) {
    // 탭 버튼 활성화
    const buttons = document.querySelectorAll('.tab-button');
    buttons.forEach(btn => btn.classList.remove('active'));
    event.target.classList.add('active');
    
    // 탭 컨텐츠 전환
    const contents = document.querySelectorAll('.tab-content');
    contents.forEach(content => content.classList.remove('active'));
    
    if (tab === 'stock') {
        document.getElementById('stockTab').classList.add('active');
    } else {
        document.getElementById('cryptoTab').classList.add('active');
        loadCryptoPrices();
    }
}

// ============================================
// 주가 예측 실행
// ============================================
async function predictStock() {
    const stockName = document.getElementById('stockSelect').value;
    const daysAhead = document.getElementById('daysSelect').value;
    
    // 로딩 표시
    const resultCard = document.getElementById('predictionResult');
    resultCard.style.display = 'block';
    document.getElementById('currentPrice').textContent = '예측 중...';
    document.getElementById('predictedPrice').textContent = '예측 중...';
    
    try {
        // 서버에 예측 요청
        const response = await fetch('/api/predict-stock', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                stock_name: stockName,
                days_ahead: daysAhead
            })
        });
        
        const result = await response.json();
        
        if (!result.success) {
            alert('예측 실패: ' + result.error);
            return;
        }
        
        // 결과 표시
        displayPredictionResult(result.prediction);
        
        // 업데이트 시간
        document.getElementById('lastUpdate').textContent = result.timestamp;
        
    } catch (error) {
        console.error('예측 오류:', error);
        alert('예측 중 오류가 발생했습니다.');
    }
}

// ============================================
// 예측 결과 표시
// ============================================
function displayPredictionResult(prediction) {
    const stats = prediction.statistics;
    const predictions = prediction.predictions;
    const lastPrediction = predictions[predictions.length - 1];
    
    // 요약 정보 표시
    document.getElementById('currentPrice').textContent = 
        formatPrice(stats.current_price);
    
    document.getElementById('predictedPrice').textContent = 
        formatPrice(stats.predicted_price);
    
    // 변동 표시
    const changeElement = document.getElementById('priceChange');
    const changeValue = stats.change;
    const changeClass = changeValue >= 0 ? 'up' : 'down';
    const changeSymbol = changeValue >= 0 ? '▲' : '▼';
    
    changeElement.textContent = `${changeSymbol} ${formatPrice(Math.abs(changeValue))}`;
    changeElement.className = `summary-value ${changeClass}`;
    
    // 변동률 표시
    const percentElement = document.getElementById('changePercent');
    percentElement.textContent = `${stats.change_percent >= 0 ? '+' : ''}${stats.change_percent.toFixed(2)}%`;
    percentElement.className = `summary-value ${changeClass}`;
    
    // 신뢰 구간 표시
    document.getElementById('confidenceRange').textContent = 
        `${formatPrice(lastPrediction.lower_bound)} ~ ${formatPrice(lastPrediction.upper_bound)}`;
    
    // 차트 그리기
    drawStockChart(prediction);
    
    // 통계 표시
    displayStatistics(stats);
}

// ============================================
// 주가 차트 그리기
// ============================================
function drawStockChart(prediction) {
    const chartData = prediction.chart_data;
    const predictions = prediction.predictions;
    
    // 과거 데이터 + 예측 데이터 결합
    const allDates = [...chartData.dates];
    const allPrices = [...chartData.prices];
    
    // 예측 데이터 추가
    predictions.forEach(pred => {
        allDates.push(pred.date.substring(5)); // MM-DD 형식
        allPrices.push(null); // 과거 데이터는 null
    });
    
    // 예측선용 데이터 (마지막 실제 가격부터 시작)
    const predictionPrices = new Array(chartData.prices.length - 1).fill(null);
    predictionPrices.push(chartData.prices[chartData.prices.length - 1]);
    predictions.forEach(pred => {
        predictionPrices.push(pred.price);
    });
    
    // 신뢰 구간
    const upperBound = new Array(chartData.prices.length).fill(null);
    const lowerBound = new Array(chartData.prices.length).fill(null);
    predictions.forEach(pred => {
        upperBound.push(pred.upper_bound);
        lowerBound.push(pred.lower_bound);
    });
    
    // 이전 차트 삭제
    if (stockChart) {
        stockChart.destroy();
    }
    
    // 차트 생성
    const canvas = document.getElementById('stockChart');
    const ctx = canvas.getContext('2d');
    
    stockChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: allDates,
            datasets: [
                {
                    label: '실제 주가',
                    data: allPrices,
                    borderColor: '#667eea',
                    backgroundColor: 'rgba(102, 126, 234, 0.1)',
                    borderWidth: 3,
                    tension: 0.4,
                    fill: true,
                    pointRadius: 3,
                    pointHoverRadius: 6
                },
                {
                    label: '예측 주가',
                    data: predictionPrices,
                    borderColor: '#f56565',
                    backgroundColor: 'rgba(245, 101, 101, 0.1)',
                    borderWidth: 3,
                    borderDash: [5, 5],
                    tension: 0.4,
                    fill: false,
                    pointRadius: 4,
                    pointHoverRadius: 7
                },
                {
                    label: '신뢰구간 상한',
                    data: upperBound,
                    borderColor: 'rgba(245, 101, 101, 0.3)',
                    backgroundColor: 'rgba(245, 101, 101, 0.05)',
                    borderWidth: 1,
                    borderDash: [2, 2],
                    tension: 0.4,
                    fill: '+1',
                    pointRadius: 0
                },
                {
                    label: '신뢰구간 하한',
                    data: lowerBound,
                    borderColor: 'rgba(245, 101, 101, 0.3)',
                    backgroundColor: 'rgba(245, 101, 101, 0.05)',
                    borderWidth: 1,
                    borderDash: [2, 2],
                    tension: 0.4,
                    fill: false,
                    pointRadius: 0
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: {
                intersect: false,
                mode: 'index'
            },
            plugins: {
                legend: {
                    display: true,
                    position: 'top',
                    labels: {
                        font: {
                            size: 12
                        },
                        filter: function(item, chart) {
                            // 신뢰구간 범례는 하나만 표시
                            return !item.text.includes('하한');
                        }
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    padding: 12,
                    titleFont: {
                        size: 14
                    },
                    bodyFont: {
                        size: 13
                    },
                    callbacks: {
                        label: function(context) {
                            let label = context.dataset.label || '';
                            if (label) {
                                label += ': ';
                            }
                            if (context.parsed.y !== null) {
                                label += formatPrice(context.parsed.y);
                            }
                            return label;
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: false,
                    ticks: {
                        callback: function(value) {
                            return formatPrice(value);
                        }
                    }
                }
            }
        }
    });
}

// ============================================
// 통계 정보 표시
// ============================================
function displayStatistics(stats) {
    const statsHtml = `
        <div class="stat-item">
            <div class="stat-label">30일 평균</div>
            <div class="stat-value">${formatPrice(stats.avg_30days)}</div>
        </div>
        <div class="stat-item">
            <div class="stat-label">30일 최고가</div>
            <div class="stat-value">${formatPrice(stats.max_30days)}</div>
        </div>
        <div class="stat-item">
            <div class="stat-label">30일 최저가</div>
            <div class="stat-value">${formatPrice(stats.min_30days)}</div>
        </div>
        <div class="stat-item">
            <div class="stat-label">변동성 (표준편차)</div>
            <div class="stat-value">${formatPrice(stats.volatility)}</div>
        </div>
    `;
    
    document.getElementById('stockStats').innerHTML = statsHtml;
}

// ============================================
// 암호화폐 가격 불러오기
// ============================================
async function loadCryptoPrices() {
    try {
        const response = await fetch('/api/crypto-prices');
        const result = await response.json();
        
        if (!result.success) {
            document.getElementById('priceList').innerHTML = '데이터를 불러올 수 없습니다';
            return;
        }
        
        const coinNames = {
            'bitcoin': '비트코인',
            'ethereum': '이더리움',
            'ripple': '리플',
            'cardano': '카르다노',
            'solana': '솔라나',
            'dogecoin': '도지코인'
        };
        
        let html = '';
        
        for (let coinId in result.data) {
            const coinData = result.data[coinId];
            const change = coinData.usd_24h_change || 0;
            const changeClass = change >= 0 ? 'up' : 'down';
            const changeSymbol = change >= 0 ? '▲' : '▼';
            
            html += `
                <div class="price-item">
                    <div>
                        <div class="coin-name">${coinNames[coinId]}</div>
                        <div class="coin-symbol">${coinId.toUpperCase()}</div>
                    </div>
                    <div style="text-align: right;">
                        <div class="price">$${coinData.usd.toLocaleString()}</div>
                        <div class="change ${changeClass}">
                            ${changeSymbol} ${Math.abs(change).toFixed(2)}%
                        </div>
                    </div>
                </div>
            `;
        }
        
        document.getElementById('priceList').innerHTML = html;
        document.getElementById('lastUpdate').textContent = result.timestamp;
        
    } catch (error) {
        console.error('가격 로딩 실패:', error);
        document.getElementById('priceList').innerHTML = '오류가 발생했습니다';
    }
}

// ============================================
// 암호화폐 차트 불러오기
// ============================================
async function loadCryptoChart() {
    const coinId = document.getElementById('coinSelect').value;
    
    try {
        const response = await fetch(`/api/crypto-chart/${coinId}`);
        const result = await response.json();
        
        if (!result.success) {
            alert('차트를 불러올 수 없습니다');
            return;
        }
        
        if (cryptoChart) {
            cryptoChart.destroy();
        }
        
        const canvas = document.getElementById('cryptoChart');
        const ctx = canvas.getContext('2d');
        
        cryptoChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: result.times,
                datasets: [{
                    label: `${coinId.toUpperCase()} 가격 (달러)`,
                    data: result.prices,
                    borderColor: '#667eea',
                    backgroundColor: 'rgba(102, 126, 234, 0.1)',
                    tension: 0.4,
                    fill: true,
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: true
                    }
                },
                scales: {
                    y: {
                        beginAtZero: false
                    }
                }
            }
        });
        
    } catch (error) {
        console.error('차트 로딩 실패:', error);
        alert('차트를 불러오는 중 오류가 발생했습니다');
    }
}

// ============================================
// 암호화폐 새로고침
// ============================================
function refreshCrypto() {
    console.log('암호화폐 데이터 새로고침');
    loadCryptoPrices();
    loadCryptoChart();
}

// ============================================
// 가격 포맷 함수
// ============================================
function formatPrice(price) {
    return Math.round(price).toLocaleString() + '원';
}

// ============================================
// 페이지 로드
// ============================================
window.onload = function() {
    console.log('페이지 로드 완료!');
    console.log('주가 예측 대시보드 준비 완료');
    
    // 암호화폐 데이터는 탭 전환시에만 로드
};