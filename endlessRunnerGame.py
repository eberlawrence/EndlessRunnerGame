import pygame
from random import randint
import numpy as np
from keras.utils import to_categorical
import matplotlib.pyplot as plt
import seaborn as sns
from DQN import DQNAgent

speed = 1

class Road:
    pygame.display.set_caption('Endless Runner Game 1.0')

    def __init__(self, width, height):
        self.width = width
        self.height = width
        self.coins = Coins(self)
        self.car = Car(self)
        self.score = 0
        
        self.crashed = False
        self.gameDisplay = pygame.display.set_mode((width, height))
        self.backGround1 = pygame.image.load("images/backGround1.png")
        self.backGround2 = pygame.image.load("images/backGround2.png")
        self.backGround3 = pygame.image.load("images/backGround3.png")


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

        self.change = 20

    def update_position(self, x, y):

        if self.position[-1][0] != x:
            if self.coins > 1:
                for i in range(0, self.coins - 1):
                    self.position[i][0], self.position[i][1] = self.position[i + 1]
            self.position[-1][0] = x
            self.position[-1][1] = y

    def moveCar(self, move, x, y, road, coins):
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

        self.x = x + moving

        if self.x < 0 or self.x > road.width - 120:
            road.crashed = True

        reach(self, coins, road)
        self.update_position(self.x, self.y)

    def displayCar(self, x, y, coins, road):
        self.position[-1][0] = x
        self.position[-1][1] = y

        if not road.crashed:
            for i in range(coins):
                x_temp, y_temp = self.position[len(self.position) - 1 - i]
                road.gameDisplay.blit(self.image, (x_temp, y_temp))

            pygame.display.update()
        else:
            pygame.time.wait(300)


class Coins(object):

    def __init__(self, road):
        self.x_coins = randint(int(road.width * 0.45), int(road.width * 0.55))
        self.y_coins = int(road.width*0.21)
        self.image = pygame.image.load('images/coinL.png')
        self.image = pygame.transform.scale(image, (int(34*0.2),int(42*0.2)))

    def moveCoins(self):
        pass

    def coinsPosition(self, road):
        self.x_coins = randint(road.width * 0.4, road.width * 0.6)
        self.y_coins = road.height * 0.3

    def displayCoins(self, x, y, road):
        road.gameDisplay.blit(self.image, (x, y))
        pygame.display.update()


def reach(car, coins, road):
    if car.x == coins.x_coins and car.y == coins.y_coins:
        coins.coinsPosition(road)
        car.reached = True
        road.score = road.score + 1


def getRecord(score, record):
        if score >= record:
            return score
        else:
            return record


def display(car, coins, road, record, background=1):
    if background == 1:
        road.gameDisplay.blit(road.backGround1, (0, 0))
    if background == 2:
        road.gameDisplay.blit(road.backGround2, (0, 0))
    if background == 3:
        road.gameDisplay.blit(road.backGround3, (0, 0))

    car.displayCar(car.position[-1][0], car.position[-1][1], car.coins, road)
    coins.displayCoins(coins.x_coins, coins.y_coins, road)
 

def startGame(car, road, coins, agent):
    preState = agent.get_state(road, car, coins)
    action = [0, 1, 0]
    car.moveCar(action, car.x, car.y, road, coins)
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
            myCar.moveCar(final_move, myCar.x, myCar.y, road, myCoins)
            state_new = agent.get_state(road, myCar, myCoins)
            #set treward for the new state
            reward = agent.set_reward(myCar, road.crashed)
            
            #train short memory base on the new action and state
            agent.train_short_memory(state_old, final_move, reward, state_new, road.crashed)
            
            # store the new data into a long term memory
            agent.remember(state_old, final_move, reward, state_new, road.crashed)
            record = getRecord(road.score, record)
            display(myCar, myCoins, road, record)
            pygame.time.wait(speed)
        
        agent.replay_new(agent.memory)
        countGames += 1
    agent.model.save_weights('weights.hdf5')



run()

