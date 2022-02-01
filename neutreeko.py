from neutreeko import utils
from random import *
import pickle
import time

REWARD_ILLEGAL = -1000
REWARD_LOSE = -100
REWARD_VICTORY = 100
REWARD_CONTINUE = -1

ACTIONS = []
for i in range(3):
    for j in utils.directions_offset.keys():
        ACTIONS.append((i, j))


class Environment:
    def __init__(self):
        self.__states = utils.get_all_states()
        self.__start = (((1, 4), (2, 1),(3, 4)), ((1, 0),(2, 3), (3, 0)))
        self.__goal = False

    def apply(self, agent, action):
        state = agent.state

        new_state = utils.move(state, action[0], action[1])
        # Le coup est valide
        if not new_state == state:
            state = new_state
            if utils.is_victory(state):
                reward = REWARD_VICTORY
                self.__goal = True
            else:
                reward = REWARD_CONTINUE

        else:
            reward = REWARD_ILLEGAL

        agent.update(action, state, reward)
        agent.switch()

        return reward

    @property
    def start(self):
        return self.__start

    @property
    def goal(self):
        return self.__goal

    @property
    def states(self):
        return self.__states

    def reset(self):
        self.__goal = False


class Agent:
    def __init__(self, environment):
        self.__environment = environment
        self.__qtable = {}
        self.__learning_rate = 1
        self.__discount_factor = 0.8
        for s in environment.states:
            self.__qtable[s] = {}
            for a in ACTIONS:
                self.__qtable[s][a] = 0
        self.__history = []
        self.__exploration = 1.0
        self.reset()

    def save(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump(self.__qtable, file)

    def load(self, filename):
        with open(filename, 'rb') as file:
            self.__qtable = pickle.load(file)

    def reset(self):
        self.__state = self.__environment.start
        self.__score = 0
        self.__last_action = None
        self.__environment.reset()

    def update_history(self):
        self.__history.append(self.__score)


    @property
    def history(self):
        return self.__history

    def switch(self):
        self.__state = utils.change_player(self.__state)

    def update(self, action, state, reward):
        # update q-table
        # Q(st, a) <- Q(st, a) + learning_rate *
        #                       [reward + discount_factor * max(qtable[st+1]) - Q(st, a)]
        maxQ = max(self.__qtable[state].values())
        self.__qtable[self.__state][action] += self.__learning_rate * \
                                               (reward + self.__discount_factor * \
                                                maxQ - self.__qtable[self.__state][action])

        self.__state = state
        self.__score += reward
        self.__last_action = action

    def best_action(self):
        rewards = self.__qtable[self.__state]
        best = None

        if random() < self.__exploration:
            best = choice(list(rewards.keys()))  # une action au hasard
            self.__exploration *= 0.9999
            #print(f"Exploration : {self.__exploration}")
        else:
            for a in rewards:
                if best is None or rewards[a] > rewards[best]:
                    best = a
        return best

    @property
    def exploration(self):
        return self.__exploration

    def do(self, action):
        self.__environment.apply(self, action)

    @property
    def state(self):
        return self.__state

    @property
    def score(self):
        return self.__score

    @property
    def qtable(self):
        return self.__qtable

    @property
    def environment(self):
        return self.__environment


if __name__ == '__main__':
    env = Environment()
    print(f"Q-table size : {len(env.states) * len(ACTIONS)}")

    agent = Agent(env)
    print("begin play")
    for i in range(1000):
        iteration = 0
        agent.reset()
        while not env.goal:
            iteration += 1
            action = agent.best_action()
            reward = env.apply(agent, action)
            #print(f"Main loop{iteration} {action} {agent.state} {reward}")
        print(i,agent.score, iteration, agent.exploration)