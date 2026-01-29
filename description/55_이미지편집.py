'''
파일 관리 + 이미지 편집 종합 프로그램
1. 파일 자동 정리
2. 폴더 용량 분석
3. 이미지 일괄 편집 (리사이징, 회전, 반전)
'''
import tkinter as tk
from tkinter import filedialog, messagebox
import os
import shutil
from PIL import Image

# ========== 파일 자동 정리 기능 ==========
def organize_files():
    """파일을 확장자별로 자동 분류하는 함수"""
    folder = filedialog.askdirectory(title="정리할 폴더 선택")
    
    if not folder:
        return
    
    categories = {
        "이미지": ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg'],
        "문서": ['.pdf', '.docx', '.txt', '.xlsx', '.pptx', '.doc'],
        "비디오": ['.mp4', '.avi', '.mkv', '.mov'],
        "음악": ['.mp3', '.wav', '.flac'],
        "압축파일": ['.zip', '.rar', '.7z'],
        "기타": []
    }
    
    count = 0
    
    try:
        for file in os.listdir(folder):
            file_path = os.path.join(folder, file)
            
            if os.path.isfile(file_path):
                ext = os.path.splitext(file)[1].lower()
                cat = next((k for k, v in categories.items() if ext in v), '기타')
                
                cat_folder = os.path.join(folder, cat)
                os.makedirs(cat_folder, exist_ok=True)
                
                dest_path = os.path.join(cat_folder, file)
                
                if os.path.exists(dest_path):
                    base, extension = os.path.splitext(file)
                    counter = 1
                    while os.path.exists(dest_path):
                        new_name = f"{base}_{counter}{extension}"
                        dest_path = os.path.join(cat_folder, new_name)
                        counter += 1
                
                shutil.move(file_path, dest_path)
                count += 1
        
        messagebox.showinfo("완료", f"✅ {count}개 파일 정리 완료!")
        
    except Exception as e:
        messagebox.showerror("오류", f"파일 정리 중 오류 발생:\n{str(e)}")


# ========== 폴더 용량 분석 기능 ==========
def analyze_folder():
    """폴더의 전체 용량과 파일 개수를 분석하는 함수"""
    folder = filedialog.askdirectory(title='분석할 폴더 선택')
    
    if not folder:
        return
    
    total_size = 0
    file_count = 0
    
    try:
        for dirpath, dirnames, filenames in os.walk(folder):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                
                if os.path.exists(fp):
                    total_size += os.path.getsize(fp)
                    file_count += 1
        
        size_mb = total_size / (1024 * 1024)
        
        if size_mb >= 1024:
            size_gb = size_mb / 1024
            size_text = f"{size_gb:.2f} GB ({size_mb:.2f} MB)"
        else:
            size_text = f"{size_mb:.2f} MB"
        
        messagebox.showinfo(
            "분석 결과",
            f"📊 폴더 용량 분석 완료\n\n"
            f"📁 폴더: {os.path.basename(folder)}\n"
            f"📄 파일 개수: {file_count:,}개\n"
            f"💾 총 용량: {size_text}"
        )
        
    except Exception as e:
        messagebox.showerror("오류", f"폴더 분석 중 오류 발생:\n{str(e)}")


# ========== 이미지 일괄 편집 기능 ==========
def open_image_editor():
    """이미지 편집 창을 여는 함수"""
    # 새 창 생성
    editor_window = tk.Toplevel()
    editor_window.title("🖼️ 이미지 일괄 편집")
    editor_window.geometry("500x550")
    editor_window.resizable(False, False)
    editor_window.configure(bg="#f0f0f0")
    
    # 선택된 이미지 파일들을 저장할 변수
    selected_files = []
    
    def select_images():
        """이미지 파일 선택"""
        files = filedialog.askopenfilenames(
            title="편집할 이미지 선택",
            filetypes=[
                ("이미지 파일", "*.jpg *.jpeg *.png *.bmp *.gif"),
                ("모든 파일", "*.*")
            ]
        )
        
        if files:
            selected_files.clear()
            selected_files.extend(files)
            file_label.config(text=f"✅ {len(selected_files)}개 이미지 선택됨")
    
    def process_images(operation):
        """이미지 처리 실행"""
        if not selected_files:
            messagebox.showwarning("경고", "먼저 이미지를 선택해주세요!")
            return
        
        # 저장 폴더 선택
        save_folder = filedialog.askdirectory(title="편집된 이미지를 저장할 폴더 선택")
        if not save_folder:
            return
        
        success_count = 0
        error_count = 0
        
        try:
            for file_path in selected_files:
                try:
                    # 이미지 열기
                    img = Image.open(file_path)
                    
                    # 파일명 추출
                    filename = os.path.basename(file_path)
                    name, ext = os.path.splitext(filename)
                    
                    # 작업 수행
                    if operation == 'resize_25':
                        new_size = (int(img.width * 0.25), int(img.height * 0.25))
                        img = img.resize(new_size, Image.Resampling.LANCZOS)
                        suffix = "_25percent"
                    
                    elif operation == 'resize_50':
                        new_size = (int(img.width * 0.5), int(img.height * 0.5))
                        img = img.resize(new_size, Image.Resampling.LANCZOS)
                        suffix = "_50percent"
                    
                    elif operation == 'rotate_90':
                        img = img.rotate(90, expand=True)
                        suffix = "_90deg"
                    
                    elif operation == 'rotate_180':
                        img = img.rotate(180, expand=True)
                        suffix = "_180deg"
                    
                    elif operation == 'rotate_270':
                        img = img.rotate(270, expand=True)
                        suffix = "_270deg"
                    
                    elif operation == 'flip_horizontal':
                        img = img.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
                        suffix = "_좌우반전"
                    
                    elif operation == 'flip_vertical':
                        img = img.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
                        suffix = "_상하반전"
                    
                    # 저장 경로 생성
                    save_path = os.path.join(save_folder, f"{name}{suffix}{ext}")
                    
                    # 같은 이름이 있으면 번호 추가
                    counter = 1
                    while os.path.exists(save_path):
                        save_path = os.path.join(save_folder, f"{name}{suffix}_{counter}{ext}")
                        counter += 1
                    
                    # 이미지 저장
                    img.save(save_path)
                    success_count += 1
                    
                except Exception as e:
                    error_count += 1
                    print(f"Error processing {filename}: {str(e)}")
            
            # 결과 메시지
            if error_count == 0:
                messagebox.showinfo(
                    "완료",
                    f"✅ 이미지 편집 완료!\n\n"
                    f"성공: {success_count}개\n"
                    f"저장 위치: {save_folder}"
                )
            else:
                messagebox.showwarning(
                    "완료",
                    f"⚠️ 이미지 편집 완료\n\n"
                    f"성공: {success_count}개\n"
                    f"실패: {error_count}개\n"
                    f"저장 위치: {save_folder}"
                )
            
        except Exception as e:
            messagebox.showerror("오류", f"이미지 처리 중 오류 발생:\n{str(e)}")
    
    # ===== 제목 =====
    title_frame = tk.Frame(editor_window, bg="#FF9800", height=70)
    title_frame.pack(fill=tk.X)
    title_frame.pack_propagate(False)
    
    tk.Label(
        title_frame,
        text="🖼️ 이미지 일괄 편집",
        font=("맑은 고딕", 16, "bold"),
        bg="#FF9800",
        fg="white"
    ).pack(expand=True)
    
    # ===== 파일 선택 영역 =====
    select_frame = tk.Frame(editor_window, bg="#f0f0f0")
    select_frame.pack(pady=20)
    
    tk.Button(
        select_frame,
        text="📂 이미지 선택",
        command=select_images,
        font=("맑은 고딕", 11, "bold"),
        bg="#2196F3",
        fg="white",
        width=20,
        height=2,
        cursor="hand2"
    ).pack()
    
    file_label = tk.Label(
        select_frame,
        text="선택된 이미지 없음",
        font=("맑은 고딕", 9),
        bg="#f0f0f0",
        fg="#666"
    )
    file_label.pack(pady=10)
    
    # ===== 크기 조절 =====
    resize_frame = tk.LabelFrame(
        editor_window,
        text="📐 크기 조절",
        font=("맑은 고딕", 10, "bold"),
        bg="#f0f0f0",
        fg="#333"
    )
    resize_frame.pack(pady=10, padx=30, fill=tk.X)
    
    btn_frame1 = tk.Frame(resize_frame, bg="#f0f0f0")
    btn_frame1.pack(pady=10)
    
    tk.Button(
        btn_frame1,
        text="25% 축소",
        command=lambda: process_images('resize_25'),
        font=("맑은 고딕", 10),
        bg="#4CAF50",
        fg="white",
        width=12,
        height=2
    ).pack(side=tk.LEFT, padx=5)
    
    tk.Button(
        btn_frame1,
        text="50% 축소",
        command=lambda: process_images('resize_50'),
        font=("맑은 고딕", 10),
        bg="#4CAF50",
        fg="white",
        width=12,
        height=2
    ).pack(side=tk.LEFT, padx=5)
    
    # ===== 회전 =====
    rotate_frame = tk.LabelFrame(
        editor_window,
        text="🔄 회전",
        font=("맑은 고딕", 10, "bold"),
        bg="#f0f0f0",
        fg="#333"
    )
    rotate_frame.pack(pady=10, padx=30, fill=tk.X)
    
    btn_frame2 = tk.Frame(rotate_frame, bg="#f0f0f0")
    btn_frame2.pack(pady=10)
    
    tk.Button(
        btn_frame2,
        text="90° 회전",
        command=lambda: process_images('rotate_90'),
        font=("맑은 고딕", 10),
        bg="#FF9800",
        fg="white",
        width=12,
        height=2
    ).pack(side=tk.LEFT, padx=5)
    
    tk.Button(
        btn_frame2,
        text="180° 회전",
        command=lambda: process_images('rotate_180'),
        font=("맑은 고딕", 10),
        bg="#FF9800",
        fg="white",
        width=12,
        height=2
    ).pack(side=tk.LEFT, padx=5)
    
    tk.Button(
        btn_frame2,
        text="270° 회전",
        command=lambda: process_images('rotate_270'),
        font=("맑은 고딕", 10),
        bg="#FF9800",
        fg="white",
        width=12,
        height=2
    ).pack(side=tk.LEFT, padx=5)
    
    # ===== 반전 =====
    flip_frame = tk.LabelFrame(
        editor_window,
        text="↔️ 반전",
        font=("맑은 고딕", 10, "bold"),
        bg="#f0f0f0",
        fg="#333"
    )
    flip_frame.pack(pady=10, padx=30, fill=tk.X)
    
    btn_frame3 = tk.Frame(flip_frame, bg="#f0f0f0")
    btn_frame3.pack(pady=10)
    
    tk.Button(
        btn_frame3,
        text="좌우 반전",
        command=lambda: process_images('flip_horizontal'),
        font=("맑은 고딕", 10),
        bg="#9C27B0",
        fg="white",
        width=12,
        height=2
    ).pack(side=tk.LEFT, padx=5)
    
    tk.Button(
        btn_frame3,
        text="상하 반전",
        command=lambda: process_images('flip_vertical'),
        font=("맑은 고딕", 10),
        bg="#9C27B0",
        fg="white",
        width=12,
        height=2
    ).pack(side=tk.LEFT, padx=5)


# ========== GUI 메인 윈도우 생성 ==========
def create_main_window():
    """메인 윈도우를 생성하고 설정하는 함수"""
    root = tk.Tk()
    root.title("파일 관리 종합 프로그램")
    root.geometry("450x550")
    root.resizable(False, False)
    
    root.configure(bg="#f0f0f0")
    
    # ===== 제목 =====
    title_frame = tk.Frame(root, bg="#2196F3", height=80)
    title_frame.pack(fill=tk.X)
    title_frame.pack_propagate(False)
    
    tk.Label(
        title_frame,
        text="🗂️ 파일 관리 종합 프로그램",
        font=("맑은 고딕", 18, "bold"),
        bg="#2196F3",
        fg="white"
    ).pack(expand=True)
    
    # ===== 설명 =====
    tk.Label(
        root,
        text="원하는 기능을 선택하세요",
        font=("맑은 고딕", 11),
        bg="#f0f0f0",
        fg="#555"
    ).pack(pady=20)
    
    # ===== 버튼 프레임 =====
    button_frame = tk.Frame(root, bg="#f0f0f0")
    button_frame.pack(pady=10)
    
    # 버튼 1: 파일 자동 정리
    btn1 = tk.Button(
        button_frame,
        text="📁 파일 자동 정리",
        command=organize_files,
        font=("맑은 고딕", 12, "bold"),
        bg="#4CAF50",
        fg="white",
        width=25,
        height=2,
        relief=tk.RAISED,
        bd=3,
        cursor="hand2"
    )
    btn1.pack(pady=8)
    
    tk.Label(
        button_frame,
        text="폴더 안의 파일을 확장자별로 자동 분류합니다",
        font=("맑은 고딕", 9),
        bg="#f0f0f0",
        fg="#666"
    ).pack()
    
    # 구분선 1
    separator1 = tk.Frame(button_frame, height=2, bg="#ddd")
    separator1.pack(fill=tk.X, pady=12, padx=30)
    
    # 버튼 2: 폴더 용량 분석
    btn2 = tk.Button(
        button_frame,
        text="📊 폴더 용량 분석",
        command=analyze_folder,
        font=("맑은 고딕", 12, "bold"),
        bg="#673AB7",
        fg="white",
        width=25,
        height=2,
        relief=tk.RAISED,
        bd=3,
        cursor="hand2"
    )
    btn2.pack(pady=8)
    
    tk.Label(
        button_frame,
        text="폴더의 전체 용량과 파일 개수를 분석합니다",
        font=("맑은 고딕", 9),
        bg="#f0f0f0",
        fg="#666"
    ).pack()
    
    # 구분선 2
    separator2 = tk.Frame(button_frame, height=2, bg="#ddd")
    separator2.pack(fill=tk.X, pady=12, padx=30)
    
    # 버튼 3: 이미지 일괄 편집 (NEW!)
    btn3 = tk.Button(
        button_frame,
        text="🖼️ 이미지 일괄 편집",
        command=open_image_editor,
        font=("맑은 고딕", 12, "bold"),
        bg="#FF9800",
        fg="white",
        width=25,
        height=2,
        relief=tk.RAISED,
        bd=3,
        cursor="hand2"
    )
    btn3.pack(pady=8)
    
    tk.Label(
        button_frame,
        text="이미지 크기 조절, 회전, 반전을 일괄 처리합니다",
        font=("맑은 고딕", 9),
        bg="#f0f0f0",
        fg="#666"
    ).pack()
    
    # ===== 하단 정보 =====
    footer_frame = tk.Frame(root, bg="#f0f0f0")
    footer_frame.pack(side=tk.BOTTOM, pady=10)
    
    tk.Label(
        footer_frame,
        text="v2.0 | 파일 관리 + 이미지 편집 도우미",
        font=("맑은 고딕", 8),
        bg="#f0f0f0",
        fg="#999"
    ).pack()
    
    root.mainloop()


# ========== 프로그램 실행 ==========
if __name__ == "__main__":
    create_main_window()