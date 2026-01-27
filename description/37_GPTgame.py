
import pygame
import random
import sys
import os

# 1. 초기화
pygame.init()

# 2. 화면 설정
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 640
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("키보드 조작 게임")

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 100, 255)
YELLOW = (255, 255, 0)

# FPS 설정
clock = pygame.time.Clock()
FPS = 60

# 폰트 설정
font = pygame.font.SysFont("malgungothic", 30)
font_large = pygame.font.SysFont("malgungothic", 50)

# 이미지 로드 함수 (이미지가 없으면 기본 도형으로 대체)
def load_image_or_placeholder(image_path, width, height, color):
    """이미지를 로드하거나, 없으면 색상 사각형 반환"""
    if os.path.exists(image_path):
        try:
            image = pygame.image.load(image_path)
            image = pygame.transform.scale(image, (width, height))
            return image, True  # 이미지 로드 성공
        except:
            pass
    
    # 이미지 로드 실패 시 기본 도형 생성
    surface = pygame.Surface((width, height))
    surface.fill(color)
    return surface, False  # 기본 도형 사용


# ==================== 게임 오브젝트 클래스 ====================

class Player:
    """플레이어 캐릭터"""
    def __init__(self):
        self.width = 60
        self.height = 60
        self.x = SCREEN_WIDTH // 2 - self.width // 2
        self.y = SCREEN_HEIGHT - self.height - 20
        self.speed = 7
        self.lives = 3  # 생명
        
        # ★★★ 여기에 플레이어 이미지 경로 입력 ★★★
        self.image, self.has_image = load_image_or_placeholder(
            "player.png",  # 이 파일명의 이미지를 같은 폴더에 넣으세요
            self.width,
            self.height,
            BLUE
        )
        
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
    
    def move(self, keys):
        """키보드 입력으로 이동"""
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x < SCREEN_WIDTH - self.width:
            self.x += self.speed
        if keys[pygame.K_UP] and self.y > 0:
            self.y -= self.speed
        if keys[pygame.K_DOWN] and self.y < SCREEN_HEIGHT - self.height:
            self.y += self.speed
        
        # Rect 위치 업데이트
        self.rect.x = self.x
        self.rect.y = self.y
    
    def draw(self, screen):
        """플레이어 그리기"""
        screen.blit(self.image, (self.x, self.y))
        
        # 이미지가 없을 때는 테두리 추가
        if not self.has_image:
            pygame.draw.rect(screen, WHITE, self.rect, 2)


class Enemy:
    """적 캐릭터"""
    def __init__(self):
        self.width = 50
        self.height = 50
        self.x = random.randint(0, SCREEN_WIDTH - self.width)
        self.y = -self.height
        self.speed = 4
        
        # ★★★ 여기에 적 이미지 경로 입력 ★★★
        self.image, self.has_image = load_image_or_placeholder(
            "enemy.png",  # 이 파일명의 이미지를 같은 폴더에 넣으세요
            self.width,
            self.height,
            RED
        )
        
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
    
    def update(self):
        """적 이동 (위에서 아래로)"""
        self.y += self.speed
        self.rect.y = self.y
    
    def draw(self, screen):
        """적 그리기"""
        screen.blit(self.image, (self.x, self.y))
        
        # 이미지가 없을 때는 원형으로 표시
        if not self.has_image:
            pygame.draw.circle(screen, RED, 
                             (self.x + self.width//2, self.y + self.height//2), 
                             self.width//2)
    
    def is_off_screen(self):
        """화면 밖으로 나갔는지 확인"""
        return self.y > SCREEN_HEIGHT


class Item:
    """수집 아이템"""
    def __init__(self):
        self.width = 35
        self.height = 35
        self.x = random.randint(0, SCREEN_WIDTH - self.width)
        self.y = -self.height
        self.speed = 3
        
        # ★★★ 여기에 아이템 이미지 경로 입력 ★★★
        self.image, self.has_image = load_image_or_placeholder(
            "item.png",  # 이 파일명의 이미지를 같은 폴더에 넣으세요
            self.width,
            self.height,
            YELLOW
        )
        
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
    
    def update(self):
        """아이템 이동"""
        self.y += self.speed
        self.rect.y = self.y
    
    def draw(self, screen):
        """아이템 그리기"""
        screen.blit(self.image, (self.x, self.y))
        
        # 이미지가 없을 때는 별 모양으로 표시
        if not self.has_image:
            center = (self.x + self.width//2, self.y + self.height//2)
            pygame.draw.circle(screen, YELLOW, center, self.width//2)
            pygame.draw.circle(screen, WHITE, center, self.width//2, 2)
    
    def is_off_screen(self):
        """화면 밖으로 나갔는지 확인"""
        return self.y > SCREEN_HEIGHT


# ==================== 게임 변수 초기화 ====================

# 배경 이미지 로드 (선택사항)
background, has_background = load_image_or_placeholder(
    "background.png",  # 배경 이미지 파일명
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    BLACK
)

# 게임 오브젝트
player = Player()
enemies = []
items = []

# 게임 상태
score = 0
game_over = False
enemy_spawn_timer = 0
item_spawn_timer = 0


# ==================== 게임 루프 ====================

running = True
while running:
    dt = clock.tick(FPS)
    
    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # 게임 오버 후 재시작
        if event.type == pygame.KEYDOWN:
            if game_over and event.key == pygame.K_SPACE:
                # 게임 재시작
                player = Player()
                enemies = []
                items = []
                score = 0
                game_over = False
                enemy_spawn_timer = 0
                item_spawn_timer = 0
    
    if not game_over:
        # 키 입력 처리
        keys = pygame.key.get_pressed()
        player.move(keys)
        
        # 적 생성 (일정 시간마다)
        enemy_spawn_timer += dt
        if enemy_spawn_timer > 1000:  # 1초마다
            enemies.append(Enemy())
            enemy_spawn_timer = 0
        
        # 아이템 생성 (일정 시간마다)
        item_spawn_timer += dt
        if item_spawn_timer > 2500:  # 2.5초마다
            items.append(Item())
            item_spawn_timer = 0
        
        # 적 업데이트
        for enemy in enemies[:]:
            enemy.update()
            
            # 화면 밖으로 나간 적 제거
            if enemy.is_off_screen():
                enemies.remove(enemy)
                score += 10  # 피한 점수
            
            # 충돌 체크
            elif player.rect.colliderect(enemy.rect):
                enemies.remove(enemy)
                player.lives -= 1
                if player.lives <= 0:
                    game_over = True
        
        # 아이템 업데이트
        for item in items[:]:
            item.update()
            
            # 화면 밖으로 나간 아이템 제거
            if item.is_off_screen():
                items.remove(item)
            
            # 아이템 획득
            elif player.rect.colliderect(item.rect):
                items.remove(item)
                score += 50  # 아이템 점수
                # 추가 효과: 생명 회복
                if player.lives < 3:
                    player.lives += 1
    
    # ==================== 화면 그리기 ====================
    
    # 배경 그리기
    screen.blit(background, (0, 0))
    
    if not game_over:
        # 게임 오브젝트 그리기
        player.draw(screen)
        
        for enemy in enemies:
            enemy.draw(screen)
        
        for item in items:
            item.draw(screen)
        
        # UI 표시
        score_text = font.render(f"점수: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        
        lives_text = font.render(f"생명: {'♥' * player.lives}", True, RED)
        screen.blit(lives_text, (10, 50))
        
        # 조작 안내
        guide_text = font.render("방향키: 이동", True, WHITE)
        screen.blit(guide_text, (SCREEN_WIDTH - 150, 10))
    
    else:
        # 게임 오버 화면
        game_over_text = font_large.render("게임 오버!", True, RED)
        final_score_text = font.render(f"최종 점수: {score}", True, WHITE)
        restart_text = font.render("SPACE: 재시작", True, YELLOW)
        
        screen.blit(game_over_text, 
                   (SCREEN_WIDTH//2 - game_over_text.get_width()//2, 
                    SCREEN_HEIGHT//2 - 100))
        screen.blit(final_score_text, 
                   (SCREEN_WIDTH//2 - final_score_text.get_width()//2, 
                    SCREEN_HEIGHT//2))
        screen.blit(restart_text, 
                   (SCREEN_WIDTH//2 - restart_text.get_width()//2, 
                    SCREEN_HEIGHT//2 + 50))
    
    pygame.display.update()

# 게임 종료
pygame.quit()
sys.exit()