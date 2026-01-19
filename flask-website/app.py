from flask import Flask, render_template, request, send_file  # 웹과 컴퓨터가 이미지를 주고받기 위해 필요한 기능
from PIL import Image, ImageEnhance  #사진 관련 설정
import os                            # 현재 나의 컴퓨터에서 특정 위치에 파일을 불러오거나 현재위치확인 저장 사용 
from io import BytesIO               # 사진 입출력


app = Flask(__name__) # 이제부터 이 파일을 웹사이트용 프로그램으로 사용하겠다.
# 가게 문을 열기 위해서 사업자등록을 하는 것과 비슷
# 파이썬이 이 가게 이름은 뭐니? -> 현재  oo파일입니다. 알려주는 자동 이름표

#https://naver.com/
'''
@app.route("/")    #클라이언트가 어떤 url로 들어왔는지   
def home():
    return render_template("index.html")
'''

@app.route("/")       
def home():
    # DB 데이터 저장소에서 넘어온 데이터
    # DB와 Python이 연결되어있다면 DB에서 저장된 데이터를 웹사이트에 보여줄 수 있다
    # name이랑 이름은 DB에서 가져온 데이터를 잠시 담아 보관하기 위한 데이터 공간
    # age라는 이름 또한 마찬가지
    # 나중에 DB와 연결하여 데이터를 성공적으로 가져오게 되면
    # 홍길동 자리에는 DB에 저장되어있는 이름이 들어갈 것
    # 현재는 DB와 연결한 상태가 아니기 때문에 홍길동 20 이라는 임의 데이터를 이용하여
    # HTML에 DB에서 가져온 데이터를 어떻게 전달하는지 확인하는 로직 작성
    name="홍길동"
    age=20
    return render_template("index.html", abc=name, xyz=age)
'''

()들을 보여줄거야(어떤 파일에서, 어떤 데이터들을 전달받을 수 있도록 설정하겠어! 설정은 무제한 갯수 가능)
abc, xyz = html에서 db에서 가져온 데이터를 어떻게 보여줄 것인지 데이터를 담아가는 공간의 명칭

보통은 html에서 사용하는 변수명칭과 python에서 html로 전달하는 변수명칭을 동일하게 작성
회사에서 데이터를 가져오는 변수명칭이 최소 10개 이상
 render_template("index.html", abc=name, xyz=age)
    <h1>{{abc}}님 환영합니다</h1>
      <h2>나이 : {{xyz}}세</h2>

'''

def 목록기능():
    과일들=['참외','바나나','포도','사과']
    for 과일하나씩담는변수공간 in 과일들:
        print("현재 과일 : ", 과일하나씩담는변수공간)
'''
@app.route("/about")       
def about():
    # 방문자 명단
    visitors=["김철수","이영희","박민수","최지원","정다은"]
    # 방문자 정보
    visitor_info = [

           {"name":"김철수", "count":15}, # 0번째 목록에 존재하는 방문자
           {"name":"이영희", "count":23}, # 1번째 목록에 존재하는 방문자
           {"name":"박민수", "count":8},  # 2번째 목록에 존재하는 방문자
           {"name":"최지원", "count":31}, # 3번째 목록에 존재하는 방문자
           {"name":"정다은", "count":12}, # 4번째 목록에 존재하는 방문자

           ]
    return render_template("about.html", visitors=visitors, visitor_info=visitor_info)
'''
@app.route("/about")       
def about():
    # 방문자 명단
    visitors=["김철수","이영희","박민수","최지원","정다은"]
    # 방문자 정보
    visitor_info = [

           {"name":"김철수", "count":15}, # 0번째 목록에 존재하는 방문자
           {"name":"이영희", "count":23}, # 1번째 목록에 존재하는 방문자
           {"name":"박민수", "count":8},  # 2번째 목록에 존재하는 방문자
           {"name":"최지원", "count":31}, # 3번째 목록에 존재하는 방문자
           {"name":"정다은", "count":12}, # 4번째 목록에 존재하는 방문자

           ]
    외부링크리스트= [
        {"주소":"https://www.google.com", "도메인이름":"구글"},
        {"주소":"https://www.naver.com", "도메인이름":"네이버"},
        {"주소":"https://www.daum.com", "도메인이름":"다음"},
    ]
    return render_template("about.html", visitors=visitors, visitor_info=visitor_info, 외부링크리스트=외부링크리스트)

# /image 라는 주소로 들어갔을 때 image-filter.html 화면이 보일 수 있도록 설정
# image-filter h1 태그로 이미지 꾸미기라는 재목 보이기

@app.route("/image")
def image():
    return render_template("image-filter.html")


업로드_폴더 = 'static/uploads'
if not os.path.exists(업로드_폴더):
    os.makedirs(업로드_폴더)

@app.route("/apply-filter", methods=["post"])
def apply_filter():
    try:
        if 'image' not in request.files:
            return '이미지를 선택해 주세요'

        file = request.files['image']
        if file.filename == "":
            return '파일이 선택되지 않았습니다'

        # 웹사이트에서 클라이언트가 지정한 필터값을 가져오기
        대비 = float(request.form.get('contrast',1.0))
        채도 = float(request.form.get('saturation',1.0))
        밝기 = float(request.form.get('brightness',1.0))

        # 클라이언트가 업로드한 이미지에 필터를 적용하기 위해 이미지 열기
        img = Image.open(file.stream)

        #필터 적용
        대비조절 = ImageEnhance.Contrast(img).enhance(대비)
        채도조절 = ImageEnhance.Color(대비조절).enhance(채도)
        밝기조절 = ImageEnhance.Brightness(채도조절).enhance(밝기)

        # 메모리에 이미지 저장
        img_io = BytesIO()
        밝기조절.save(img_io, "PNG")
        img_io.seek(0)

        return send_file(img_io, mimetype="image/png")
    
    except Exception as e:
        return f"에러 발생"


'''
아래 존재하는 주석을 참고하여
외부링크리스트 완성하고, 완성된 데이터를 about.html에서 보여주기
{% for 외부링크 in 외부링크리스트 %}
     <a href='{{외부링크주소}}'>{{외부링크.도메인이름}}</a>
     {% endfor %}
<!--
    <a href='https://www.google.com/'>구글로 이동하기</a>
    <a href="https://www.naver.com/">네이버로 이동하기</a>
    <a href="https://www.daum.net/">다음으로 이동하기</a>
           -->
'''
'''
    과일1번 = '참외'
    과일2번 = '사과'
    과일3번 = '포도'
    과일4번 = '바나나'
    과일들 = ['참외','바나나','포도','사과']
    return render_template("about.html", fruits=과일들)
'''
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