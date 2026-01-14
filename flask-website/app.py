from flask import Flask, render_template


app = Flask(__name__) # 이제부터 이 파일을 웹사이트용 프로그램으로 사용하겠다.
# 가게 문을 열기 위해서 사업자등록을 하는 것과 비슷
# 파이썬이 이 가게 이름은 뭐니? -> 현재  oo파일입니다. 알려주는 자동 이름표

#https://naver.com/
@app.route("/")       
def home():
    return render_template("index.html")

@app.route("/about")       
def about():
    return render_template("about.html")

'''
#https://naver.com/news/section/105
@app.route("/news/section/105")       # 클라이언트가 어떤 URL로 들어왔을 때 어떤 기능을 보여줄지 연결

def home():
    return render_template("뉴스에서_특정섹션을_클릭했을때_보여질화면.html")
render_template = 특정 주소를 접속했을 때 보여질 화면은 (특정)양식을 통해서 보여질 것이다.

render   = 컴퓨터 프로그램을 이용해서 사진이나 영상 화면을 만들어내는 과정
template = 틀, 양식



'''
if __name__ == "__main__": # 만약 다른 파일에서 불러올 때 import"파일이름" 형태로 작성
    app.run(debug=True)    # 개발모드에서만 True
    # 프로그램을 실행하는데 어떤 문제가 발생하는지 개발자가 눈으로 보며 
    # 코드를 수정하기 위해서 True로 설정하지만 클라이언트에게 전달 후에는 False로 변경


'''
Flask, render_template
 Flask(__name__)
Flask() 를 사용해서 웹사이트를 만들 것인데 

__name__ : 어떤 .py에서 프로젝트 시작을 해야하고
           프로젝트 내부에 어떤 구조로 파일들이 존재하는지 확인

__name__ 을 사용하지 않고 flask로 웹사이트 구축할 수 있으나, 경로나 파일 꼬일 가능성이 있음

__name__ = 이 앱이 어디에 있냐를 알기 위해서 
           templates/ 폴더를 찾고, static/ 폴더를 찾고, 에러메세지, 로그 이름 정함
           내가 시작하는 파일 위치라는 기준점


@app.route("/")
render_template
__name__ == "__main__":

app.run(debug=True)

웹사이트가 실행하는 구조 

사람이 ▷ 화살표를 누르면 python app.py 라는 명령어가 수행
▷ = python 현재파일.py 실행하겠다와 같은 명령어를 보유하고 있다.
            ↓
__name__ == "__main__":  메일 파일이고, 현재 폴더와 파일 구조를 파악하겠다.
            ↓
        app.run(debug=True) 실행
            ↓
서버실행 -> 웹사이트 브라우저 / 개발자가 개발을 진행할 수 있는 웹사이트 요청
            ↓
        @app.route("/") 연결되어있는 함수와 html 파일 실행

@app = 우리 프로젝트에서 
.route("주소")                              클라이언트가 이 위치로 이동하면
def home():                                 메인페이지를 보여주는 기능
    return render_template("index.html")    index.html이라는 템플릿을 렌더링하겠다.  

'''