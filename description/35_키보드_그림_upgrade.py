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
t.pensize(3)        # 거북이 크기  1   --> 50 숫자가 커질수록 점점 커지며, 숫자값 조절하며 확

# 상태 표시용 터틀 (글자 전용)

writer = turtle.Turtle()
writer.hideturtle()
writer.penup()
writer.color("white")
writer.goto(-280, 260)

def update_status():
    # 현재 거북이의 위치를 화면 상단에 갱신
    writer.clear()
    # 폰트설정(폰트이름, 크기, 스타일)
    font_style = ("Arial",12,"bold") # 폰트스타일 , 폰트 크기, 굵기
    writer.write(f"거북이 위치:{t.pos()} | 색상 : {t.pencolor()}", font=font_style)

def check_bound():
    # 거북이가 화면 밖으로 나가지 않게 체크
    if abs(t.cor()) > 290 or abs(t.ycor()) >290 :   # 절대값(abs) : -200 = 200 정수 200으로 처리하는 형태
        t.undo() #마지막 이동 취소

# 이동 함수 정의
# 거북이의 위치가 바뀔 때 마다 거북이 위치 확인을 하기 위해서 작성
# 거북이 위치를 변경할 때 마다 update_status()를 호출하여 매번 위치 새로 고쳐서 다시 작성하도록 만드는 것
def move_up():
    t.setheading(90)  # 거북이가 위쪽으로    90도 바라보기
    t.forward(20)     # 20만큼 앞으로 가기
    update_status()

def move_down():
    t.setheading(270)  # 거북이가 아래쪽으로 270도 바라보기
    t.forward(20)     # 20만큼 앞으로 가기
    update_status()

def move_left():
    t.setheading(180) # 거북이가 왼쪽으로   180도 바라보기
    t.forward(20)     # 20만큼 앞으로 가기
    update_status()

def move_right():
    t.setheading(0)   # 거북이가 오른쪽으로   0도 바라보기
    t.forward(20)     # 20만큼 앞으로 가기
    update_status()

def clear_screen():
    t.clear()         # 그린 선 지우기
    update_status()

import random
def change_color():
    # 무작위로 거북이 색상 변경
    colors=['#FF5733', '#33FF57', '#3357FF', '#FFFF33', "cyan", "white"]
    t.color(random.choice(colors))

# 키보드에서 c를 눌렀다 뗐을 때 거북이 색상 변경되게 하기
# .onkeypress(기능, "키보드명칭") 할당한 키보드를 눌렀다 뗐을 때 해당하는 기능 구현

# 키보드 이벤트 연결
screen.listen()       # 사용자 입력을 기다림
screen.onkeypress(move_up, "Up")       #키보드 키에서 ↑
screen.onkeypress(move_down, "Down")   #키보드 키에서 ↓
screen.onkeypress(move_left, "Left")   #키보드 키에서 ←
screen.onkeypress(move_right, "Right") #키보드 키에서 →
screen.onkeypress(clear_screen, "space") # 키보드 space 모두 지우기
screen.onkeypress(change_color, "c")

# 창이 닫히지 않게 설정
# 초기 상태 표기
update_status()
screen.mainloop()