# Lab1: Program a rat that moves randomly while avoiding walls
# The standard how we choose next square to visit:
# We move on a square not visited yet
# If impossible, we move at random
# Copyright: Xi SONG 05/09/2019

###############################
# When the player is performing a move, it actually sends a character to the main program
# The four possibilities are defined here
MOVE_DOWN = 'D'
MOVE_LEFT = 'L'
MOVE_RIGHT = 'R'
MOVE_UP = 'U'
# Create a map for the calculation of next location
DIRECTION_TO_CALCULATION = {
    MOVE_DOWN: (0, -1), 
    MOVE_LEFT: (-1, 0), 
    MOVE_RIGHT: (1, 0), 
    MOVE_UP: (0, 1)
    }

###############################
# Please put your imports here
import random
import numpy

###############################
# Globla variable 
# A set remebers all the cell that have been visited
cellVisited = set()

# Calculate the direction according to player location and next location
def calMove(playerLocation, nextLocation):
    move_vector = tuple(numpy.subtract(nextLocation, playerLocation))
    for MOVE in DIRECTION_TO_CALCULATION:
        if move_vector == DIRECTION_TO_CALCULATION[MOVE]:
            return MOVE

def randomVisite(playerLocation, mazeMap):
    possibilities = list(mazeMap[playerLocation].keys())
    return calMove(playerLocation, random.choice(possibilities))

# Choose next location according to two principals
def chooseNextLocation(playerLocation, mazeMap):
    for nextPossibleLocation in mazeMap[playerLocation]:
        if nextPossibleLocation not in cellVisited:
            return calMove(playerLocation, nextPossibleLocation)
    return randomVisite(playerLocation, mazeMap)

###############################
# Preprocessing function
# The preprocessing function is called at the start of a game
# It can be used to perform intensive computations that can be
# used later to move the player in the maze.
###############################
# Arguments are:
# mazeMap : dict(pair(int, int), dict(pair(int, int), int))
# mazeWidth : int
# mazeHeight : int
# playerLocation : pair(int, int)
# opponentLocation : pair(int,int)
# piecesOfCheese : list(pair(int, int))
# timeAllowed : float
###############################
# This function is not expected to return anything
def preprocessing(mazeMap, mazeWidth, mazeHeight, playerLocation, opponentLocation, piecesOfCheese, timeAllowed):
    pass

###############################
# Turn function
# The turn function is called each time the game is waiting
# for the player to make a decision (a move).
###############################
# Arguments are:
# mazeMap : dict(pair(int, int), dict(pair(int, int), int))
# mazeWidth : int
# mazeHeight : int
# playerLocation : pair(int, int)
# opponentLocation : pair(int, int)
# playerScore : float
# opponentScore : float
# piecesOfCheese : list(pair(int, int))
# timeAllowed : float
###############################
# This function is expected to return a move
def turn(mazeMap, mazeWidth, mazeHeight, playerLocation, opponentLocation, playerScore, opponentScore, piecesOfCheese, timeAllowed):
    cellVisited.add(playerLocation)
    return chooseNextLocation(playerLocation, mazeMap)
