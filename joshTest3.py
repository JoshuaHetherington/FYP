from flat_game import carmunkExperiment3
import numpy as np
import random
import csv
import os.path
import timeit
import sys

GAMMA = 0.9 
ALPHA = 0.1

#method for printing position of agent in cell map 
def printCellMap(game_state):
    cellList = game_state.cellList
    for r in range(9):
        for c in range(10):
            if (cellList[r][c].current):
                print(" 1 ", end='')
            else:
                print(" 0 ", end='')
        print()
    print()

#method for printing parameters
def writeValuesToActionMap(fileObj, action, maxQ, currentQ, newQ, reward):
    fileObj.write("[ N , E , S , W ]\n")
    fileObj.write("Action: " + str(action) + " MaxQ: " + str(maxQ) + " CurrentQ: " + str(currentQ) + " NewQ: " + str(newQ) + " Reward: " + str(reward) + "\n")
    fileObj.write("----------------------------------------------------------------------------\n")

#method for printing the action values from the cell map
def writeActionMap(game_state, fileObj):
    cellList = game_state.cellList
    for r in range(9):
        for c in range(10):
            fileObj.write("[")
            for a in range(4):
                actionValue = "{:.2f}".format(cellList[r][c].actions[a])
                fileObj.write(actionValue + " ")
            if(cellList[r][c].current):
                fileObj.write("Pos(" + str(r) + "," + str(c) + ")")
            fileObj.write("]")
        fileObj.write("\n")
    fileObj.write("----------------------------------------------------------------------------\n")

#method for writing episodes and number fo steps to csv file
def writeCSVFile(game_state, fileObj, episode):
    fileObj.write(str(episode) + "," + str(game_state.num_steps) + "\n")

#method for choosing which action to take
def choose_Action(epsilon, game_state):
    rand = random.random()
    #get the row and column of the agents current position
    for i in range(10):
            for j in range(9):
                if(game_state.cellList[j][i].current):
                    row = j
                    column = i

    #based on the epsilon and random number generated, we will choose a random action
    if (rand < epsilon):
        action = np.random.randint(0, 4)
    else:
        # Get Q values for each action.
        count = 0
        cellActions = game_state.cellList[row][column].actions
        maxQ = cellActions[0]
        action = 0
        for a in range(4):
            if(maxQ < cellActions[a]):
                maxQ = cellActions[a]
                action = a

        for m in range(4):
            if(maxQ == cellActions[m]):
                count = count + 1

        if(count > 1):
            r = np.random.randint(0, count)
            ran = 0
            for i in range(4):
                if(cellActions[i] == maxQ):
                    if(r == ran):
                       action = i
                    ran = ran + 1

    return action, row, column

def learn():

    observe = 1000 # Number of frames to observe before reducing epsilon.
    epsilon = 0.1
    episodes = 10000 # Number of frames to play.

    # Just stuff used below.
    max_car_distance = 0
    car_distance = 0
    e = 0

    totalReward = 0.0
    fileObj = open("experiment4.csv", "w")

    # Create a new game instance.
    game_state = carmunkExperiment3.GameState()

    # Run the frames.
    while e < episodes:

        e += 1
        reward = 0.0
        game_state.num_steps = 0
        gameFinished = False
        
        while gameFinished == False:
             row = 0
             column = 0
       
             # Choose an action.
             action, row, column = choose_Action(epsilon, game_state)
             currentQ = game_state.cellList[row][column].actions[action]


             reward = game_state.frame_step(action)

             for r in range(9):
                 for c in range(10):
                     if(game_state.cellList[r][c].current):
                         currentCell = game_state.cellList[r][c]

             #get the MaxQ value
             maxQ = currentCell.actions[0]
             for i in range(4):
                  if(currentCell.actions[i] > maxQ):
                       maxQ = currentCell.actions[i]

             newQ = currentQ + (ALPHA *(reward +(GAMMA * maxQ) - currentQ))

             game_state.cellList[row][column].actions[action] = newQ
             
             #reset agent to start position when finish line is reached
             if(currentCell.end):
                 currentCell.current = False
                 game_state.cellList[2][0].current = True
                 gameFinished = True
             
        #end while
        # Decrement epsilon over time.
        if (e % observe == 0):
             epsilon -= 0.01
        
        writeCSVFile(game_state, fileObj, e)
    #end while
    #writeActionMap(game_state, fileObj)
    #print("Finished")
    fileObj.close()
    

if __name__ == "__main__":
    learn()
