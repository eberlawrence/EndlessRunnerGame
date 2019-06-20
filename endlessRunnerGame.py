import pygame
from random import randint
import numpy as np
from keras.utils import to_categorical
import matplotlib.pyplot as plt
import seaborn as sns

class Road:
    pygame.display.set_caption('Endless Runner Game 1.0')
    def __init__(self, width, height)
        self.width = width
        self.height = width
        
        self.crashed = False
        self.gameDisplay = pygame.display.set_mode((width, height))
        self.backGround1 = pygame.image.load("images/backGround1.png")
        self.backGround2 = pygame.image.load("images/backGround2.png")
        self.backGround3 = pygame.image.load("images/backGround3.png")

class Car(object):
    
    def __init__(self, road):
        self.x = 0.5 * road.width
        self.y = 0.1 * road.height
        # self.x = x - x % 20
        # self.y = y - y % 20

        self.image = pygame.image.load('img/snakeBody.png')

        self.position = []
        self.position.append([self.x, self.y])
        self.food = 1
        self.eaten = False

        self.x_change = 120
        self.y_change = 0

    def do_move(self, move, x, y, game, food):
        move_array = [self.x_change, self.y_change]

        if self.eaten:
            self.position.append([self.x, self.y])
            self.eaten = False
            self.food = self.food + 1
        if np.array_equal(move, [1, 0]):
            move_array = [self.x_change, self.y_change]
        elif np.array_equal(move, [0, 1]):
            move_array = [-self.x_change, self.y_change]

        self.x_change, self.y_change = move_array
        self.x = x + self.x_change
        self.y = y + self.y_change


        if self.x < 0 or self.x > game.width - 120:
            game.crashed = True
        eat(self, food, game)

        self.update_position(self.x, self.y)


    def display_player(self, x, y, food, game):
        self.position[-1][0] = x
        self.position[-1][1] = y

        if not game.crash:
            for i in range(food):
                x_temp, y_temp = self.position[len(self.position) - 1 - i]
                game.gameDisplay.blit(self.image, (x_temp, y_temp))

            update_screen()
        else:
            pygame.time.wait(300)


class Coins(object):

    def __init__(self):
        self.x_coins = 240
        self.y_coins = 200
        self.image = pygame.image.load('img/food2.png')

    def food_coord(self, game, player):
        x_rand = randint(20, game.game_width - 40)
        self.x_coins = x_rand - x_rand % 20
        y_rand = randint(20, game.game_height - 40)
        self.y_coins = y_rand - y_rand % 20
        if [self.x_coins, self.y_coins] not in player.position:
            return self.x_coins, self.y_coins
        else:
            self.food_coord(game,player)

    def display_food(self, x, y, game):
        game.gameDisplay.blit(self.image, (x, y))
        update_screen()


def eat(player, food, game):
    if player.x == food.x_food and player.y == food.y_food:
        food.food_coord(game, player)
        player.eaten = True
        game.score = game.score + 1


def get_record(score, record):
        if score >= record:
            return score
        else:
            return record


def display_ui(game, score, record):
    game.gameDisplay.blit(game.bg, (10, 10))


def display(player, food, game, record):
    game.gameDisplay.fill((255, 255, 255))
    display_ui(game, game.score, record)
    player.display_player(player.position[-1][0], player.position[-1][1], player.food, game)
    food.display_food(food.x_food, food.y_food, game)


def update_screen():
    pygame.display.update()


def initialize_game(player, game, food, agent):
    state_init1 = agent.get_state(game, player, food)  # [0 0 0 0 0 0 0 0 0 1 0 0 0 1 0 0]
    action = [1, 0, 0]
    player.do_move(action, player.x, player.y, game, food, agent)
    state_init2 = agent.get_state(game, player, food)
    reward1 = agent.set_reward(player, game.crash)
    agent.remember(state_init1, action, reward1, state_init2, game.crash)
    agent.replay_new(agent.memory)











pygame.init()

display_width = 800
display_height = 600
bat_width = 55

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('A bit Racey')
clock = pygame.time.Clock()

batImg1 = pygame.image.load('images/bat1.png')
batImg2 = pygame.image.load('images/bat2.png')


def bat(img1, x, y):
    gameDisplay.blit(img1, (x, y))


def loop():
    flag = True
    count = 0
    x = (display_width * 0.45)
    y = (display_height * 0.8)
    x_change, y_change = 0, 0

    crash = False
    while not crash:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x_change = -55
            if event.key == pygame.K_RIGHT:
                x_change = 55        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                x_change = 0
        
        x += x_change

        gameDisplay.fill(white)

        if flag == True:
            bat(batImg1, x, y)
            count += 1
            if count == 25: 
                flag = False
                count = 0
        else:
            bat(batImg2, x, y)
            count += 1
            if count == 15: 
                flag = True
                count = 0
    
        if x > display_width - bat_width or x < 0:
            crash = True
            
        pygame.display.update()
        clock.tick(60)

loop()
pygame.quit()
quit()



