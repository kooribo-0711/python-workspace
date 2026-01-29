'''
자동화 + 폴더 용량 분석 하는 기능을
하나의 exe 파일로 생성하기
'''
import tkinter as tk
from tkinter import filedialog, messagebox
import os
import shutil

# ===============================
# 기능 1️⃣ 폴더 용량 분석
# ===============================
def analyze_folder():
    folder = filedialog.askdirectory(title='폴더 선택')
    if not folder:
        return

    total_size = 0
    file_count = 0

    for dirpath, dirnames, filenames in os.walk(folder):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            try:
                total_size += os.path.getsize(fp)
                file_count += 1
            except:
                pass

    size_mb = total_size / (1024 * 1024)

    messagebox.showinfo(
        '분석 결과',
        f'파일 개수 : {file_count}개\n총 용량 : {size_mb:.2f} MB'
    )


# ===============================
# 기능 2️⃣ 파일 자동 정리
# ===============================
def organize_files():
    folder = filedialog.askdirectory(title="정리할 폴더 선택")
    if not folder:
        return

    categories = {
        "이미지": ['.jpg', '.png'],
        "문서": ['.pdf', '.docx', '.txt'],
        "기타": []
    }

    count = 0

    for file in os.listdir(folder):
        file_path = os.path.join(folder, file)

        if os.path.isfile(file_path):
            ext = os.path.splitext(file)[1].lower()
            category = next(
                (k for k, v in categories.items() if ext in v),
                "기타"
            )

            target_dir = os.path.join(folder, category)
            os.makedirs(target_dir, exist_ok=True)

            shutil.move(file_path, os.path.join(target_dir, file))
            count += 1

    messagebox.showinfo("완료", f"{count}개 파일 정리 완료")


# ===============================
# 메인 GUI (런처)
# ===============================
root = tk.Tk()
root.title("종합 유틸리티 프로그램")
root.geometry("400x300")
root.resizable(False, False)

tk.Label(
    root,
    text="📦 종합 프로그램",
    font=("맑은 고딕", 18, "bold")
).pack(pady=25)

tk.Button(
    root,
    text="📁 폴더 용량 분석",
    command=analyze_folder,
    width=25,
    height=2,
    bg="#673AB7",
    fg="white"
).pack(pady=10)

tk.Button(
    root,
    text="🗂 파일 자동 정리",
    command=organize_files,
    width=25,
    height=2,
    bg="#4CAF50",
    fg="white"
).pack(pady=10)

tk.Label(
    root,
    text="원하는 기능을 선택하세요",
    font=("맑은 고딕", 9)
).pack(pady=15)

root.mainloop()
