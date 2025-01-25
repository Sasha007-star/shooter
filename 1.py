from pygame import *
from random import randint 
import time as pytime

mixer.init() 
mixer.music.load('space.ogg.mp3')
mixer.music.play()
fire_sound = mixer.Sound('boom.ogg.mp3')

font.init()
font1 = font.Font(None, 80)
font2 = font.Font(None, 36)
win = font1.render('YOU WIN!', True, (255, 255, 255))
lose = font1.render('YOU LOSE!', True, (180, 0, 0))

img_back = "background.png.png"
img_hero = "rocket.png"
img_bullet = "bullets.png"
img_enemy = "enemy.png"

clock = time.Clock()
FPS = 30

score = 0
goal = 50
lost = 0
max_lost = 3
life = 3
bullet_count = 10
reload_start_time = None

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(
            image.load(player_image), (size_x, size_y))
        self.speed = player_speed

        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width -80:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet(
            img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15
        )
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1

win_width = 700
win_height = 700
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))

ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)

monsters = sprite.Group()
for i in range(1,6):
    monster = Enemy(img_enemy, randint
(80, win_width - 80), -40, 80, 50, randint(1,3))
    monsters.add(monster)

bullets = sprite.Group()

finish = False
run = True

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        
        elif e.type == KEYDOWN:
            if e.key == K_SPACE and bullet_count > 0 and reload_start_time is None:
                bullet_count -= 1
                fire_sound.play()
                ship.fire() 

    if not finish:
        window.blit(background, (0, 0))

        text = font2.render("Рахунок: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))

        text_lose = font2.render("Пропущено: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        ship.update()
        monsters.update()
        bullets.update()

        ship.reset()
        monsters.draw(window)
        bullets.draw(window)

        if bullet_count == 0 and reload_start_time is None:
            reload_start_time = pytime.time()
        
        if reload_start_time:
            if pytime.time() - reload_start_time > 3:
                bullet_count = 10
                reload_start_time = None

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for collide in collides:
            score = score + 1
            monster = Enemy(
                img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5)
            )
            monsters.add(monster)
        
        if sprite.spritecollide(ship, monsters, True):
            life -= 1
            monster = Enemy(
                img_enemy, randint(80,win_width - 80), -40, 80, 50, randint(1,5)
            )
            monsters.add(monster)
        
        text_life = font1.render(str(life), 1, (255, 0, 0))
        window.blit(text_life, (650, 10))

        if life == 0 or lost >= max_lost:
            finish = True
            mixer.music.stop()
            window.blit(lose, (200, 200))
        
        if score >= goal:
            finish = True
            mixer.music.stop()
            window.blit(win, (200, 200))

    display.update() 
    clock.tick(FPS)  
    
