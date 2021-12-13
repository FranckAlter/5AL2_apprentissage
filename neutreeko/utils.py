from itertools import combinations

start = (((1, 0), (3, 0), (2, 3)), ((2, 1), (1, 4), (3, 4)))
directions_offset = {'UP': (0, 1), 'DOWN': (0, -1), 'LEFT': (-1, 0), 'RIGHT' : (1, 0), 'UP_LEFT' : (-1,1) , 'UP_RIGHT': (1,1), 'DOWN_LEFT' : (-1,-1) , 'DOWN_RIGHT': (1,-1)}

def get_all_states():
    cases = []
    for row in range(5):
        for col in range(5):
            cases.append((row, col))
    white = combinations(cases, 3)
    states = []
    for i in list(white):
        cases_restantes = set(cases).difference(set(i))
        black = combinations(cases_restantes, 3)
        for j in list(black):
            states.append((i, j))
        if is_victory((i, "toto")):
            print (i)
    return states

def is_victory (state):
    active_player = sorted(state[0])
    dx1 = active_player[1][0] - active_player[0][0]
    dx2 = active_player[2][0] - active_player[1][0]
    dy1 = active_player[1][1] - active_player[0][1]
    dy2 = active_player[2][1] - active_player[1][1]
    return dx1 == dx2 and dy1 == dy2  and dx1 < 2 and dx1 > -2 and dy1 < 2 and dy1 > -2

def move (state, jeton, direction):
    active_jeton = state[0][jeton]
    save_active_jeton = active_jeton
    memory_jeton = None
    condition = True
    while condition:
        posex = active_jeton[0] + directions_offset[direction][0]
        posey = active_jeton[1] + directions_offset[direction][1]
        active_jeton = (posex, posey)
        condition = isPositionValid (state, active_jeton)
        if condition:
            memory_jeton = active_jeton
    if memory_jeton is not None:
        state = (tuple(x for x in state[0] if x is not save_active_jeton) + (memory_jeton,), state[1])
        sorted(state[0])
    return state


def isPositionValid(state, position):
    posOK = position[0]>-1 and position[0] < 5 and position[1]>-1 and position[1] < 5
    return posOK and not (position in state[0] or position in state[1])

def game ():
    end_game = False
    players = ['black', 'white']
    active_player = players[0]
    state = start
    while (not end_game):
        print (state)
        print ("C'est au tour de : " + active_player)
        mouv_is_ok = False
        while (not mouv_is_ok):
            jeton = int(input("Quel jeton voulez-vous bouger?"))
            direction = input("Dans quelle direction?")
            new_state = move(state, jeton, direction)
            if (new_state == state):
                print ('mouvement impossible')
            else:
                print ('mouvement enregistré')
                mouv_is_ok = True
        victory = is_victory(new_state)
        if victory:
            print ("Fin du jeu, victoire de : " + active_player)
            end_game = True
        else:
            if active_player == players[0]:
                active_player = players[1]
            else:
                active_player = players[0]
            state = (new_state[1], new_state[0])






#get_all_states()
game()


