'''

UI = User interface : 유저가 보는 화면
CLI = 오직 키보드만 가능한 창
GUI = 키보드와 마우스를 이용해서 화면을 클릭하거나 이동할 수 있는 화면

pip install pygame
파이썬으로 2D 게임 만들기 위해 설계된 라이브러리
소리 출력, 키보드/마우스 입력 처리, 충돌 감지 등 게임 제작에 필요한 도구 보유

무한 루프 : 게임은 멈춰있는 프로그램이 아니라, 초당 수십번씩 화면을 그리는 무한 루프
게임의 경우 - 메모리, 트래픽 관리 신경써야 함

Event  : 유저가 키보드를 누르거나, 움직이거나, 마우스를 클릭하는 것과 같이 가만히 있는 화면에서 행동을 하는 것을 말함.
         사람이 하는 모든 행동 = 이벤트(예상치못한행위)
Update : 캐릭터의 위치를 계산하고, 적과 부딫혔는지 확인
Draw   : 계산된 위치에 맞게 캐릭터와 배경을 화면에 새로 그림.
Tick   : 게임이 너무 빠르거나 느리지 않게 초당 프레임 고정
Surface: 그림을 그리는 도화지
Rect   : 위치와 크기를 다루는 사각형 / 충돌 체크의 핵심
Event  : 사용자의 입력 감지
Mixer  : 효과음이나 배경 제생
Font   : 화면에 글자 표시
'''

import pygame, random, sys

# 1. 초기화
pygame.init()

# 2. 화면 설정
screen_width = 480
screen_height = 640
#         게임    화면   크기세팅     가로크기      세로크기
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption(" 유성 피하기 게임")

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
# 언어에서 대문자를 사용한다는 것은 변수 이름을 사용한다는 것은 개발자간의 표기

# 초당 보여줄 화면 프레임 설정
# FPS 설정
clock = pygame.time.Clock() # 프레임 수 제어를 위한 시계 객체 생성

# 2. 게임 설정
# 플레이어 (사각형으로 대체)
player_size = 40                                         # 플레이어 사각형 크기
player_x = screen_width / 2 - player_size / 2            # 가로 중앙에 오도록 배치 계산
player_y = screen_height - player_size -10               # 바닥 근처에 위치
player_speed = 7                                         # 한 프레임 당 이동 할 속도

# 적 (유성)
enemy_size = 30                                          # 유성 크기
enemy_x = random.randint(0, screen_width - enemy_size)   # 0부터 창 너비 사이 랜덤 위치
enemy_y = 0                                              # 화면 맨 위에서 시작. (맨 위 y 좌표 = 0)
enemy_speed = 5                                          # 유성이 떨어지는 기본 속도

# 점수
score = 0
font = pygame.font.SysFont("mlagungothic" , 30)          # 맑은 고딕 폰트, 크기 30

# 게임 루프

running = True                                           # 게임이 실행 중인지 확인하는 변수  
while running : # while은 True에서 False가 될 때 까지 횟수 제한 없이 평생 반봇
    dt = clock.tick(60) # FPS를 60으로 고정               # 1초에 60번 루프를 돌아 움직임을 자연스럽게 설정 

    # 이벤트 처리
    for event in pygame.event.get():                     # 현재 발생한 모든 이벤트를 가져오기
        if event.type == pygame.QUIT: # 이벤트 타입이 .QUIT() 종료와 같다면 (창 닫기 버튼을 눌렀다면)
            running = False # 게임 플레이를 멈추겠다.
    # 키 입력 처리
    keys = pygame.key.get_pressed() # 클라이언트가 입력하는 키보드 데이터 모두 가져오기
    if keys[pygame.K_LEFT] and player_x > 0:                              # 왼쪽 화살표 키 + 화면 안이라면
        player_x -= player_speed                                          # 왼쪽으로 이동 (0,0) -> 왼쪽 위로 이동 (-숫자, -숫자)    
    if keys[pygame.K_RIGHT] and player_x < screen_width - player_size:    # 오른쪽 화살표 키 + 화면 안이라면
        player_x += player_speed                                          # 오른쪽으로 이동 (0,0) -> 오른쪽 아래로 이동 (+숫자, +숫자)  
    
    # 위치 업데이트
    enemy_y += enemy_speed                                                # 유성의 위치 추락

    # 유성이 떨어지면 다시 생성
    if enemy_y > screen_height:                                           # 유성의 y 위치가 화면 위치보다 더 아래에 있다면 유성 떨어짐 
        enemy_y = 0                                                       # 다시 유성 화면 꼭대기로 이동시킴
        enemy_x = random.randint(0, screen_width - enemy_size)            # 새로운 x 좌표 위치   
        score += 1                                                        # 피하면 스코어 증가
        enemy_speed += 0.2 # 피하고 점수가 높을 수록 난이도 상승

    # 4. 충돌 처리
    player_rect = pygame.Rect(player_x, player_y, player_size, player_size)  # 컴퓨터는 ■ 네모의 틀들로 이루어진 구성
    enemy_rect = pygame.Rect(enemy_x, enemy_y, enemy_size, enemy_size)       # 유성도 사각형 틀 처리를 하여  
    
    if player_rect.colliderect(enemy_rect):                                  # 사각형끼리 맞닿은 것이 사실이라면
        print(f"충돌 최종점수 : {score}")                                     # 충돌로 보고 게임 종료
        running = False
    
    # 5. 화면 그리기
    screen.fill(BLACK) # 배경 색상 채우기

    # 플레이어와 적 그리기
    pygame.draw.rect(screen, YELLOW, player_rect)                            # 화면에서 노란색상으로 유저를 그리기
    pygame.draw.circle(screen, RED, (enemy_x + enemy_size//2, enemy_y + enemy_size//2), enemy_size//2)  
    #  '/'  : 나누기 = 소수점까지 정확히 계산
    # '//'  : 몫만 건지는 나누기 = 소수점 이하는 버리고 정수만 반환
    #  '%'  : 나머지 = 나누고 남은 값을 반환
    # 컴퓨터의 네모난 픽셀은 정수여야만 한다. 컴퓨터 모니터의 화면 입자는 1.5칸이라는 소수 개념이 없음
    # 1번 칸 아니면 2번 칸 형태로 위치나 크기 계산
    # 유성의 크기가 30이라면 그 절반인 15를 더해줘야 유성의 정 중앙 좌표를 그릴 수 있다.
    # //2 를 쓰면 항상 정수로 결과가 떨어지기 때문에 그림을 오류 없이 정확한 위치에 그림
    # 게임== 수학
    # Yellow라는 자리에 image 넣으면 이미지 형태로 게임을 즐길 수 있다.

    # 점수 표기
    score_text = font.render(f"Score : {score}", True, WHITE)
    screen.blit(score_text, (10,10))
    pygame.display.update() # 화면 업데이트

pygame.quit() #게임 종료하고
sys.exit() # 화면 나가기