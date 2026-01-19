# app.py
from flask import Flask, render_template

app = Flask(__name__)

# 메인 페이지
@app.route("/")
def home():
    return render_template("index.html")

# 연구 분야
@app.route("/research")
def research():
    researches = [
        {"title": "유전체 분석", "desc": "차세대 염기서열 분석 및 유전체 데이터 처리", "icon": "🧬"},
        {"title": "단백질 구조 예측", "desc": "AI 기반 단백질 3D 구조 분석", "icon": "🔬"},
        {"title": "질병 바이오마커", "desc": "빅데이터 기반 질병 진단 마커 발굴", "icon": "💊"}
    ]
    return render_template("research.html", researches=researches)

# 현재 연구원
@app.route("/members")
def members():
    professor = {"name": "김바이오", "position": "교수", "email": "kimbio@university.ac.kr"}
    
    students = [
        {"name": "이유전", "position": "박사과정", "research": "유전체 분석"},
        {"name": "박단백", "position": "석사과정", "research": "단백질 구조"},
        {"name": "최데이터", "position": "학부연구생", "research": "바이오마커"}
    ]
    return render_template("members.html", professor=professor, students=students)

# 졸업생 (새로 추가)
@app.route("/alumni")
def alumni():
    alumni_list = [
        {"name": "정유진", "year": "2023", "position": "박사", "current": "서울대병원 연구원"},
        {"name": "강민수", "year": "2023", "position": "석사", "current": "삼성바이오로직스"},
        {"name": "홍지연", "year": "2022", "position": "박사", "current": "KAIST 교수"},
        {"name": "윤서준", "year": "2022", "position": "석사", "current": "마크로젠"},
        {"name": "임수빈", "year": "2021", "position": "박사", "current": "미국 NIH 연구원"}
    ]
    return render_template("alumni.html", alumni_list=alumni_list)

# 논문/성과
@app.route("/publications")
def publications():
    papers = [
        {"title": "딥러닝 기반 유전자 발현 패턴 분석", "year": "2024", "journal": "Nature Biotechnology"},
        {"title": "암 진단 바이오마커 발굴 연구", "year": "2023", "journal": "Cell"},
        {"title": "단백질 상호작용 네트워크 분석", "year": "2023", "journal": "Bioinformatics"}
    ]
    return render_template("publications.html", papers=papers)

# 연락처
@app.route("/contact")
def contact():
    info = {
        "lab": "바이오인포매틱스 연구실",
        "address": "서울시 관악구 관악로 1 서울대학교",
        "phone": "02-880-1234",
        "email": "bioinfo@snu.ac.kr",
        "map_lat": "37.4601",  # 서울대 좌표
        "map_lng": "126.9520"
    }
    return render_template("contact.html", info=info)

if __name__ == "__main__":
    app.run(debug=True)