import pygame as pg
import random
import os
import shelve
from random import randint
from os import path

game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'models')
snd_folder = os.path.join(game_folder, 'sounds')

W = 480
H = 600
FPS = 60
poweruptime = 3000
newscore = 0
lvl = 1

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (255, 100, 255)
YELLOW = (255, 255, 0)

# Игра и окно
pg.init()
pg.mixer.init()
screen = pg.display.set_mode((W, H))
pg.display.set_caption("Shoot’em up")
clock = pg.time.Clock()

fontname = pg.font.match_font('verdana')
            
def text(surf, text, meaning, size, x, y):
    font = pg.font.Font(fontname, size)
    text = font.render(text+meaning, True, WHITE)
    place = text.get_rect()
    place.midtop = (x, y)
    surf.blit(text, place)

def draw_hp_bar(surf, x, y, hp):
    if hp < 0:
        hp = 0
    hp_l = 100
    hp_h = 10
    fill = (hp / 100) * hp_l
    hp_bar = pg.Rect(x, y, hp_l, hp_h)
    hp_rect = pg.Rect(x, y, fill, hp_h)
    pg.draw.rect(surf, GREEN, hp_rect)
    pg.draw.rect(surf, WHITE, hp_bar, 2)

def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)

def create_new_mob():
        m = Mob()
        all_sprites.add(m)
        mobs.add(m)

def pause():
    paused = True
    while paused:
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONDOWN:
                if (W/2 - 50 <= mouse[0] <= W/2+50 and H-140 <= mouse[1] <= H-100):
                    pg.quit()
                    exit()
                elif (W/2 - 100 <= mouse[0] <= W/2+100 and H-350 <= mouse[1] <= H-300):
                    paused = False
        screen.blit(background, background_rect)
        text(screen, 'Пауза', '', 64, W / 2, H - 480)
        mouse = pg.mouse.get_pos()
        if (W/2 - 50 <= mouse[0] <= W/2+50 and H-140 <= mouse[1] <= H-100):
            pg.draw.rect(screen,PURPLE,[W/2-50,H-140,100,40])
            pg.draw.rect(screen,BLACK,[W/2-100, H-350,200,50])
        elif (W/2 - 100 <= mouse[0] <= W/2+100 and H-350 <= mouse[1] <= H-300):
            pg.draw.rect(screen,BLUE,[W/2-100,H-350,200,50])
            pg.draw.rect(screen,BLACK,[W/2-50, H-140,100,40])
        else:
            pg.draw.rect(screen,BLACK,[W/2-50, H-140,100,40])
            pg.draw.rect(screen,BLACK,[W/2-100, H-350,200,50])
        quittext = text(screen, 'Выход', '', 22, W / 2, H - 135)
        continuetext = text(screen, 'Продолжить', '', 25, W / 2, H - 340)
        pg.display.update()
    
def highscore():
    with open('records.txt','r') as file:
        lines = file.readlines()
        score = lines[0].strip()
    return score
    file.close()
        
def save_highscore(hscore):
    hscore = highscore()
    with open('records.txt','w') as file:
        if str(score)>hscore:
            file.write(str(score))
        else:
            file.write(str(hscore))
    file.close()
    
def show_menu():
    text(screen, 'Нажмите "пробел" чтобы начать игру', '', 19, W / 2, H - 300)
    menu = True
    while menu:
        clock.tick(FPS)
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONDOWN:
                if (W/2 - 50 <= mouse[0] <= W/2+50 and H-140 <= mouse[1] <= H-100):
                    pg.quit()
                    exit()
                elif (W/2 - 100 <= mouse[0] <= W/2+100 and H-350 <= mouse[1] <= H-300):
                    menu = False
        screen.blit(background, background_rect)
        text(screen, 'Shoot’em up', '', 64, W / 2, H - 580)
        text(screen, 'Управление:', '', 20, W / 2, H - 500)
        text(screen, 'стрелочки <-  -> для передвижения', '', 18, W / 2, H - 480)
        text(screen, '"пробел" чтобы стрелять', '', 18, W / 2, H - 460)
        text(screen, 'нажмите "P" для паузы', '', 18, W / 2, H - 440)
        hscore = highscore()
        text(screen, 'Лучший счет: ', (hscore), 18, W / 2, H - 280)
        mouse = pg.mouse.get_pos()
        if (W/2 - 50 <= mouse[0] <= W/2+50 and H-140 <= mouse[1] <= H-100):
            pg.draw.rect(screen,PURPLE,[W/2-50,H-140,100,40])
            pg.draw.rect(screen,BLACK,[W/2-100, H-350,200,50])
        elif (W/2 - 100 <= mouse[0] <= W/2+100 and H-350 <= mouse[1] <= H-300):
            pg.draw.rect(screen,BLUE,[W/2-100,H-350,200,50])
            pg.draw.rect(screen,BLACK,[W/2-50, H-140,100,40])
        else:
            pg.draw.rect(screen,BLACK,[W/2-50, H-140,100,40])
            pg.draw.rect(screen,BLACK,[W/2-100, H-350,200,50])
        quittext = text(screen, 'Выход', '', 22, W / 2, H - 135)
        playtext = text(screen, 'Начать игру', '', 25, W / 2, H - 340)
        pg.display.update()

class Player(pg.sprite.Sprite):
    def __init__(player):
        pg.sprite.Sprite.__init__(player)
        player.image = player_img
        player.image.set_colorkey(BLACK)
        player.rect = player.image.get_rect()
        player.radius = int(player.rect.width / 2)
        player.rect.centerx = W / 2
        player.rect.bottom = H - 15
        player.speedx = 0
        player.hp = 100
        player.shoot_delay = 250
        player.last_shot = pg.time.get_ticks()
        player.lives = 3
        player.hidden = False
        player.hide_timer = pg.time.get_ticks()
        player.power = 1
        player.power_time = pg.time.get_ticks()
        
    def update(player):

        if player.power >= 2 and pg.time.get_ticks() - player.power_time > poweruptime:
            player.power -= 1
            player.power_time = pg.time.get_ticks()
        
        if player.hidden and pg.time.get_ticks() - player.hide_timer > 1000:
            player.hidden = False
            player.rect.centerx = W / 2
            player.rect.bottom = H - 10
            
        player.speedx = 0
        key = pg.key.get_pressed()
        if key[pg.K_LEFT]:
            player.speedx = -5
        if key[pg.K_RIGHT]:
            player.speedx = 5
        if key[pg.K_SPACE]:
            player.shoot()
        if key[pg.K_p]:
            pause()
        player.rect.x += player.speedx
        if player.rect.right > W:
            player.rect.right = W
        if player.rect.left < 0:
            player.rect.left = 0

    def powerup(player):
        player.power_time = pg.time.get_ticks()
        player.power += 1
        player.power_time = pg.time.get_ticks()
        
    def shoot(player):
        current_time = pg.time.get_ticks()
        if current_time - player.last_shot > player.shoot_delay:
            player.last_shot = current_time
            if player.power == 1:
                bullet = Bullet(player.rect.centerx, player.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
                shoot_snd.play()
            if player.power == 2:
                b1 = Bullet(player.rect.left, player.rect.centery)
                b2 = Bullet(player.rect.right, player.rect.centery)
                all_sprites.add(b1)
                all_sprites.add(b2)
                bullets.add(b1)
                bullets.add(b2)
                shoot_snd.play()
            if player.power >= 3:
                b1 = Bullet(player.rect.left, player.rect.centery)
                b2 = Bullet(player.rect.right, player.rect.centery)
                b3 = Bullet(player.rect.centerx, player.rect.top)
                all_sprites.add(b1)
                all_sprites.add(b2)
                all_sprites.add(b3)
                bullets.add(b1)
                bullets.add(b2)
                bullets.add(b3)
                shoot_snd.play()
                

    def hide(player):
        player.hidden = True
        player.hide_timer = pg.time.get_ticks()
        player.rect.center = (W / 2, H + 200)

class Bullet(pg.sprite.Sprite):
    def __init__(bullet, x, y):
        pg.sprite.Sprite.__init__(bullet)
        bullet.image = pg.Surface((3, 15))
        bullet.image.fill(YELLOW)
        bullet.rect = bullet.image.get_rect()
        bullet.rect.bottom = y
        bullet.rect.centerx = x
        bullet.speedy = -10

    def update(bullet):
        bullet.rect.y += bullet.speedy
        if bullet.rect.bottom < 0:
            bullet.kill()

class Mob(pg.sprite.Sprite):
    def __init__(mob):
        pg.sprite.Sprite.__init__(mob)
        mob.image_orig = random.choice(mobs_img)
        mob.image_orig.set_colorkey(BLACK)
        mob.image = mob.image_orig.copy()
        mob.rect = mob.image.get_rect()
        mob.radius = int(mob.rect.width / 2)
        mob.rect.x = random.randrange(W - mob.rect.width)
        mob.rect.y = random.randrange(-100, -40)
        mob.speedx = random.randrange(-1, 1)
        if (lvl >= 1):
            mob.speedy = 1
        if (lvl >= 3):
            mob.speedy = random.randrange(1, 3)
        if (lvl >= 5):
            mob.speedy = random.randrange(3, 5)
        if (lvl >= 7):
            mob.speedy = random.randrange(5, 10)
        if (lvl >= 9):
            mob.speedy = random.randrange(5, 15)
        
    def update(mob):
        mob.rect.x += mob.speedx
        mob.rect.y += mob.speedy
        if mob.rect.top > H + 10 or \
           mob.rect.left < -10 or \
           mob.rect.right > W + 10:
            mob.kill()
            create_new_mob()

class Explosion(pg.sprite.Sprite):
    def __init__(expl, center, size):
        pg.sprite.Sprite.__init__(expl)
        expl.size = size
        expl.image = expl_anim[expl.size][0]
        expl.rect = expl.image.get_rect()
        expl.rect.center = center
        expl.frame = 0
        expl.last_update = pg.time.get_ticks()
        expl.frame_rate = 50

    def update(expl):
        now = pg.time.get_ticks()
        if now - expl.last_update > expl.frame_rate:
            expl.last_update = now
            expl.frame += 1
            if expl.frame == len(expl_anim[expl.size]):
                expl.kill()
            else:
                center = expl.rect.center
                expl.image = expl_anim[expl.size][expl.frame]
                expl.rect = expl.image.get_rect()
                expl.rect.center = center

class Powerup(pg.sprite.Sprite):
    def __init__(power, center):
        pg.sprite.Sprite.__init__(power)
        power.type = random.choice(['healthup', 'gun'])
        power.image = powerup_img[power.type]
        power.image.set_colorkey(BLACK)
        power.rect = power.image.get_rect()
        power.rect.center = center
        power.speedy = 2
    
    def update(power):
        power.rect.y += power.speedy
        if power.rect.top > H:
            power.kill()

# Загрузка игровой графики
background = pg.image.load(path.join(img_folder, 'sky.png')).convert()
background_rect = background.get_rect()
player_img = pg.image.load(os.path.join(img_folder, 'player spaceship0.png')).convert()
player_live_img = pg.transform.scale(player_img, (25, 30))
player_live_img.set_colorkey(BLACK)
mobs_img = []
mobs_list = ['mob1.png', 'mob1 big.png', 'mob1 small.png',
             'mob2.png', 'mob2 big.png', 'mob2 small.png',
             'mob3.png', 'mob3 big.png','mob3 small.png']
for models in mobs_list:
    mobs_img.append(pg.image.load(path.join(img_folder, models)).convert())
powerup_img = {}
powerup_img['healthup'] = pg.image.load(path.join(img_folder, 'healthup.png')).convert()
powerup_img['gun'] = pg.image.load(path.join(img_folder, 'gun.png')).convert()

# Анимации
expl_anim = {}
expl_anim['ex'] = []
expl_anim['player'] = []
for i in range(8):
    filename = 'ex{}.png'.format(i)
    img = pg.image.load(path.join(img_folder, filename)).convert()
    img.set_colorkey(BLACK)
    img_ex = pg.transform.scale(img, (70, 70))
    expl_anim['ex'].append(img_ex)
    
    filename = 'expl{}.png'.format(i)
    img = pg.image.load(path.join(img_folder, filename)).convert()
    img.set_colorkey(BLACK)
    img_ex_pl = pg.transform.scale(img, (120, 120))
    expl_anim['player'].append(img_ex_pl)

# Загрузка звуковой части
shoot_snd = pg.mixer.Sound(path.join(snd_folder, 'laser.wav'))
expl_snd = pg.mixer.Sound(path.join(snd_folder, 'explosion.ogg'))
powerup_snd = pg.mixer.Sound(path.join(snd_folder, 'powerup.wav'))
kill_snds = []
for snd in ['kill mob 1.wav', 'kill mob 2.wav']:
    kill_snds.append(pg.mixer.Sound(path.join(snd_folder, snd)))
pg.mixer.music.load(path.join(snd_folder, 'theme.mp3'))
pg.mixer.music.set_volume(0.4)
pg.mixer.music.play(loops=-1)

# Цикл игры
menu = True
game_over = True
running = True
paused = False
record = False
while running:
    key = pg.key.get_pressed()
    if game_over:
        score = 0
        show_menu()
        game_over = False
        all_sprites = pg.sprite.Group()
        mobs = pg.sprite.Group()
        powerups = pg.sprite.Group()
        bullets = pg.sprite.Group()
        player = Player()
        all_sprites.add(player)
        for i in range(6):
            create_new_mob()
            
    clock.tick(FPS)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if (score >= newscore+1500):
            lvl+=1
            newscore += 1500

    all_sprites.update()

    hits_mobs = pg.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits_mobs:
        score += 60 - hit.radius
        random.choice(kill_snds).play()
        expl = Explosion(hit.rect.center, 'ex')
        all_sprites.add(expl)
        if random.random() > 0.9:
            powerup = Powerup(hit.rect.center)
            all_sprites.add(powerup)
            powerups.add(powerup)
        create_new_mob()
    
    hits_player = pg.sprite.spritecollide(player, mobs, True, pg.sprite.collide_circle)
    for hit in hits_player:
        player.hp -= hit.radius / 1.5
        expl_snd.play()
        expl = Explosion(hit.rect.center, 'ex')
        all_sprites.add(expl)
        create_new_mob()
        if player.hp <= 0:
            death_expl = Explosion(player.rect.center, 'player')
            all_sprites.add(death_expl)
            player.hide()
            player.lives -= 1
            player.hp = 100
        
    player_powerup = pg.sprite.spritecollide(player, powerups, True)
    for hit in player_powerup:
        if hit.type == 'healthup':
            powerup_snd.play()
            player.hp += random.randrange(10, 30)
            if player.hp >= 100:
                player.hp = 100
        if hit.type == 'gun':
            powerup_snd.play()
            player.powerup()

    if player.lives == 0 and not death_expl.alive():
        save_highscore(score)
        game_over = True

    # Рендеринг   
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    text(screen, 'Уровень: ', str(int(lvl)), 18, W/2, 1)
    text(screen, 'Очки: ', str(int(score)), 18, W/2, 20)
    draw_hp_bar(screen, W - 110, 5, player.hp)
    draw_lives(screen, 5, 5, player.lives, player_live_img)
    pg.display.flip()

pg.quit()
