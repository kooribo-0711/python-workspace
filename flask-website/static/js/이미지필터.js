// 이미지필터.js

// 1. 파일 선택했을 때
document.getElementById('파일선택').addEventListener('change', function(e) {
    // 선택한 파일 가져오기
    const file = e.target.files[0];
    
    if (file) {
        // 파일 이름 보여주기
        document.getElementById('fileName').textContent = '선택된 파일: ' + file.name;
        
        // 원본 이미지 미리보기 만들기
        const reader = new FileReader();
        reader.onload = function(event) {
            // 이미지 태그 만들기
            const img = document.createElement('img');
            img.src = event.target.result;
            
            // 미리보기 영역에 이미지 넣기
            const originalPreview = document.getElementById('originalPreview');
            originalPreview.innerHTML = '';
            originalPreview.appendChild(img);
        };
        reader.readAsDataURL(file);
        
        // 필터 적용 버튼 활성화
        document.getElementById('applyBtn').disabled = false;
    }
});

// 2. 폼 제출했을 때 (필터 적용 버튼 눌렀을 때)
document.getElementById('filterForm').addEventListener('submit', async function(e) {
    e.preventDefault(); // 페이지 새로고침 방지
    
    // 폼 데이터 가져오기
    const formData = new FormData(this);
    const applyBtn = document.getElementById('applyBtn');
    
    // 버튼 비활성화하고 "처리중..." 표시
    applyBtn.disabled = true;
    applyBtn.textContent = '처리 중...';
    
    try {
        // 서버에 데이터 보내기
        const response = await fetch('/apply-filter', {
            method: 'POST',
            body: formData
        });
        
        // 성공하면
        if (response.ok) {
            // 결과 이미지 받기
            const blob = await response.blob();
            const imageUrl = URL.createObjectURL(blob);
            
            // 결과 이미지 보여주기
            const img = document.createElement('img');
            img.src = imageUrl;
            
            const resultPreview = document.getElementById('resultPreview');
            resultPreview.innerHTML = '';
            resultPreview.appendChild(img);
            
            // 다운로드 링크 만들기
            const downloadLink = document.createElement('a');
            downloadLink.href = imageUrl;
            downloadLink.download = 'filtered_image.png';
            downloadLink.textContent = '다운로드';
            downloadLink.style.display = 'block';
            downloadLink.style.marginTop = '10px';
            downloadLink.style.color = '#667eea';
            resultPreview.appendChild(downloadLink);
            
        } else {
            alert('오류가 발생했습니다.');
        }
    } catch (error) {
        alert('에러: ' + error.message);
    }
    
    // 버튼 다시 활성화
    applyBtn.disabled = false;
    applyBtn.textContent = '필터 적용하기';
});