import pygame
from random import randint
import numpy as np
from keras.utils import to_categorical
import matplotlib.pyplot as plt
import seaborn as sns
from DQN import DQNAgent

speed = 10

class Road:
    pygame.display.set_caption('Endless Runner Game 1.0')

    def __init__(self, width, height):
        self.width = width
        self.height = width
        self.coins = Coins(self)
        self.car = Car(self)
        self.box = Box(self)
        self.score = 0
        
        
        self.gameDisplay = pygame.display.set_mode((width, height))
        self.backGround1 = pygame.image.load("images/backGround1.png")
        self.backGround2 = pygame.image.load("images/backGround2.png")
        self.backGround3 = pygame.image.load("images/backGround3.png")


class Car(object):
    
    def __init__(self, road):
        self.x = 0.5 * road.width - 60
        self.y = 0.45 * road.height
        self.crashed = False

        self.image = pygame.image.load('images/car1.png')
        self.imageM = pygame.image.load('images/car2.png')

        self.coins = 1
        self.reached = False
        self.rotation = False

        self.change = 20
        
    def moveCar(self, move, x, y, road, coins):
        moving = self.change

        if self.reached:
            self.reached = False
            self.coins = self.coins + 1

        if np.array_equal(move, [1, 0, 0]):
            moving = 0

        elif np.array_equal(move, [0, 1, 0]):
            moving = self.change

        elif np.array_equal(move, [0, 0, 1]):
            moving = -self.change

        self.x = x + moving

        reachOrCrash(self, coins, road)


    def displayCar(self, x, y, coins, road):

        if not self.crashed:
            if not self.rotation:
                road.gameDisplay.blit(self.image, (x, y))
                self.rotation = True
            else:
                road.gameDisplay.blit(self.imageM, (x, y))
                self.rotation = False

            pygame.display.update()
        else:
            pygame.time.wait(100)


class Coins(object):

    def __init__(self, road):
        self.i = 0
        self.rand = 0
        self.x_coins = 0
        self.y_coins = 0

    def firstPosition(self, road):
        self.y_coins = int(road.width*0.215)
        self.rand = randint(1, 4)
        if self.rand == 1:
            self.x_coins = (road.width * 0.4750) + 4
        if self.rand == 2:
            self.x_coins = (road.width * 0.4875) + 4
        if self.rand == 3:
            self.x_coins = (road.width * 0.5) + 4
        if self.rand == 4:
            self.x_coins = (road.width * 0.5125) + 4

    def moveCoins(self, road):
        pos = [0, 5, 10, 15, 25, 30, 35, 40, 45, 50]
        esc = [0.10, 0.12, 0.16, 0.22, 0.30, 0.40, 0.52, 0.66, 0.82, 1.0]
        if self.i == 0:
            self.firstPosition(road)
        if self.rand == 1:                        
            self.imageOriginal = pygame.image.load('images/coinL.png')
            self.x_coins -= pos[self.i] * 0.95       
        if self.rand == 2:
            self.imageOriginal = pygame.image.load('images/coinL.png')
            self.x_coins -= pos[self.i] * 0.2                  
        if self.rand == 3:
            self.imageOriginal = pygame.image.load('images/coinR.png')
            self.x_coins += pos[self.i] * 0.2
        if self.rand == 4:
            self.imageOriginal = pygame.image.load('images/coinR.png')
            self.x_coins += pos[self.i] * 0.95              

        self.size = list(self.imageOriginal.get_rect().size)
        self.image = pygame.transform.scale(self.imageOriginal, (int(self.size[0] * esc[self.i]), int(self.size[1] * esc[self.i]))) 
        self.y_coins += pos[self.i]
        self.i += 1

        if self.i == 10:
            self.firstPosition(road)                        
            self.i = 0

    def displayCoins(self, x, y, road):
        if self.i == 0:
            pass        
        else:
            road.gameDisplay.blit(self.image, (x, y))



class Box(object):

    def __init__(self, road):
        self.i = 0
        self.rand = 0
        self.x_box = 0
        self.y_box = 0

    def firstPosition(self, road):
        self.y_box = int(road.width*0.215)
        self.rand = randint(1, 4)
        if self.rand == 1:
            self.x_box = (road.width * 0.4750) + 4
        if self.rand == 2:
            self.x_box = (road.width * 0.4875) + 4
        if self.rand == 3:
            self.x_box = (road.width * 0.5) + 4
        if self.rand == 4:
            self.x_box = (road.width * 0.5125) + 4

    def moveBox(self, road):
        pos = [0, 5, 10, 15, 25, 30, 35, 40, 45, 50]
        esc = [0.10, 0.12, 0.16, 0.22, 0.30, 0.40, 0.52, 0.66, 0.82, 1.0]
        if self.i == 0:
            self.firstPosition(road)
        if self.rand == 1:                        
            self.imageOriginal = pygame.image.load('images/boxLL.png')
            self.x_box -= pos[self.i] * 0.95       
        if self.rand == 2:
            self.imageOriginal = pygame.image.load('images/boxL.png')
            self.x_box -= pos[self.i] * 0.2                  
        if self.rand == 3:
            self.imageOriginal = pygame.image.load('images/boxRR.png')
            self.x_box += pos[self.i] * 0.2
        if self.rand == 4:
            self.imageOriginal = pygame.image.load('images/boxR.png')
            self.x_box += pos[self.i] * 0.95              

        self.size = list(self.imageOriginal.get_rect().size)
        self.image = pygame.transform.scale(self.imageOriginal, (int(self.size[0] * esc[self.i]), int(self.size[1] * esc[self.i]))) 
        self.y_box += pos[self.i]
        self.i += 1

        if self.i == 10:
            self.firstPosition(road)                        
            self.i = 0

    def displayBox(self, x, y, road):
        if self.i == 0:
            pass        
        else:
            road.gameDisplay.blit(self.image, (x, y))


def reachOrCrash(car, coins, road):

    if car.x < road.width * 0.125 or car.x > (road.width * 0.875) - 120:
        car.crashed = True
    if car.x <= coins.x_coins and car.x + 120 >= coins.x_coins + 34 and car.y >= coins.y_coins and car.y <= coins.y_coins + 50:
        car.reached = True
        road.score = road.score + 1


def getRecord(score, record):
        if score >= record:
            return score
        else:
            return record


def display(car, coins, box, road, record, background=1):
    if background == 1:
        road.gameDisplay.blit(road.backGround1, (0, 0))
    if background == 2:
        road.gameDisplay.blit(road.backGround2, (0, 0))
    if background == 3:
        road.gameDisplay.blit(road.backGround3, (0, 0))
    coins.displayCoins(coins.x_coins, coins.y_coins, road)
    box.displayBox(box.x_box, box.y_box, road)
    car.displayCar(car.x, car.y, car.coins, road)

def startGame(car, coins, box, road, agent):
    preState = agent.get_state(car, coins, box, road)
    action = [0, 1, 0]
    car.moveCar(action, car.x, car.y, road, coins)
    coins.moveCoins(road)
    box.moveBox(road)
    posState = agent.get_state(car, coins, box, road)
    reward1 = agent.set_reward(car, car.crashed)
    agent.remember(preState, action, reward1, posState, car.crashed)
    agent.replay_new(agent.memory)


def run():
    pygame.init()
    agent = DQNAgent()
    countGames = 0    
    countGa = 0
    record = 0
    while countGames < 50:
        print("GAME " + str(countGames))
        # Initialize classes
        road = Road(800, 450)
        myCar = road.car
        myCoins = road.coins
        myBox = road.box
        backG = 1
        # Perform first move
        startGame(myCar, myCoins, myBox, road, agent)
        display(myCar, myCoins, myBox, road, record, backG)
    
        while not myCar.crashed:
            
            #agent.epsilon is set to give randomness to actions
            agent.epsilon = 80 - countGames
            
            #get old state
            state_old = agent.get_state(myCar, myCoins, myBox, road)
            
            #perform random actions based on agent.epsilon, or choose the action
            if randint(0, 200) < agent.epsilon:
                final_move = to_categorical(randint(0, 2), num_classes=3)
            else:
                # predict action based on the old state
                prediction = agent.model.predict(state_old.reshape((1, agent.dimInput)))
                final_move = to_categorical(np.argmax(prediction[0]), num_classes=3)    
            #perform new move and get new state
            myCar.moveCar(final_move, myCar.x, myCar.y, road, myCoins)
            myCoins.moveCoins(road)
            myBox.moveBox(road)
            state_new = agent.get_state(myCar, myCoins, myBox, road)
            #set treward for the new state
            reward = agent.set_reward(myCar, myCar.crashed)
            
            #train short memory base on the new action and state
            agent.train_short_memory(state_old, final_move, reward, state_new, myCar.crashed)
            
            # store the new data into a long term memory
            agent.remember(state_old, final_move, reward, state_new, myCar.crashed)
            record = getRecord(road.score, record)
            display(myCar, myCoins, myBox, road, record, backG)
            pygame.time.wait(speed)
            backG += 1
            if backG == 4:
                backG = 1
        agent.replay_new(agent.memory)
        countGames += 1
    agent.model.save_weights('weights.hdf5')



run()

