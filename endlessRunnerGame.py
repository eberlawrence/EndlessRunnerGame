'''
Eber Lawrence Souza Gouveia
Federal University of Uberlandia - UFU
Biomedical Engineering Lab - BioLab

To do:


'''
import pygame
from random import randint
import numpy as np
from keras.utils import to_categorical
import matplotlib.pyplot as plt
import seaborn as sns
from reinforcementLearning import deep_QNetwork
import matplotlib.pyplot as plt

speed = 1

class Road:
    pygame.display.set_caption('Endless Runner Game 1.0')

    def __init__(self, width, height):
        self.width = width
        self.height = width
        self.coins = Coins(self)
        self.car = Car(self)
        
        
        self.gameDisplay = pygame.display.set_mode((width, height))
        self.backGround1 = pygame.image.load("images/backGround1.png")
        self.backGround2 = pygame.image.load("images/backGround2.png")
        self.backGround3 = pygame.image.load("images/backGround3.png")
        self.backGround4 = pygame.image.load("images/backGround4.png")


class Car(object):
    
    def __init__(self, road):
        self.x = 0.5 * road.width - 60
        self.y = 0.46 * road.height        
        self.image = pygame.image.load('images/car1.png')
        self.imageM = pygame.image.load('images/car2.png')
        self.exp1 = pygame.image.load('images/explosion1.png')
        self.exp2 = pygame.image.load('images/explosion2.png')
        self.exp3 = pygame.image.load('images/explosion3.png')
        self.exp4 = pygame.image.load('images/explosion4.png')
        self.reachedBool = False        
        self.reached = 0
        self.missed = 0
        self.crashed = False
        self.rotation = False
        self.change = 0
        
    def moveCar(self, move, x, y, coins, road):

        if self.reachedBool:
            self.reachedBool = False

        if np.array_equal(move, [1, 0, 0]):
            self.change = 0
        elif np.array_equal(move, [0, 1, 0]):
            self.change = 60
        elif np.array_equal(move, [0, 0, 1]):
            self.change = -60
        self.x = x + self.change
        crash(self, road)

    def displayCar(self, x, y, road):
        if not self.rotation:
            road.gameDisplay.blit(self.image, (x, y))
            self.rotation = True
        else:
            road.gameDisplay.blit(self.imageM, (x, y))
            self.rotation = False
        pygame.display.update()
                
    def explosionCar(self, road, x, y, e=0):
        if   e == 0:
            road.gameDisplay.blit(self.exp1, (x+10, y-4))                
        elif e == 1:
            road.gameDisplay.blit(self.exp2, (x-15, y-58))
        elif e == 2:
            road.gameDisplay.blit(self.exp3, (x-40, y-94))          
        elif e == 3:
            road.gameDisplay.blit(self.exp4, (x-65, y-154))          
        pygame.display.update()  
        pygame.time.wait(150)

    def win(self, road):
        myfont = pygame.font.SysFont('Segoe UI', 100, True)
        text = myfont.render("You win!!!", True, (255,255,255))
        w, h = myfont.size("You win!!!")
        road.gameDisplay.blit(text, (((800 / 2) - (w / 2)), ((450 / 2) - (h / 2))))
        pygame.display.update()  
        pygame.time.wait(1000)
           

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

    def moveCoins(self, car, road):
        pos = [0, 4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48, 52]
        esc = [0.0714, 0.1428, 0.2142, 0.2857, 0.3571, 0.4285, 0.5, 0.5714, 0.6428, 0.7142, 0.7857, 0.8571, 0.9285, 1.0]
        if self.i == 0:
            self.firstPosition(road)
        if self.rand == 1:                        
            self.imageOriginal = pygame.image.load('images/coinL.png')
            self.x_coins -= pos[self.i] * 0.9       
        if self.rand == 2:
            self.imageOriginal = pygame.image.load('images/coinL.png')
            self.x_coins -= pos[self.i] * 0.2                  
        if self.rand == 3:
            self.imageOriginal = pygame.image.load('images/coinR.png')
            self.x_coins += pos[self.i] * 0.2
        if self.rand == 4:
            self.imageOriginal = pygame.image.load('images/coinR.png')
            self.x_coins += pos[self.i] * 0.9             

        self.size = list(self.imageOriginal.get_rect().size)
        self.image = pygame.transform.scale(self.imageOriginal, (int(self.size[0] * esc[self.i]), int(self.size[1] * esc[self.i]))) 
        self.y_coins += pos[self.i]
        self.i += 1
        
        if self.i == 13:
            reachOrMiss(car, self)
        if self.i == 14:
            self.firstPosition(road)                        
            self.i = 0

    def displayCoins(self, x, y, road):
        if self.i == 0:
            pass        
        else:
            road.gameDisplay.blit(self.image, (x, y))


def reachOrMiss(car, coins):   
    if car.x <= coins.x_coins and car.x + 120 >= coins.x_coins + 34:
        car.reached += 1
        car.reachedBool = True
        print("reached", car.reached)
    else:
        car.missed += 1
        print("missed", car.missed)

 
def crash(car, road):
    if car.x < road.width * 0.1 or car.x > (road.width * 0.9) - 120:
        car.crashed = True
    else:
        car.crashed = False


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
    if background == 4:
        road.gameDisplay.blit(road.backGround4, (0, 0))

    coins.displayCoins(coins.x_coins, coins.y_coins, road)
    car.displayCar(car.x, car.y, road)
    displayScore(car, road, record)


def displayScore(car, road, record):
    myfont = pygame.font.SysFont('Segoe UI', 20)
    myfont_bold = pygame.font.SysFont('Segoe UI', 20, True)

    text_score = myfont.render('SCORE: ', True, (255,255,255))
    road.gameDisplay.blit(text_score, (45, 440))

    text_score_number = myfont.render(str(car.reached), True, (255,255,255))
    road.gameDisplay.blit(text_score_number, (120, 440))

    text_highest = myfont.render('HIGHEST SCORE: ', True, (255,255,255))
    road.gameDisplay.blit(text_highest, (190, 440))

    text_highest_number = myfont_bold.render(str(record), True, (255,255,255))
    road.gameDisplay.blit(text_highest_number, (350, 440))

    
def startGame(car, coins, road, nn):
    preState = nn.get_state(car, coins, road)
    action = [0, 1, 0]
    car.moveCar(action, car.x, car.y, coins, road)
    coins.moveCoins(car, road)
    posState = nn.get_state(car, coins, road)
    reward1 = nn.set_reward(car)
    nn.remember(preState, action, reward1, posState, car.crashed)
    nn.replay_new(nn.memory)

def stopGame():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            break

def run():
    pygame.init()
    nn = deep_QNetwork()
    countGames = 0    
    record = 0
    backG = 1
    listReaches = []
    listMisses = []
    var = 0
    while countGames < 200:
        
        print("GAME " + str(countGames))
        road = Road(800, 450)

        myCar = road.car
        myCoins = road.coins  
      
        startGame(myCar, myCoins, road, nn)
        display(myCar, myCoins, road, record, backG)

        while (myCar.reached + myCar.missed) < 50:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    break
      
            oldState = nn.get_state(myCar, myCoins, road)
            nn.epsilon = 90 - var
            if randint(0, 100) <= nn.epsilon:
                final_move = to_categorical(randint(0, 2), num_classes=3)
            else:
                prediction = nn.model.predict(oldState.reshape((1, nn.dimInput)))
                final_move = to_categorical(np.argmax(prediction[0]), num_classes=3)  
  
            myCar.moveCar(final_move, myCar.x, myCar.y, myCoins, road)
            myCoins.moveCoins(myCar, road)
           
            newState = nn.get_state(myCar, myCoins, road)
            reward = nn.set_reward(myCar)
            nn.train_short_memory(oldState, final_move, reward, newState, myCar.crashed)
            nn.remember(oldState, final_move, reward, newState, myCar.crashed)

            record = getRecord(myCar.reached, record)

            display(myCar, myCoins, road, record, backG)   
       
            pygame.time.wait(speed)

            backG += 1
            if backG == 5:
                backG = 1
        if var < 80:
            var += 1
        listReaches.append(myCar.reached)
        listMisses.append(myCar.missed)
        if myCar.reached <= myCar.missed:        
            for j in range(4):
                myCar.explosionCar(road, myCar.x, myCar.y, j)
        if myCar.reached > myCar.missed:
            myCar.win(road)
  
        nn.replay_new(nn.memory)
        countGames += 1

    print(listReaches)
    print(listMisses)
    plt.plot(listReaches)
    plt.plot(listMisses)
    plt.show()
    nn.model.save_weights('weights.hdf5')

run()

