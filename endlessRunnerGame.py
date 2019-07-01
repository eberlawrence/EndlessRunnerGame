'''
Eber Lawrence Souza Gouveia
Federal University of Uberlandia - UFU
Biomedical Engineering Lab - BioLab

To do:
Create the coins and box asynchronously
One or more coins and box per time

'''
import pygame
from random import randint
import numpy as np
from keras.utils import to_categorical
import matplotlib.pyplot as plt
import seaborn as sns
from reinforcementLearning import deep_QNetwork

speed = 1

class Road:
    pygame.display.set_caption('Endless Runner Game 1.0')

    def __init__(self, width, height):
        self.width = width
        self.height = width
        self.coins = Coins(self)
        self.car = Car(self)
        self.box = Box(self)
        
        
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
        self.coins = 1
        self.reached = False
        self.stumbled = False
        self.crashed = False
        self.rotation = False
        self.change = 0
        
    def moveCar(self, move, x, y, coins, box, road):

        if self.reached:
            self.reached = False
        if self.stumbled:
            self.stumbled = False


        if np.array_equal(move, [1, 0, 0]):
            self.change = 0

        elif np.array_equal(move, [0, 1, 0]):
            self.change = 20

        elif np.array_equal(move, [0, 0, 1]):
            self.change = -20

        self.x = x + self.change
        

        reachOrCrash(self, coins, box, road)


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
            crashed = False
                
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

        if self.i == 14:
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
        pos = [0, 4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48, 52]
        esc = [0.0714, 0.1428, 0.2142, 0.2857, 0.3571, 0.4285, 0.5, 0.5714, 0.6428, 0.7142, 0.7857, 0.8571, 0.9285, 1.0]
        if self.i == 0:
            self.firstPosition(road)
        if self.rand == 1:                        
            self.imageOriginal = pygame.image.load('images/boxLL.png')
            self.x_box -= pos[self.i] * 0.9       
        if self.rand == 2:
            self.imageOriginal = pygame.image.load('images/boxL.png')
            self.x_box -= pos[self.i] * 0.2                  
        if self.rand == 3:
            self.imageOriginal = pygame.image.load('images/boxRR.png')
            self.x_box += pos[self.i] * 0.2
        if self.rand == 4:
            self.imageOriginal = pygame.image.load('images/boxR.png')
            self.x_box += pos[self.i] * 0.9             

        self.size = list(self.imageOriginal.get_rect().size)
        self.image = pygame.transform.scale(self.imageOriginal, (int(self.size[0] * esc[self.i]), int(self.size[1] * esc[self.i]))) 
        self.y_box += pos[self.i]
        self.i += 1

        if self.i == 14:
            self.firstPosition(road)                        
            self.i = 0

    def displayBox(self, x, y, road):
        if self.i == 0:
            pass        
        else:
            road.gameDisplay.blit(self.image, (x, y))


def reachOrCrash(car, coins, box, road):

    if car.x < road.width * 0.1 or car.x > (road.width * 0.9) - 120:
        car.crashed = True
    if car.x <= box.x_box and car.x + 120 >= box.x_box + 34 and car.y >= box.y_box and car.y <= box.y_box + 40:
        car.stumbled = True   
    if car.x <= coins.x_coins and car.x + 120 >= coins.x_coins + 34 and car.y >= coins.y_coins and car.y <= coins.y_coins + 40:
        car.reached = True
        car.coins = car.coins + 1


def getRecord(score, record):
        if score >= record:
            return score
        else:
            return record


def display(car, coins, box, road, record, background=1, count=0):
    if background == 1:
        road.gameDisplay.blit(road.backGround1, (0, 0))
    if background == 2:
        road.gameDisplay.blit(road.backGround2, (0, 0))
    if background == 3:
        road.gameDisplay.blit(road.backGround3, (0, 0))
    if background == 4:
        road.gameDisplay.blit(road.backGround4, (0, 0))
    if count > 0:
        box.displayBox(box.x_box, box.y_box, road)
    coins.displayCoins(coins.x_coins, coins.y_coins, road)
    car.displayCar(car.x, car.y, car.coins, road)

    myfont = pygame.font.SysFont('Segoe UI', 20)
    myfont_bold = pygame.font.SysFont('Segoe UI', 20, True)
    text_score = myfont.render('SCORE: ', True, (255,255,255))
    text_score_number = myfont.render(str(car.coins), True, (255,255,255))
    text_highest = myfont.render('HIGHEST SCORE: ', True, (255,255,255))
    text_highest_number = myfont_bold.render(str(record), True, (255,255,255))
    road.gameDisplay.blit(text_score, (45, 440))
    road.gameDisplay.blit(text_score_number, (120, 440))
    road.gameDisplay.blit(text_highest, (190, 440))
    road.gameDisplay.blit(text_highest_number, (350, 440))

def startGame(car, coins, box, road, nn):
    preState = nn.get_state(car, coins, box, road)
    action = [0, 1, 0]
    car.moveCar(action, car.x, car.y, coins, box, road)
    coins.moveCoins(road)
    box.moveBox(road)
    posState = nn.get_state(car, coins, box, road)
    reward1 = nn.set_reward(car)
    nn.remember(preState, action, reward1, posState, car.crashed)
    nn.replay_new(nn.memory)


def run():
    pygame.init()
    nn = deep_QNetwork()
    countGames = 0    
    
    record = 0
    backG = 1
    while countGames < 50:
        count = 0
        print("GAME " + str(countGames))
        road = Road(800, 450)
        myCar = road.car
        myCoins = road.coins
        myBox = road.box        
        startGame(myCar, myCoins, myBox, road, nn)
        display(myCar, myCoins, myBox, road, record, backG, count)
        while not myCar.crashed:           
            nn.epsilon = 80 - countGames           
            state_old = nn.get_state(myCar, myCoins, myBox, road)
            
            if randint(0, 200) < nn.epsilon:
                final_move = to_categorical(randint(0, 2), num_classes=3)
            else:
                prediction = nn.model.predict(state_old.reshape((1, nn.dimInput)))
                final_move = to_categorical(np.argmax(prediction[0]), num_classes=3)    
            myCar.moveCar(final_move, myCar.x, myCar.y, myCoins, myBox, road)
            myCoins.moveCoins(road)
            if count > 0:            
                myBox.moveBox(road)
            state_new = nn.get_state(myCar, myCoins, myBox, road)
            reward = nn.set_reward(myCar)
            nn.train_short_memory(state_old, final_move, reward, state_new, myCar.crashed)
            nn.remember(state_old, final_move, reward, state_new, myCar.crashed)
            record = getRecord(myCar.coins, record)
            #if myCar.reached:
               # print("Ganhou ponto")
            #if myCar.stumbled:
                #print("Perdeu ponto")
            display(myCar, myCoins, myBox, road, record, backG, count)
            pygame.time.wait(speed)
            backG += 1
            count += 1
            if backG == 5:
                backG = 1
        for j in range(4):
            myCar.explosionCar(road, myCar.x, myCar.y, j)
        nn.replay_new(nn.memory)
        countGames += 1
    nn.model.save_weights('weights.hdf5')

run()

