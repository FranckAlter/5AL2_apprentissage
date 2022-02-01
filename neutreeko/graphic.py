import pygame
import time

from neutreeko.utils import move

surf = pygame.display.set_mode((800,600))
GREEN = (152, 251, 152)
RED = (139, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
SCALE = 100
ACTION_SCALE = 50

active_player = ['black', 'white']
playersColor = {'black' : (BLACK, WHITE), 'white': (WHITE, BLACK) }

class Grid:
    def __init__(self, beginPos,  scale, nb_cases):
        self.beginPos = beginPos
        self.scale = scale
        self.nb_cases = nb_cases

    def draw (self, surf):
        for i in range(self.nb_cases + 1):
            pygame.draw.line(surf, BLACK, (self.beginPos[0], self.beginPos[1] + self.scale * i), (self.beginPos[0] +  self.nb_cases * self.scale, self.beginPos[1] + self.scale * i))
            pygame.draw.line(surf, BLACK, (self.beginPos[0] + self.scale * i, self.beginPos[1]), (self.beginPos[0] + self.scale * i, self.beginPos[1] +  self.nb_cases * self.scale))

    def is_in (self, pos):
        return pos[0]>self.beginPos[0] and pos[0]<self.beginPos[0]+self.nb_cases*self.scale and \
               pos[1]>self.beginPos[1] and pos[1]<self.beginPos[1]+self.nb_cases*self.scale

    def get_coordonate (self, pos):
        return (int((pos[0]-self.beginPos[0])/self.scale), int((pos[1]-self.beginPos[1])/self.scale))

    def get_coordonate_case (self, case):
        return (self.beginPos[0] + case[0]*self.scale, self.beginPos[1] + case[1]*self.scale)

    def color_case (self, surf, case):
        pygame.draw.rect(surf, RED, pygame.Rect(self.get_coordonate_case(case), (self.scale, self.scale )))

def drawToken (surf, pos_x, pos_y, color):
  pygame.draw.circle(surf, color, (pos_x*SCALE + SCALE/2, pos_y*SCALE + SCALE/2), SCALE * 0.4)

def drawState (surf, state, active_player):
    for i in range (2):
        for token in state[i]:
            drawToken (surf, token[0], token[1], playersColor[active_player][i])

def colorCase (surf, pos):
    print (str(pos[0]) + " " + str(pos[1]))

surf.fill(GREEN)
play_grid = Grid ((0, 0), SCALE, 5)
action_grid = Grid ((600, 0), ACTION_SCALE, 3)
play_grid.draw(surf)
action_grid.draw(surf)
start = (((1, 4), (3, 4), (2, 1)), ((2, 3), (1, 0), (3, 0)))
directions_offset = {'UP': (0, -1), 'DOWN': (0, 1), 'LEFT': (-1, 0), 'RIGHT' : (1, 0), 'UP_LEFT' : (-1,-1) , 'UP_RIGHT': (1,-1), 'DOWN_LEFT' : (-1,1) , 'DOWN_RIGHT': (1,1)}
directions_croix = {(1, 0) : 'UP', (1, 2) : 'DOWN'}
drawState (surf, start, 'black')
var = True
while var:
        pygame.display.update()
        events = pygame.event.get(pygame.MOUSEBUTTONUP)
        case_play = 0
        case_action = 0
        actual = start
        case_play_1 = None
        case_action_1 = None
        for event in events:
            pos = pygame.mouse.get_pos()

            if play_grid.is_in(pos):
                case_play = play_grid.get_coordonate(pos)
                case_play_1 = case_play
                play_grid.color_case(surf, play_grid.get_coordonate(pos))
                print (case_play_1)
                print (case_action_1)
            if action_grid.is_in(pos):
                case_action = action_grid.get_coordonate(pos)
                case_action_1 = case_action
                action_grid.color_case(surf, action_grid.get_coordonate(pos))
                print(case_play_1)
                print(case_action_1)

            if case_play_1 is not None and case_action_1 is not None:
                count = 0
                int_case = None
                for case in actual[0]:
                    if case == case_play:
                        int_case = count
                    count += 1
                print (int_case)
                print (directions_croix[case_action])
                actual = move(actual, int_case, directions_croix[case_action])
                print (actual)






