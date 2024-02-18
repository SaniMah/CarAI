import pygame
import random
import sys


pygame.init()


WIDTH, HEIGHT = 600, 1000
FPS = 60
WHITE = (255, 255, 255)
RED = (255, 0, 0)
CAR_WIDTH, CAR_HEIGHT = 50, 290
CAR_SPEED = 5
ENEMY_SPEED = 3
ENEMY_ADD_FREQUENCY = 0.01


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Avoid the Cars")


player_car_img = pygame.image.load("main_car2.png")  
enemy_car_img = pygame.image.load("main_car1.png")  
road_img = pygame.image.load("road.png")  


road_img = pygame.transform.scale(road_img, (WIDTH, HEIGHT))


player_car = pygame.Rect(WIDTH // 2 - CAR_WIDTH // 2, HEIGHT - CAR_HEIGHT - 10, CAR_WIDTH, CAR_HEIGHT)


enemies = []


road_y = 0


score = 0
lives = 3
font = pygame.font.Font(None, 36)


clock = pygame.time.Clock()


def draw_player_car():
    screen.blit(player_car_img, (player_car.x, player_car.y))

def draw_enemy_cars():
    for enemy in enemies:
        screen.blit(enemy_car_img, (enemy.x, enemy.y))


def move_enemy_cars():
    global score, lives
    for enemy in enemies:
        enemy.y += ENEMY_SPEED
        if enemy.y > HEIGHT:
            enemies.remove(enemy)
            score += 1  


def add_enemy_car():
    enemy_width = CAR_WIDTH
    enemy_height = CAR_HEIGHT
    while True:
        enemy_x = random.randint(0, WIDTH - enemy_width)
        enemy_y = -enemy_height
        enemy_rect = pygame.Rect(enemy_x, enemy_y, enemy_width, enemy_height)
        
        if not enemy_rect.colliderect(player_car):
            if not any(enemy_rect.colliderect(existing_enemy) for existing_enemy in enemies):
                enemies.append(enemy_rect)
                break


def draw_info():
    score_text = font.render("Score: {}".format(score), True, (0, 0, 0))
    lives_text = font.render("Lives: {}".format(lives), True, (0, 0, 0))
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (10, 50))


while lives > 0:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_car.x > 0:
        player_car.x -= CAR_SPEED
    if keys[pygame.K_RIGHT] and player_car.x < WIDTH - CAR_WIDTH:
        player_car.x += CAR_SPEED

    
    move_enemy_cars()

    
    if random.random() < ENEMY_ADD_FREQUENCY:
        add_enemy_car()

    
    for enemy in enemies:
        if player_car.colliderect(enemy):
            lives -= 1  
            enemies.remove(enemy)

   
    screen.fill(WHITE)

    
    road_y += ENEMY_SPEED  
    if road_y > HEIGHT:
        road_y = 0

    
    screen.blit(road_img, (0, road_y))
    screen.blit(road_img, (0, road_y - HEIGHT))  

    
    draw_player_car()
    draw_enemy_cars()

    
    draw_info()

    
    pygame.display.flip()

    
    clock.tick(FPS)


game_over_text = font.render("Game Over - Score: {}".format(score), True, (255, 0, 0))
screen.blit(game_over_text, (WIDTH // 2 - 150, HEIGHT // 2 - 20))
pygame.display.flip()
pygame.time.wait(2000) 
pygame.quit()
sys.exit()

