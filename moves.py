from math import floor, sqrt
import random 
from math import floor
import random
from tracemalloc import start 
import numpy as np
from pyparsing import col
from boardproperties import boardpostionscenter,boardpostions
import time
import pyautogui
import collections

# Prints with spaces :(
def print2nd(array, arraysize):
    for x in range(arraysize):
       for y in range(arraysize):
        print(array[x][y])

def getLegalMoves(board, size):
    # Create a board to insert legal moves into
    # A 1 is an illegal move, and 0 is legal
    # First assume all moves to be illegal.
    movesboard = []
    legalmovesarray = []
    for i in range (size):
        movesboard.insert(i, [1]*size)

    # Then, find the blank space.
    for i in range (size):
        for x in range (size):
            if board[i][x] == 0:
                blankX = i
                blankY = x

    # Finally, iterate through the blank's row and col and make the moves all legal.
    for i in range (size):
        movesboard[blankX][i] = 0
        movesboard[i][blankY] = 0
    
    # You cannot click on the blank space.
    movesboard[blankX][blankY] = 2
    #Parse legal moves into 1d array
    for i in range(size*size):
        if movesboard[floor(i/size)][i%size] == 0:
            legalmovesarray.append(i)
    legalmovesarray = np.asarray(legalmovesarray)
    movesboard = np.array(movesboard)

    return legalmovesarray, movesboard
# def MakeMoves(boardarry, size, action, movesboard):
#     # find the position of the blank tile
#     for i in range(size):
#         for j in range(size):
#             if movesboard[i][j] == 2:
#                 BlankYpos = i
#                 BlankXpos = j
#                 break
    
#     # create the bufferboard
#     bufferboard = [['-']*size for _ in range(size)]
    
#     # update the bufferboard and boardarry
#     if BlankYpos == action // size:
#         bufferboard[BlankYpos][action % size] = 0
#         for i in range(BlankXpos, action % size):
#             bufferboard[BlankYpos][i+1] = boardarry[BlankYpos][i]
#         for i in range(BlankXpos, action % size, -1):
#             bufferboard[BlankYpos][i-1] = boardarry[BlankYpos][i]
#         for i in range(size*size-1):
#             if bufferboard[BlankYpos][i % size] != '-':
#                 boardarry[BlankYpos][i % size] = bufferboard[BlankYpos][i % size]
#     elif BlankXpos == action % size:
#         bufferboard[action // size][BlankXpos] = 0
#         for i in range(BlankYpos, action // size):
#             bufferboard[i+1][BlankXpos] = boardarry[i][BlankXpos]
#         for i in range(BlankYpos, action // size, -1):
#             bufferboard[i-1][BlankXpos] = boardarry[i][BlankXpos]
#         for i in range(size*size-1):
#             if bufferboard[i // size][BlankXpos] != '-':

def MakeMoves(boardarry, size, action, movesboard):
    blankposition = np.argwhere(np.array(movesboard) == 2)
    BlankYpos = blankposition[0][0]
    BlankXpos = blankposition[0][1]
    bufferboard = []
    for i in range (size):
        bufferboard.insert(i, ['-']*size)
    if(floor(action/size) == (BlankYpos)):
        bufferboard[floor(action/size)][action%size] = 0
        for i in range(BlankXpos-(action%size)):
            bufferboard[floor(action/size)][(action%size)+i+1] = boardarry[floor(action/size)][(action%size)+i]
            ...
        for i in range((action%size)-BlankXpos):
            bufferboard[floor(action/size)][(action%size)-i-1] = boardarry[floor(action/size)][(action%size)-i]
            ...
        for i in range((size*size)-1):
            if bufferboard[BlankYpos][i%size] != '-':
                boardarry[BlankYpos][i%size] = bufferboard[BlankYpos][i%size]
            ...
    elif((action % size) == BlankXpos):
        bufferboard[floor(action/size)][action%size] = 0
        for i in range(BlankYpos-(floor(action/size))):
            bufferboard[floor(action/size)+i+1][(action%size)] = boardarry[floor(action/size)+i][(action%size)]
            ...
        for i in range((floor(action/size))-BlankYpos):
            bufferboard[floor(action/size)-i-1][(action%size)] = boardarry[floor(action/size)-i][(action%size)]
            ...
        for i in range((size*size)-1):
            if bufferboard[floor(i/size)][BlankXpos] != '-':
                boardarry[floor(i/size)][BlankXpos] = bufferboard[floor(i/size)][BlankXpos]
            ...
    # time.sleep(0.1)
    # pyautogui.click(boardpostionscenter[f"x{action+1}"],boardpostionscenter[f"y{action+1}"])
    # print(f'Clicked slot: {action+1}')
    
    
def CreateRandomBoard(level):
    starttime = time.time()
    numbers = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 0]])
    for i in range(level):
        legalmoves, movesarray = getLegalMoves(numbers, int(sqrt(numbers.size)))
        intnum = random.randint(0,3)
        MakeMoves(numbers, int(sqrt(numbers.size)), legalmoves[intnum], movesarray)
    # while numbers[2][2] != 0:
    #     legalmoves, movesarray = getLegalMoves(numbers, int(sqrt(numbers.size)))
    #     intnum = random.randint(0,3)
    #     MakeMoves(numbers, int(sqrt(numbers.size)), legalmoves[intnum], movesarray)
    stoptime = time.time()
    # print(f"Time elapsed: {stoptime-starttime}")
    # print(f"The new working board i hope {numbers}")
    return numbers

def AreArraysEqual(currnt, desired):
    # input("move on")
    # print(currnt)
    # print(desired)
    # print(list(currnt) == list(desired.flatten()))
    if(list(currnt) == list(desired.flatten())):
        return True
    else:
        return False
    for i in range(9):
        if currnt[floor(i/3)][i%3] != desired[floor(i/3)][i%3]:
            return False
    return True

# def CalucateReward(current, desired, PreviousReward, moved):
def CalucateReward(current, desired):
    reward = 0
    for i in range(9):
        if current[floor(i/3)][i%3] == desired[floor(i/3)][i%3]:
            reward = reward + 1
        
        # else:
        #     place = np.argwhere(np.array(current) == i+1)
        #     correctplace = np.argwhere(np.array(desired) == i+1)
        #     correctplaceX = correctplace[0][0]
        #     correctplaceY = correctplace[0][1]
        #     placeX = place[0][0]
        #     placeY = place[0][1]
        #     size = sqrt(current.size)
            
        #     if placeX >= correctplaceX:
        #         distanceX = placeX-correctplaceX
        #     else:
        #         distanceX = correctplaceX - placeX
            
        #     if placeY >= correctplaceY:
        #         distanceY = placeY - correctplaceY
        #     else:
        #         distanceY = correctplaceY - placeY
            
        #     reward = i-((distanceX*(1/(size+size))+distanceY*(1/(size+size))))
        #     reward = float(reward)
                
                
            
        #     print(f'REWARD: {reward}')
        #     return reward
    return reward
    
def parseboard(tiles , board):
    currentboard = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
    for i in range(len(tiles)):
        for l in range(8):
            if board['x'+str(i+1)]-20 <= tiles[l][0] <= board['x'+str(i+1)]+20 and (board['y'+str(i+1)])-20 <= tiles[l][1] <= (board['y'+str(i+1)])+20:
                print(str(l+1) + " is in tile " + str(i+1))
                currentboard[floor(i/3)][i%3] = l + 1
    return currentboard

def getboardfromscreen():
  try:
      x1 , y1 , w ,h = pyautogui.locateOnScreen('./img/Screenshot 2022-09-26 203221.png' , confidence=0.9)
      x2 , y2 , w ,h = pyautogui.locateOnScreen('./img/Screenshot 2022-09-26 203302.png' , confidence=0.9)
      x3 , y3 , w ,h = pyautogui.locateOnScreen('./img/Screenshot 2022-09-26 203323.png' , confidence=0.9)
      x4 , y4 , w ,h = pyautogui.locateOnScreen('./img/Screenshot 2022-09-26 203336.png' , confidence=0.9)
      x5 , y5 , w ,h = pyautogui.locateOnScreen('./img/Screenshot 2022-09-26 203354.png' , confidence=0.9)
      x6 , y6 , w ,h = pyautogui.locateOnScreen('./img/Screenshot 2022-09-26 203414.png' , confidence=0.9)
      x7 , y7 , w ,h = pyautogui.locateOnScreen('./img/Screenshot 2022-09-26 203426.png' , confidence=0.9)
      x8 , y8 , w ,h = pyautogui.locateOnScreen('./img/Screenshot 2022-09-26 203443.png' , confidence=0.9)
      tiles = [[x1,y1],[x2,y2],[x3,y3],[x4,y4],[x5,y5],[x6,y6],[x7,y7],[x8,y8]]
      return tiles
  except Exception as e:
    print(e)        

def SolveBoard(currentboard, desiredboard):
    queue = collections.deque([str(currentboard)])
    seen = set()
    seen.add(queue[0])
    size = int(sqrt(currentboard.size))
    bufferarray = []
    node = str(currentboard)
    while queue:
        print(node)
        queue = collections.deque(sorted(list(queue), key=lambda node: node.f))
        node = queue.popleft()
        if AreArraysEqual(currentboard, desiredboard):
            return node.path

        for move, action in node.actions:
            legalmovesarray, movesboard = getLegalMoves(currentboard, int(sqrt(currentboard.size)))
            MakeMoves(currentboard,int(sqrt(currentboard.size)), legalmovesarray[action], movesboard )
            child = currentboard

            if child not in seen:
                queue.appendleft(child)
                seen.add(child)
        
