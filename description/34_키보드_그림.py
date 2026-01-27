import turtle

# 화면 설정
screen = turtle.Screen()
screen.title("방향키로 거북이를 조종하세요.")
screen.bgcolor("black") #배경색상 검정

# 거북이 설정
t = turtle.Turtle() # 거북이를 t라는 명칭으로 소환
t.shape("turtle")   # 거북이가 진짜 거북이모양으로 변경
t.speed(0)          # 이동속도 조절 (0이 가장 빠름)
t.color("cyan")
t.pensize(3)        # 거북이 크기  1   --> 50 숫자가 커질수록 점점 커지며, 숫자값 조절하며 확인


# 이동 함수 정의
def move_up():
    t.setheading(90)  # 거북이가 위쪽으로    90도 바라보기
    t.forward(20)     # 20만큼 앞으로 가기

def move_down():
    t.setheading(270)  # 거북이가 아래쪽으로 270도 바라보기
    t.forward(20)     # 20만큼 앞으로 가기

def move_left():
    t.setheading(180) # 거북이가 왼쪽으로   180도 바라보기
    t.forward(20)     # 20만큼 앞으로 가기

def move_right():
    t.setheading(0)   # 거북이가 오른쪽으로   0도 바라보기
    t.forward(20)     # 20만큼 앞으로 가기

def clear_screen():
    t.clear()         # 그린 선 지우기

# 키보드 이벤트 연결
screen.listen()       # 사용자 입력을 기다림
screen.onkeypress(move_up, "Up")       #키보드 키에서 ↑
screen.onkeypress(move_down, "Down")   #키보드 키에서 ↓
screen.onkeypress(move_left, "Left")   #키보드 키에서 ←
screen.onkeypress(move_right, "Right") #키보드 키에서 →

# 창이 닫히지 않게 설정

screen.mainloop()