import pygame
from random import randint
import numpy as np
from keras.utils import to_categorical
import matplotlib.pyplot as plt
import seaborn as sns
from DQN import DQNAgent


display_option =  True
speed = 1000

class Road:
    pygame.display.set_caption('Endless Runner Game 1.0')

    def __init__(self, width, height):
        self.width = width
        self.height = width
        self.coins = Coins()
        self.car = Car(self)
        self.score = 0
        
        self.crashed = False
        self.gameDisplay = pygame.display.set_mode((width, height))
        self.backGround1 = pygame.image.load("images/backGround1.png")
        #self.backGround2 = pygame.image.load("images/backGround2.png")
        #self.backGround3 = pygame.image.load("images/backGround3.png")


class Car(object):
    
    def __init__(self, road):
        self.x = 0.5 * road.width - 60
        self.y = 0.4 * road.height
        # self.x = x - x % 20
        # self.y = y - y % 20

        self.image = pygame.image.load('images/car1.png')

        self.position = []
        self.position.append([self.x, self.y])
        self.coins = 1
        self.reached = False

        self.change = 120

    def update_position(self, x, y):

        if self.position[-1][0] != x:
            if self.coins > 1:
                for i in range(0, self.coins - 1):
                    self.position[i][0], self.position[i][1] = self.position[i + 1]
            self.position[-1][0] = x
            self.position[-1][1] = y

    def do_move(self, move, x, y, road, coins):
        moving = self.change

        if self.reached:
            self.position.append([self.x, self.y])
            self.reached = False
            self.coins = self.coins + 1

        if np.array_equal(move, [1, 0, 0]):
            moving = 0

        elif np.array_equal(move, [0, 1, 0]):
            moving = self.change

        elif np.array_equal(move, [0, 0, 1]):
            moving = -self.change

        print(moving)
        self.x = x + moving

        if self.x < 0 or self.x > road.width - 120:
            road.crashed = True

        reach(self, coins, road)
        self.update_position(self.x, self.y)

    def display_Car(self, x, y, coins, road):
        self.position[-1][0] = x
        self.position[-1][1] = y

        if not road.crashed:
            for i in range(coins):
                x_temp, y_temp = self.position[len(self.position) - 1 - i]
                road.gameDisplay.blit(self.image, (x_temp, y_temp))

            update_screen()
        else:
            pygame.time.wait(300)


class Coins(object):

    def __init__(self):
        self.x_coins = 240
        self.y_coins = 200
        self.image = pygame.image.load('images/coins.png')

    def coins_coord(self, road, car):
        x_rand = randint(20, road.width - 40)
        self.x_coins = x_rand - x_rand % 20
        y_rand = randint(20, road.height - 40)
        self.y_coins = y_rand - y_rand % 20
        if [self.x_coins, self.y_coins] not in car.position:
            return self.x_coins, self.y_coins
        else:
            self.coins_coord(road, car)

    def display_coins(self, x, y, road):
        road.gameDisplay.blit(self.image, (x, y))
        update_screen()


def reach(car, coins, road):
    if car.x == coins.x_coins and car.y == coins.y_coins:
        coins.coins_coord(road, car)
        car.reached = True
        road.score = road.score + 1


def get_record(score, record):
        if score >= record:
            return score
        else:
            return record


def display_Road(road, score, record, background=1):
    if background == 1:
        road.gameDisplay.blit(road.backGround1, (0, 0))
    if background == 2:
        road.gameDisplay.blit(road.backGround2, (0, 0))
    if background == 3:
        road.gameDisplay.blit(road.backGround3, (0, 0))


def display(car, coins, road, record):
    display_Road(road, road.score, record,)
    car.display_Car(car.position[-1][0], car.position[-1][1], car.coins, road)
    coins.display_coins(coins.x_coins, coins.y_coins, road)


def update_screen():
    pygame.display.update()


def startGame(car, road, coins, agent):
    preState = agent.get_state(road, car, coins)  # [0 0 0 0 0 0 0 0 0 1 0 0 0 1 0 0]
    action = [0, 1, 0]
    car.do_move(action, car.x, car.y, road, coins)
    posState = agent.get_state(road, car, coins)
    reward1 = agent.set_reward(car, road.crashed)
    agent.remember(preState, action, reward1, posState, road.crashed)
    agent.replay_new(agent.memory)


def run():
    pygame.init()
    agent = DQNAgent()
    countGames = 0    
    countGa = 0
    record = 0
    while countGames < 50:
        # Initialize classes
        road = Road(800, 450)
        myCar = road.car
        myCoins = road.coins

        # Perform first move
        startGame(myCar, road, myCoins, agent)
        if display_option:
            display(myCar, myCoins, road, record)

        while not road.crashed:
                 
            #agent.epsilon is set to give randomness to actions
            agent.epsilon = 80 - countGames
            
            #get old state
            state_old = agent.get_state(road, myCar, myCoins)
            
            #perform random actions based on agent.epsilon, or choose the action
            if randint(0, 200) < agent.epsilon:
                final_move = to_categorical(randint(0, 2), num_classes=3)
            else:
                # predict action based on the old state
                prediction = agent.model.predict(state_old.reshape((1, 4)))
                final_move = to_categorical(np.argmax(prediction[0]), num_classes=3)    
            #perform new move and get new state
            myCar.do_move(final_move, myCar.x, myCar.y, road, myCoins)
            state_new = agent.get_state(road, myCar, myCoins)
            #set treward for the new state
            reward = agent.set_reward(myCar, road.crashed)
            
            #train short memory base on the new action and state
            agent.train_short_memory(state_old, final_move, reward, state_new, road.crashed)
            
            # store the new data into a long term memory
            agent.remember(state_old, final_move, reward, state_new, road.crashed)
            record = get_record(road.score, record)
            if display_option:
                display(myCar, myCoins, road, record)
                pygame.time.wait(speed)
        
        agent.replay_new(agent.memory)
        countGames += 1
    agent.model.save_weights('weights.hdf5')



run()

