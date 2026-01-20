// script.js - 웹사이트 기능 파일

// ============================================
// 전역 변수 (어디서든 사용할 수 있는 변수)
// ============================================
let myChart = null;  // 차트 객체를 저장할 변수


// ============================================
// 1. 현재 시간 표시하기
// ============================================
function updateCurrentTime() {
    // 현재 시간 가져오기
    const now = new Date();
    
    // 시간을 "시:분:초" 형식으로 변환
    const timeString = now.toLocaleTimeString('ko-KR');
    
    // HTML에 표시하기
    document.getElementById('currentTime').textContent = timeString;
}

// 1초마다 시간 업데이트
setInterval(updateCurrentTime, 1000);
updateCurrentTime();  // 처음에 한번 실행


// ============================================
// 2. 암호화폐 가격 불러오기
// ============================================
async function loadPrices() {
    try {
        // 서버에 가격 데이터 요청
        const response = await fetch('/api/crypto-prices');
        const result = await response.json();
        
        // 에러 체크
        if (!result.success) {
            document.getElementById('priceList').innerHTML = '데이터를 불러올 수 없습니다';
            return;
        }
        
        // 코인 이름 한글로 바꾸기
        const coinNames = {
            'bitcoin': '비트코인',
            'ethereum': '이더리움',
            'ripple': '리플',
            'cardano': '카르다노',
            'solana': '솔라나',
            'dogecoin': '도지코인'
        };
        
        // HTML 만들기
        let html = '';
        
        // 각 코인마다 반복
        for (let coinId in result.data) {
            const coinData = result.data[coinId];
            
            // 24시간 변동률
            const change = coinData.usd_24h_change || 0;
            
            // 상승인지 하락인지 판단
            const changeClass = change >= 0 ? 'up' : 'down';
            const changeSymbol = change >= 0 ? '▲' : '▼';
            
            // HTML 조각 만들기
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
        
        // HTML에 넣기
        document.getElementById('priceList').innerHTML = html;
        
        // 업데이트 시간 표시
        document.getElementById('lastUpdate').textContent = result.timestamp;
        
    } catch (error) {
        console.error('가격 로딩 실패:', error);
        document.getElementById('priceList').innerHTML = '오류가 발생했습니다';
    }
}


// ============================================
// 3. 차트 그리기
// ============================================
async function loadChart() {
    // 선택한 코인 가져오기
    const coinId = document.getElementById('coinSelect').value;
    
    try {
        // 서버에 차트 데이터 요청
        const response = await fetch(`/api/crypto-chart/${coinId}`);
        const result = await response.json();
        
        // 에러 체크
        if (!result.success) {
            alert('차트를 불러올 수 없습니다');
            return;
        }
        
        // 이전 차트가 있으면 삭제
        if (myChart) {
            myChart.destroy();
        }
        
        // 차트 그릴 위치 찾기
        const canvas = document.getElementById('priceChart');
        const ctx = canvas.getContext('2d');
        
        // 새 차트 만들기
        myChart = new Chart(ctx, {
            type: 'line',  // 선 그래프
            data: {
                labels: result.times,  // x축 (시간)
                datasets: [{
                    label: `${coinId.toUpperCase()} 가격 (달러)`,
                    data: result.prices,  // y축 (가격)
                    borderColor: '#667eea',  // 선 색깔
                    backgroundColor: 'rgba(102, 126, 234, 0.1)',  // 배경 색깔
                    tension: 0.4,  // 선 곡선 정도
                    fill: true  // 배경 채우기
                }]
            },
            options: {
                responsive: true,  // 반응형
                maintainAspectRatio: false,  // 비율 유지 안함
                plugins: {
                    legend: {
                        display: true  // 범례 표시
                    }
                },
                scales: {
                    y: {
                        beginAtZero: false  // y축 0부터 시작 안함
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
// 4. 트렌딩 코인 불러오기
// ============================================
async function loadTrending() {
    try {
        // 서버에 트렌딩 데이터 요청
        const response = await fetch('/api/trending');
        const result = await response.json();
        
        // 에러 체크
        if (!result.success) {
            document.getElementById('trendingList').innerHTML = '데이터를 불러올 수 없습니다';
            return;
        }
        
        // HTML 만들기
        let html = '';
        
        // 각 트렌딩 코인마다 반복
        result.trending.forEach((coin, index) => {
            html += `
                <div class="trending-item">
                    <div class="trending-rank">#${index + 1}</div>
                    <img src="${coin.image}" class="trending-image">
                    <div>
                        <div class="trending-name">${coin.name}</div>
                        <div class="trending-symbol">${coin.symbol}</div>
                    </div>
                </div>
            `;
        });
        
        // HTML에 넣기
        document.getElementById('trendingList').innerHTML = html;
        
    } catch (error) {
        console.error('트렌딩 로딩 실패:', error);
        document.getElementById('trendingList').innerHTML = '오류가 발생했습니다';
    }
}


// ============================================
// 5. 전체 새로고침
// ============================================
function refreshAll() {
    console.log('전체 새로고침 시작');
    loadPrices();     // 가격 새로고침
    loadChart();      // 차트 새로고침
    loadTrending();   // 트렌딩 새로고침
}


// ============================================
// 6. 페이지 로드되면 자동 실행
// ============================================
window.onload = function() {
    console.log('페이지 로드 완료!');
    refreshAll();  // 모든 데이터 불러오기
    
    // 30초마다 가격 자동 업데이트
    setInterval(loadPrices, 30000);
};


// ============================================
// 도움말 함수들
// ============================================

// 숫자를 천단위로 콤마 찍기
function formatNumber(num) {
    return num.toLocaleString();
}

// 퍼센트 색깔 정하기
function getChangeColor(change) {
    return change >= 0 ? 'red' : 'blue';
}