from keras.optimizers import Adam
from keras.models import Sequential
from keras.layers.core import Dense, Dropout
import random
import numpy as np
from operator import add


class deep_QNetwork(object):

    def __init__(self):
        self.dimInput = 5
        self.reward = 0
        self.gamma = 0.9
        self.short_memory = np.array([])
        self.agent_target = 1
        self.agent_predict = 0
        self.learning_rate = 0.0005
        self.model = self.network('weights.hdf5')
        #self.model = self.network()
        self.epsilon = 0
        self.actual = []
        self.memory = []


    def get_state(self, car, coins, road):

        state = [car.change == 0,
		 car.change == 40,
                 car.change == -40, 
                 coins.x_coins <= car.x or coins.x_coins <= car.x + 60, 
                 coins.x_coins >= car.x + 120 or coins.x_coins <= car.x + 60]

        for i in range(len(state)):
            if state[i]:
                state[i] = 1
            else:
                state[i] = 0
        
        self.dimInput = len(state)

        return np.asarray(state)

    def set_reward(self, car):
        self.reward = 0
        if car.crashed:
            self.reward = -5
            return self.reward       
        if car.reachedBool:
            self.reward = 10
        return self.reward

    def network(self, weights=None):
        model = Sequential()
        model.add(Dense(output_dim=120, activation='relu', input_dim=self.dimInput))
        model.add(Dropout(0.15))
        model.add(Dense(output_dim=120, activation='relu'))
        model.add(Dropout(0.15))
        model.add(Dense(output_dim=120, activation='relu'))
        model.add(Dropout(0.15))
        model.add(Dense(output_dim=3, activation='softmax'))
        opt = Adam(self.learning_rate)
        model.compile(loss='mse', optimizer=opt)

        if weights:
            model.load_weights(weights)
        return model

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def replay_new(self, memory):
        if len(memory) > 1000:
            minibatch = random.sample(memory, 1000)
        else:
            minibatch = memory
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                target = reward + self.gamma * np.amax(self.model.predict(np.array([next_state]))[0])
            target_f = self.model.predict(np.array([state]))
            target_f[0][np.argmax(action)] = target
            self.model.fit(np.array([state]), target_f, epochs=1, verbose=0)

    def train_short_memory(self, state, action, reward, next_state, done):
        target = reward
        if not done:
            target = reward + self.gamma * np.amax(self.model.predict(next_state.reshape((1, self.dimInput)))[0])
        target_f = self.model.predict(state.reshape((1, self.dimInput)))
        target_f[0][np.argmax(action)] = target
        self.model.fit(state.reshape((1, self.dimInput)), target_f, epochs=1, verbose=0)




