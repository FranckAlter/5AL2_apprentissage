from neutreeko import utils

class Environment:
    def __init__(self):
        self.__states = utils.get_all_states()
        self.__start = (((0, 1), (0, 3), (4, 2)), ((1, 2), (4, 1), (4, 3)))






    def apply(self, agent, action):
        state = agent.state
        if action == UP:
            new_state = (state[0] - 1, state[1])
        elif action == DOWN:
            new_state = (state[0] + 1, state[1])
        elif action == LEFT:
            new_state = (state[0], state[1] - 1)
        elif action == RIGHT:
            new_state = (state[0], state[1] + 1)
        else:
            raise Exception('Unknown action')

        if new_state in self.__states:
            state = new_state
            if new_state == self.__goal:
                reward = REWARD_GOAL
            elif self.__states[new_state] in [MAZE_BORDER, MAZE_START]:
                reward = REWARD_BORDER
            else:
                reward = REWARD_EMPTY
        else:
            reward = REWARD_OUT

        agent.update(state, action, reward)

        return reward

    @property
    def start(self):
        return self.__start

    @property
    def goal(self):
        return self.__goal

    @property
    def states(self):
        return self.__states.keys()