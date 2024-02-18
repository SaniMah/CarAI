import pygame
import random
import os
import neat


pygame.init()

WIN_WIDTH = 600
WIN_HEIGHT = 800
FLOOR = 730
STAT_FONT = pygame.font.SysFont("comicsans", 50)


WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Car Game")

car_img = pygame.image.load("main_car2.png")
road_img = pygame.image.load("road.png")


road_img = pygame.transform.scale(road_img, (WIN_WIDTH, WIN_HEIGHT))


gen = 0


class Car:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel = 0
        self.img = car_img

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= 5
        if keys[pygame.K_RIGHT] and self.x < WIN_WIDTH - self.img.get_width():
            self.x += 5

        ROAD_SCROLL_SPEED = 5
        self.y -= ROAD_SCROLL_SPEED

        # Add bounds checking to keep the car within the screen
        self.x = max(0, min(self.x, WIN_WIDTH - self.img.get_width()))
        self.y = max(0, min(self.y, WIN_HEIGHT - self.img.get_height()))

    def draw(self, win):
        win.blit(self.img, (self.x, self.y))


class EnemyCar:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel = 3
        self.img = pygame.image.load("main_car1.png") 

    def move(self):
        self.y += self.vel

    def draw(self, win):
        win.blit(self.img, (self.x, self.y))

        
        
        


def draw_window(win, player_car, enemies, score, gen):
    win.blit(road_img, (0, 0))
    player_car.draw(win)

 
    for enemy in enemies:
        enemy.draw(win)

    # score
    score_label = STAT_FONT.render("Score: " + str(score), 1, (255, 255, 255))
    win.blit(score_label, (WIN_WIDTH - score_label.get_width() - 15, 10))

    # generations
    gen_label = STAT_FONT.render("Gens: " + str(gen - 1), 1, (255, 255, 255))
    win.blit(gen_label, (10, 10))

    pygame.display.update()


def eval_genomes(genomes, config):
    global WIN, gen
    win = WIN
    gen += 1

    nets = []
    cars = []
    ge = []
    for genome_id, genome in genomes:
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        cars.append(Car(WIN_WIDTH // 2, WIN_HEIGHT - 150))
        ge.append(genome)

    enemies = []

    clock = pygame.time.Clock()

    score = 0
    run = True
    ENEMY_SPAWN_INTERVAL = 200  # Adjust this interval as needed

    while run and len(cars) > 0:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
                break

        for x, car in enumerate(cars):
            ge[x].fitness += 0.1
            car.move()

            # Ensure there is at least one enemy in the list before accessing its elements
            if not enemies:
                enemies.append(EnemyCar(random.randint(0, WIN_WIDTH - 50), -100))

            # send car location, enemy location and determine from network whether to move left or right
            output = nets[cars.index(car)].activate((car.x, abs(car.x - enemies[0].x), abs(car.x - enemies[0].y)))

            if output[0] > 0.5:
                car.x -= 5
            else:
                car.x += 5

        for enemy in enemies:
            enemy.move()

        # Generate a new enemy at regular intervals
        if pygame.time.get_ticks() % ENEMY_SPAWN_INTERVAL == 0:
            enemies.append(EnemyCar(random.randint(0, WIN_WIDTH - 50), -100))

        draw_window(WIN, cars[0], enemies, score, gen)

        # check for collision
        for car in cars:
            for enemy in enemies:
                if car.x < enemy.x + enemy.img.get_width() and car.x + car.img.get_width() > enemy.x \
                        and car.y < enemy.y + enemy.img.get_height() and car.y + car.img.get_height() > enemy.y:
                    ge[cars.index(car)].fitness -= 1
                    nets.pop(cars.index(car))
                    ge.pop(cars.index(car))
                    cars.pop(cars.index(car))




def run(config_file):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                 neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                 config_file)

    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(eval_genomes, 50)

    print('\nBest genome:\n{!s}'.format(winner))


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-file.txt')
    run(config_path)
