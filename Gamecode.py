import pygame
import random
import math
from pygame import mixer

# initialize pygame always required
pygame.init()
# creates the screen ((height,width))
height = 600
width = 800
screen = pygame.display.set_mode((width, height))

# backgroud image
# background = pygame.image.load('image name/ locaiton)
# mixer.music.load(r'C:\Users\sense\Documents\python_game_resources\Sounds\laserattack.wav')
# mixer.music.play(-1)
# Title and Icon
pygame.display.set_caption('Jo Mama Invaders')
# icon=pygame.image.load('name_of_image.filetype') if you want to make an icon
# pygame.dislpay.set_icon(icon) if you want to display that icon

# creates the player
player_image = pygame.image.load(r'C:\Users\sense\Documents\python_game_resources\Icons\space-invaders.png')
player_x = round(width / 2)
player_y = height - 64
player_x_ch = 0
player_y_ch = 0

# creates the enemys
enemy_image = []
enemy_x = []
enemy_y = []
enemy_x_ch = []
enemy_y_ch = []
num_of_en = 6
for i in range(num_of_en):
    enemy_image.append(pygame.image.load(r'C:\Users\sense\Documents\python_game_resources\Icons\ufo.png'))
    enemy_x.append(random.randint(0, width - 64))
    enemy_y.append(random.randint(0, round(height / 2)))
    enemy_x_ch.append(.5)
    enemy_y_ch.append(30)

# Projectile//missile
# ready state means you cant see the bullet and fire
shoot = pygame.image.load(r'C:\Users\sense\Documents\python_game_resources\Icons\missile.png')
shoot_x = player_x
shoot_y = player_y
shoot_x_ch = 0
shoot_y_ch = 8
# ready state means you cant see the bullet and fire
shoot_state = 'ready'

#creates a second kind of attack
super = pygame.image.load(r'C:\Users\sense\Documents\python_game_resources\Icons\fighter.png')
super_x = player_x
super_y = player_y
super_x_ch = 0
super_y_ch = .5
# ready state means you cant see the bullet and fire
super_state = 'ready'
super_shots = 0

# initializing enemy bombs
bomb = pygame.image.load(r'C:\Users\sense\Documents\python_game_resources\Icons\bomb.png')
bomb_x = enemy_x[1]
bomb_y = enemy_y[1]+10

# score
score = 0
font = pygame.font.Font('freesansbold.ttf', 32)
text_x = 10
text_y = 10
last_step_score = 0

def show_score(x, y):
    sc = font.render('Score: ' + str(score)+ " Fighters: " + str(super_shots), True, (255, 255, 255))
    screen.blit(sc, (text_x, text_y))


def player(x, y):
    screen.blit(player_image, (x, y))


def enemy(x, y, i):
    screen.blit(enemy_image[i], (x, y))


def fire_bullet(x, y):
    global shoot_state
    shoot_state = 'fire'
    screen.blit(shoot, (x + 16, y + 10))

def fire_super(x, y):
    global super_state
    super_state = 'fire'
    screen.blit(super, (x + 16, y + 10))


def hit(enemy_x, enemy_y, shoot_x, shoot_y, hit_box):
    distance = math.sqrt(math.pow((enemy_x - shoot_x), 2) + math.pow((enemy_y - shoot_y), 2))
    if distance < hit_box:
        return True
    else:
        return False


# Game loop, keeps it open till you close it
running = True
player_death = False
# keeps the game window open with an infinite loop
while running:
    # RGB ((red,green,blue)) 0-255
    screen.fill((10, 0, 30))
    # to add a background image for will slow down code
    # screen.blit(background, (0,0))
    for event in pygame.event.get():

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_ch = -1.5
            if event.key == pygame.K_RIGHT:
                player_x_ch = 1.5
            if event.key == pygame.K_UP:
                player_y_ch = -1.5
            if event.key == pygame.K_DOWN:
                player_y_ch = 1.5
            if event.key == pygame.K_SPACE:
                if shoot_state is 'ready':
                    missile_sound = mixer.Sound(r'C:\Users\sense\Documents\python_game_resources\Sounds\missile.wav')
                    missile_sound.play(0)
                    shoot_x = player_x
                    fire_bullet(shoot_x, shoot_y)
            if event.key == pygame.K_TAB:
                if super_state is 'ready' and super_shots >=1:
                    super_x = player_x+20
                    fire_super(super_x, super_y)
                    super_shots -=1

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_ch = 0

            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                player_y_ch = 0

        if event.type == pygame.QUIT:
            # quits the game when you hit the close button
            running = False
    if score%10 == 0 and score!=last_step_score:
        super_shots+=1
    last_step_score = score
    # player movement
    player_x += player_x_ch
    if player_x <= 0:
        player_x = 0
    if player_x >= width - 64:
        player_x = width - 64
    player(player_x, player_y)

    player_y += player_y_ch
    if player_y <= 0:
        player_y = 0
    if player_y >= height - 64:
        player_y = height - 64
    player(player_x, player_y)

    # enemy movement
    for i in range(num_of_en):
        if enemy_x[i] >= width - 64:
            enemy_x_ch[i] = -1.5
            enemy_y[i] += enemy_y_ch[i]
        if enemy_x[i] <= 0:
            enemy_x_ch[i] = 1.5
            enemy_y[i] += enemy_y_ch[i]
        enemy_x[i] += enemy_x_ch[i]
        enemy(enemy_x[i], enemy_y[i], i)
    # enemy bomb (1)
    screen.blit(bomb, (bomb_x, bomb_y))
    if bomb_y >= height:
        bomb_y = enemy_y[1]
        bomb_x = enemy_x[1]
    else:
        bomb_y += 1

    # projectile movement
    if shoot_state is 'fire':
        fire_bullet(shoot_x, shoot_y)
        shoot_y -= shoot_y_ch
    if shoot_y <= 0:
        shoot_state = 'ready'
        shoot_y = player_y

    if super_state is 'fire':
        fire_super(super_x, super_y)
        super_y -= super_y_ch
    if super_y <= 0:
        super_state = 'ready'
        super_y = player_y

    # kill enemy
    for i in range(num_of_en):
        kill = hit(enemy_x[i], enemy_y[i], shoot_x, shoot_y, 30)
        if kill == True:
            shoot_y = player_y
            shoot_state = 'ready'
            score += 1
            ex_sound = mixer.Sound(r'C:\Users\sense\Documents\python_game_resources\Sounds\explosion.wav')
            ex_sound.play(0)
            enemy_x[i] = random.randint(0, width - 64)
            enemy_y[i] = random.randint(0, height - 250)
        super_kill = hit(enemy_x[i], enemy_y[i], super_x, super_y, 150)
        if super_kill == True:
            shoot_state = 'ready'
            score += 1
            ex_sound = mixer.Sound(r'C:\Users\sense\Documents\python_game_resources\Sounds\explosion.wav')
            ex_sound.play(0)
            enemy_x[i] = random.randint(0, width - 64)
            enemy_y[i] = random.randint(0, height-120)
    player_death = hit(bomb_x, bomb_y, player_x, player_y, 40)
    if player_death == True:
        ex_sound = mixer.Sound(r'C:\Users\sense\Documents\python_game_resources\Sounds\explosion.wav')
        ex_sound.play(0)
        running = False
    for i in range(num_of_en):
        player_death = hit(enemy_x[i], enemy_y[i], player_x, player_y, 60)
        if player_death:
            ex_sound = mixer.Sound(r'C:\Users\sense\Documents\python_game_resources\Sounds\explosion.wav')
            ex_sound.play(0)
            running = False

    show_score(text_x, text_y)
    pygame.display.update()
    # always required for anything to change
over = True
while over==True:
    screen.fill((250, 0, 0))
    #screen.fill((random.randint(0,255), random.randint(0,255), random.randint(0,255)))
    over_text = font.render('GAME OVER Score = ' + str(score), True, (255, 255, 255))
    screen.blit(over_text, (round(width / 2) - 200, round(height / 2)))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
        # quits the game when you hit the close button
            over = False
    pygame.display.update()
