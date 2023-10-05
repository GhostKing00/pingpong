import pygame
from pygame import mixer

# Создай окно игры
window = pygame.display.set_mode((700, 500))

# Задай фон сцены
pygame.display.set_caption("Ping pong")
background = pygame.transform.scale(pygame.image.load("background.jpg"), (700, 500))
win_or_lose = None  # Изменил значение по умолчанию на None

class GameSprite(pygame.sprite.Sprite):
    def __init__(self, images):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(images), (30, 30))
        self.rect = self.image.get_rect()

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Ball(GameSprite):
    def __init__(self, images, enemy_x, enemy_y, enemy_speed):
        super().__init__(images)
        self.speed_x = enemy_speed
        self.speed_y = enemy_speed
        self.rect.x = enemy_x
        self.rect.y = enemy_y

    def move_enemy(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        
        if self.rect.y <= 0 or self.rect.y >= 470:
            self.speed_y *= -1
    
    def win_lose(self):
        global win_or_lose  # Добавлено глобальное объявление переменной win_or_lose
        if self.rect.x < 28:
            win_or_lose = True
        elif self.rect.x > 678:
            win_or_lose = False

class Player(pygame.sprite.Sprite):
    def __init__(self, images, player_x, player_y, player_speed):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(images), (10, 90))
        self.rect = self.image.get_rect()
        self.speed = player_speed
        self.rect.x = player_x
        self.rect.y = player_y

    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

# Создай спрайты и размести их на сцене
sprite1 = Player("sprite.png", 50, 0, 10)
sprite2 = Player("sprite.png", 640, 0, 10)
Enemy = Ball("ball.png", 401, 250, 3)

# Обработай событие «клик по кнопке "Закрыть окно"»
pygame.font.init()
font = pygame.font.Font(None, 70)
win = font.render('2nd Player lose!!', True, (255, 215, 0))
lose = font.render('1st Player lose!!', True, (255, 0, 0))

# Музыка
mixer.init()
mixer.music.load("music.mp3")
mixer.music.play()
kick = mixer.Sound("kick.mp3")

game = True
fps = pygame.time.Clock()

while game:
    window.blit(background, (0, 0))
    sprite1.draw()
    sprite2.draw()
    key_pressed = pygame.key.get_pressed()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False

    Enemy.reset()
    Enemy.move_enemy()
    
    if pygame.sprite.spritecollide(sprite1, [Enemy], False) or pygame.sprite.spritecollide(sprite2, [Enemy], False):
        Enemy.speed_x *= -1

    if key_pressed[pygame.K_UP] and sprite1.rect.y > 0:
        sprite1.rect.y -= 10
    if key_pressed[pygame.K_DOWN] and sprite1.rect.y < 410:
        sprite1.rect.y += 10

    if key_pressed[pygame.K_w] and sprite2.rect.y > 0:
        sprite2.rect.y -= 10
    if key_pressed[pygame.K_s] and sprite2.rect.y < 410:
        sprite2.rect.y += 10
    
    Enemy.win_lose()
    
    if win_or_lose is not None:
        if win_or_lose:
            window.blit(lose, (0, 0))
        else:
            window.blit(win, (0, 0))
        
    
    pygame.display.update()
    fps.tick(60)