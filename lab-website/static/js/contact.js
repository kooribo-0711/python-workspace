// contact.js - 지도 기능

// 주소 클릭했을 때
document.getElementById('addressBtn').addEventListener('click', function() {
    const mapContainer = document.getElementById('mapContainer');
    mapContainer.classList.add('show');
    
    // 지도 표시
    showMap();
    
    // 지도로 스크롤
    mapContainer.scrollIntoView({ behavior: 'smooth' });
});

// 닫기 버튼
document.getElementById('closeMap').addEventListener('click', function() {
    const mapContainer = document.getElementById('mapContainer');
    mapContainer.classList.remove('show');
});

// 간단한 지도 표시 함수
function showMap() {
    const mapDiv = document.getElementById('map');
    
    // 이미 지도가 있으면 리턴
    if (mapDiv.innerHTML !== '') {
        return;
    }
    
    // 간단한 지도 HTML 만들기
    mapDiv.innerHTML = `
        <div class="simple-map">
            <div class="map-icon">🗺️</div>
            <div class="map-address">${mapData.address}</div>
            <div class="map-info">
                <p>위도: ${mapData.lat}</p>
                <p>경도: ${mapData.lng}</p>
            </div>
            <a href="https://map.naver.com/p/search/${encodeURIComponent(mapData.address)}" 
               target="_blank">
               네이버 지도에서 보기
            </a>
            <a href="https://www.google.com/maps/search/?api=1&query=${mapData.lat},${mapData.lng}" 
               target="_blank"
               style="margin-left: 10px;">
               구글 지도에서 보기
            </a>
        </div>
    `;
}