import pygame
import sys
from pygame.locals import *
from Player import Player
from Bubble import Bubble
 
pygame.init()
 
screen = pygame.display.set_mode((640, 460))
screen.fill((255, 255, 255))
pygame.display.set_caption('Bubble Buster!')
font = pygame.font.SysFont(None, 36)
 
main_clock = pygame.time.Clock()
 
score = 0
 
#Adding lives
lives = 3
alive = True
 
#create and set up values for the player
player = Player()
player.rect.x = 250
player.rect.y = 380
player_speed = player.speed

draw_group = pygame.sprite.Group()
draw_group.add(player)


bubble_group = pygame.sprite.Group()


move_left = False
move_right = False
move_down = False
move_up = False
 
def draw_screen():
    screen.fill((255, 255, 255))
def draw_player():
    pygame.draw.rect(screen, (0, 0, 0), player)
 
def draw_text(display_string, font, surface, x, y):
    text_display = font.render(display_string, 1, (0, 0, 0))
    text_rect = text_display.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_display, text_rect)
 
x_position = 320
y_position = 380
last_x = x_position
last_y = y_position
ball = pygame.draw.circle(screen, (0, 0, 0), (x_position, y_position), 5, 0)
ball_can_move = False
 
speed = [5,-5]
 
 
#values for all bubbles to use
all_bubbles = []
number_of_bubbles = 30
bubble_radius = 20
bubble_edge = 1
initial_bubble_position = 70
bubble_spacing = 60
 
def create_bubbles():
    bubble_x = initial_bubble_position
    bubble_y = initial_bubble_position
 
    for rows in range(0, 3):
        for columns in range(0, 10):
            bubble = Bubble(bubble_x, bubble_y)
            bubble_group.add(bubble)
            bubble_x += bubble_spacing
            #all_bubbles.append(bubble)
        bubble_y += bubble_spacing
        bubble_x = initial_bubble_position
 
create_bubbles()
 
def draw_bubbles():
    for bubble in all_bubbles:
        bubble = pygame.draw.circle((screen), (0, 0, 0), (bubble.x, bubble.y), bubble_radius, bubble_edge)
 
while True:
    # check for events
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        #Keyboard input for players
        if event.type == KEYDOWN:
            if event.key == K_a:
                move_right = False
                move_left = True
            if event.key == K_d:
                move_left = False
                move_right = True
            if event.key == K_s:
                move_down = True
                move_up = False
            if event.key == K_w:
                move_down = False
                move_up = True
        if event.type == KEYUP:
            if event.key == K_a:
                move_left = False
            if event.key == K_d:
                move_right = False
            if event.key == K_s:
                move_down = False
            if event.key == K_w:
                move_up = False
        
            if alive:
                if event.key == K_SPACE:
                    ball_can_move = True
            if not alive:
                if event.key == K_RETURN:
                    alive = True
                    lives = 3
                    score = 0
                    ball_can_move = False
                    for x in range(0, len(all_bubbles)):
                        all_bubbles.pop()
                    create_bubbles()
 
    #Ensure consistent frames per second
    main_clock.tick(50)
 
    #Move the player
    if move_left and player.rect.left > 0:
        player.rect.x -= player_speed
    if move_right and player.rect.right < 640:
        player.rect.x += player_speed
    if move_up and player.rect.up > 0:
        player.rect.y -= player_speed
    if move_up and player.rect.down < 460:
        player.rect.y += player_speed
 
    #Move the ball
    if ball_can_move:
        last_x = x_position
        last_y = y_position
 
        x_position += speed[0]
        y_position += speed[1]
        if ball.x <= 0:
            x_position = 15
            speed[0] = -speed[0]
        elif ball.x >= 640:
            x_position = 625
            speed[0] = -speed[0]
        if ball.y <= 0:
            y_position = 15
            speed[1] = -speed[1]
                #Subtracting lives
        elif ball.y >= 460:
            lives -= 1
            ball_can_move = False
 
        #Test collisions with the player
        if ball.colliderect(player):
            y_position -= 15
            speed[1] = -speed[1]
 
        #Move direction vector
        move_direction = ((x_position - last_x), (y_position - last_y))
 
        #Test collisions with the bubbles
        for bubble in bubble_group:
            if ball.colliderect(bubble.rect):
                if move_direction[1] > 0:
                    speed[1] = -speed[1]
                    y_position -= 10
                elif move_direction[1] < 0:
                    speed[1] = -speed[1]
                    y_position += 10
                bubble_group.remove(bubble)
                pygame.display.update()
                score += 100
                break
 
    else:
        x_position = player.rect.x + 30
        y_position = player.rect.y + 30
 
    if lives <= 0:
        alive = False
 
    draw_screen()
    draw_group.draw(screen)
    draw_bubbles()
    ball = pygame.draw.circle(screen, (0, 0, 0), (x_position, y_position), 6, 0)
 
    if alive:
        draw_text('Score: %s' % (score), font, screen, 5, 5)
        draw_text('Lives: %s' % (lives), font, screen, 540, 5)
    else:
        draw_text('Game Over', font, screen, 255, 5)
        draw_text('Press Enter to Play Again', font, screen, 180, 50)
 
    pygame.display.update()
