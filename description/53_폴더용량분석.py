'''

이미지 리사이즈 프로그램
텍스트 파일 병합기
중복 파일 찾기
파일명에 날짜 추가
파일 백업 프로그램
파일명 일괄 변경
폴더 용량 분석
클립보트 저장
엑셀 병합
pdf 합치기
워터마크 추가 등.... 다양한 exe 파일 생성 가능

'''

#폴더 용량 분석
import tkinter as tk
from tkinter import filedialog, messagebox
import os

def analyze_folder():
    # 사용자에게 폴더를 선택하는 창을 띄우고, 선택한 폴더 경로를 folder 변수에 저장
    folder = filedialog.askdirectory(title='폴더선택')
    if not folder: return

    # 전체 파일 용량 합계 (초기값 0)
    total_size = 0
    # 파일 갯수 세기 (초기값 0)
    file_count = 0

    # 선택한 폴더의 모든 하위 폴더까지 탐색
    # dirpath = 현재 폴더 경로
    # dirnames = 현재 폴더 안의 폴더들
    # filenames = 현재 폴더 안의 파일들
    for dirpath, dirnames, filenames in os.walk(folder):
        # 각 파일 이름을 하나씩 가져옴
        for f in filenames:
            # 폴더 경로 + 파일 이름을 합쳐서 전체 경로 만들기
            fp = os.path.join(dirpath, f)
            # 하나씩 하나씩 알아낸 파일의 크기를 total_size에 더하기
            total_size += os.path.getsize(fp) # += 기존에 존재하는 소수/정수에 더하기 누적
            # 파일 갯수 누적하여 갯수 증가
            file_count +=1
    # 바이트를 메가바이트(MB)로 변환
    size_mb = total_size / (1024 * 1024)

    # 알림창 띄우기
    # f"..."        : f-string (변수를 문자에 넣기)
    # {size_mb:.2f} : 소수점 2자리 까지 표시
    messagebox.showinfo('분석 결과', 
                        f'파일 개수 : {file_count}개\n'
                        f'총 용량 : {size_mb:.2f} MB')
root = tk.Tk()
root.title('폴더 용량 분석')
root.geometry('300x150')
tk.Label(root, 
         text='폴더 용량 분석', 
         font=('맑은 고딕', 14, 'bold')).pack(pady=20)
tk.Button(root,
          text='분석 시작',
          command=analyze_folder,  # 버튼을 클릭하면 해당 기능 실행
          bg='#673AB7',
          fg='white',
          width=20,
          height=2).pack(pady=10)

root.mainloop()

