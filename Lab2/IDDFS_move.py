# Lab2: Implement BFS to get only one peace of cheese with the 
# implementation of queue structure. 
# ATTENTION: In a maze without mud -> An unweighted graph
# Copyright: Xi SONG 14/09/2019


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
import numpy as np

###############################
# Please put your global variables here
cellVisited = set()
# Calculate the direction according to player location and next location
def calMove(playerLocation, nextLocation):
    move_vector = tuple(np.subtract(nextLocation, playerLocation))
    for MOVE in DIRECTION_TO_CALCULATION:
        if move_vector == DIRECTION_TO_CALCULATION[MOVE]:
            return MOVE


def findShortestPath(routeTable, piecesOfCheese):
    """
    According to the route table, find the shortest path

    Parameters: routeTable -> route table
                piecesOfCheese -> the destination of this shortest path

    Return: A list filled with instructions from the beginning to the destination
    """
    instructions = {}
    currentVertex = piecesOfCheese[0]
    while routeTable[currentVertex] != None:
        move = calMove(routeTable[currentVertex], currentVertex)
        instructions[routeTable[currentVertex]] = move
        currentVertex = routeTable[currentVertex]

    return instructions


def InterativeDeepningDepthFirstSearch(mazeMap, currentVertex, lastLocation, piecesOfCheese):
    """
    Fill the route table using IDDFS
    Parameters: 
                mazeMap -> a unweighted directed graph
                currentVertex -> current coordinate
    Fonction: Fill the route table
    """
    for depth in range(len(mazeMap.keys())):
        routeTable = DepthLimitedSearch(depth, currentVertex, lastLocation, piecesOfCheese, mazeMap)
        if piecesOfCheese[0] in routeTable.keys():
            break
    return routeTable

def DepthLimitedSearch(depth, currentVertex, lastLocation, piecesOfCheese, mazeMap, routeTable = {}):
    """
    Applying DFS according to the limit of depth
    Parameters:
                depth -> the limit of depth
                currentVertex -> current location of DFS
                lastLocation -> last location of DFS
                piecesOfCheese -> Destination
                mazeMap -> unweighted directed graph
    Fonction: Fill the route table
    """
    cellVisited.add(currentVertex)
    routeTable[currentVertex] = lastLocation
    # cellVisited.add(currentVertex)
    if depth == 0 and currentVertex == piecesOfCheese[0]:
        routeTable[currentVertex] = lastLocation
        return routeTable
    elif depth > 0:
        for neighbor in mazeMap[currentVertex]:
            if neighbor not in cellVisited:
                DepthLimitedSearch(depth - 1, neighbor, currentVertex, piecesOfCheese, mazeMap, routeTable)
            if piecesOfCheese[0] in routeTable.keys():
                return routeTable
    # print(routeTable)
    cellVisited.remove(currentVertex)
    del routeTable[currentVertex]
    return routeTable

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
    routeTable = InterativeDeepningDepthFirstSearch(mazeMap, playerLocation, None, piecesOfCheese)
    # print(routeTable)
    ins = findShortestPath(routeTable, piecesOfCheese)
    with open("instructions.txt", 'w') as f:    # Use instructions.txt to save the prepared path
        for key in ins:
            line = str(key) + ':' + str(ins[key]) + '\n'
            f.write(line)

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
    instructions = {}
    with open("instructions.txt") as f:
        for line in f.readlines():
            strip = line.split(':')
            instructions[strip[0]] = strip[1][0]

    return instructions[str(playerLocation)]