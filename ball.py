import fcntl
import termios
import struct
import pyautogui

import sys
from os import system
from time import sleep
from random import randint

if len(sys.argv) != 3:
    X_MAP = 10
    Y_MAP = 5
else:
    X_MAP = int(sys.argv[1])
    Y_MAP = int(sys.argv[2])

MAPPING = {0: " ", 1: "@", 2: "*", 3: "█"}

if "full" in sys.argv:
    Y_MAP, X_MAP = struct.unpack('hh', fcntl.ioctl(0, termios.TIOCGWINSZ, '1234'))
    # X_MAP-=1
    Y_MAP-=5

ugly = False

random_ball = [5, 2, 1]
move_right = True
move_up = True
rebound = 0

map = [[0 for x in range(X_MAP)] for y in range(Y_MAP)]

def place_on_map(map, place):
    """
    place = [\n
    X, Y | element\n
    [3,2,2],\n
    [1,1,1],\n
    . . .]
    """

    # Проходим по высоте карты. 
    # Если на n высоте есть элемент, 
    # добираемся до его позиции и вставляем его в карту
    # иначе ставим пустоту (это 0)

    for element in place:
        for y in range(Y_MAP):
            if y == element[1]:
                for x in range(X_MAP):
                    if x == element[0]:
                        map[y][x] = element[2]
                    else:
                        map[y][x] = 0
            # else:
            #     for x in range(X_MAP):
            #         map[y][x] = 0
    return map


def render(map):
    if ugly == False:
        # print("-" * X_MAP)
        for line in map:
            print("".join([MAPPING[place] for place in line]))
            # print("".join([MAPPING[place] for place in line]) + "|")
        # print("-" * X_MAP)
    else:
        for line in map:
            print(f"{line}\n")
    
    sleep(0.02)
    system('clear')

def randomize(rebound=rebound):
    if randint(0, 1) == 1:
        random_ball[1] += 1
    else:
        random_ball[0] += 1
    return rebound + 1

def get_cursor_position():
    x, y = pyautogui.position()
    try: cursor = [int(X_MAP/(pyautogui.size()[0]/x)+1), 
                   int(Y_MAP/(pyautogui.size()[1]/y)+1), 
                   3]
    except: cursor = [0, 0, 3]
    return cursor

while True:
    cursor = get_cursor_position()
    map = place_on_map(map, [cursor, random_ball])

    render(map)

    if move_right == True:
        if random_ball[0] < X_MAP-1:
            random_ball[0] += 1
        else:
            move_right = False
            # rebound = randomize(rebound)
    
    else:
        if random_ball[0] != 0:
            random_ball[0] -= 1
        else:
            move_right = True
            # rebound = randomize(rebound)

    if move_up == True:        
        if random_ball[1] < Y_MAP-1:
            random_ball[1] += 1
        else:
            move_up = False
            # rebound = randomize(rebound)
    else:
        if random_ball[1] != 0:
            random_ball[1] -= 1
        else:
            move_up = True
            # rebound = randomize(rebound)

    # print(f"Отскоков: {rebound}")
    # print(move_right)
    print(random_ball)
    # print(f"курсор в терминале: {cursor}")
    # print(f"карта: {X_MAP, Y_MAP}")