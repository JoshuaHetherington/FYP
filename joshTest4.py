from flat_game import carmunkExperiment4
import numpy as np
import random
import csv
import os.path
import timeit
import sys

GAMMA = 0.9  
ALPHA = 0.1

#method for writing episodes and number fo steps to csv file
def writeCSVFile(game_state, fileObj, episode):
    fileObj.write(str(episode) + "," + str(game_state.num_steps) + "\n")

#method to find the current state of the agent
def getCurrentState(game_state):
    currentState = game_state.stateList[0]
    for i in range(len(game_state.stateList)):
         if(game_state.car_body.position == game_state.stateList[i]):
             currentState = game_state.stateList[i]
    return currentState

#method for choosing which action to take
def choose_Action(epsilon, game_state):
    
    rand = random.random()
    #based on the epsilon and random number generated, we will choose a random action
    if (rand < epsilon):
        action = np.random.randint(0, 3)  

    else:
        # Get Q values for each action.
        count = 0
        currentState = getCurrentState(game_state)
        maxQ = currentState.actionValues[0]
        action = 0

        for a in range(3):
            if(currentState.actionValues[a] > maxQ):
               maxQ = currentState.actionValues[a]
               action = a
            if(currentState.actionValues[a] == maxQ):
               count += 1

        if(count > 1):
            r = np.random.randint(0, count)
            ran = 0
            for b in range(3):
                if(currentState.actionValues[b] == maxQ):
                    if(r == ran):
                       action = b
                    ran = ran + 1
           
    return action

def learn():

    observe = 1000 # Number of frames to observe before reducing epsilon.
    epsilon = 0.1
    episodes = 1 # Number of frames to play.

    # Just stuff used below.
    max_car_distance = 0
    car_distance = 0
    e = 0

    totalReward = 0.0
    fileObj = open("experiment4.csv", "w")

    # Create a new game instance.
    game_state = carmunkExperiment4.GameState()

    # Get initial state by doing nothing and getting the state.
    r, s = game_state.frame_step((3))
    

    # Run the frames.
    while e < episodes:

        e += 1
        reward = 0.0
        game_state.num_steps = 0
        gameFinished = False
        
        while gameFinished == False:
       
             # Choose an action.
             action = choose_Action(epsilon, game_state)

             #get the currentQ from the states action value based on the chosen action (Before Move)
             currentState = getCurrentState(game_state)
             currentQ = currentState.actionValues[action]

             #Move made, state will change
             reward, newState = game_state.frame_step(action)

             #get the MaxQ value from the current States action Values (After a move)
             maxQ = newState.actionValues[0]
             for a in range(3):
                 if(newState.actionValues[a] > maxQ):
                      maxQ = newState.actionValues[a]

             newQ = currentQ + (ALPHA *(reward +(GAMMA * maxQ) - currentQ))

             #change the action value of the chosen action from the old state to the newQ value
             currentState.actionValues[action] = newQ
             
             if(reward == 1.0):
                 gameFinished = True
             
        #end while
        # Decrement epsilon over time.
        if (e % observe == 0):
             epsilon -= 0.01
        
        #writeCSVFile(game_state, fileObj, e)
    #end while
    #print("Finished")
    fileObj.close()
    

if __name__ == "__main__":
    learn()
