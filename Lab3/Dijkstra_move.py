# Lab3: Implement Dijkstra's algorithm to get only one peace of cheese 
# using priority queue (heapq). 
# Copyright: Xi SONG 24/09/2019


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
import heapq
import numpy as np

###############################
# Please put your global variables here
ins = {}

class VertexDistance:
    """
    A class created to simpolify the utilization of heapq.heappush()
    """

    def __init__(self, currentVertex, lastVertex, distance):
        """
        Generate a new instance to be stored in priority queue
        """
        self.__vertex = currentVertex
        self.__father = lastVertex
        self.__distance = distance
    
    def __lt__(self, anotherVertexDistance):
        return self.__distance < anotherVertexDistance.distance()

    def __str__(self):
        return str(self.vertex()) + ", " + str(self.distance())

    def distance(self):
        return self.__distance
    
    def vertex(self):
        return self.__vertex

    def father(self):
        return self.__father


def calMove(playerLocation, nextLocation):
    """
    Calculate the direction according to player location and next location
    """
    move_vector = tuple(np.subtract(nextLocation, playerLocation))
    for MOVE in DIRECTION_TO_CALCULATION:
        if move_vector == DIRECTION_TO_CALCULATION[MOVE]:
            return MOVE
    return "Not right"


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

def dijkstra(mazeMap, playerLocation, piecesOfCheese):
    """
    According to Dijkstra's algorithm, fill the route table
    Parameters:
                mazeMap -> The weighted graph
                playerLocation -> Initial vertex
                piecesOfCheese -> Destination
    Return: 
                The route table
    """
    routeTable = {}
    cellVisited = set()
    priorityQ = []

    # initialize
    vertexDistancePair = VertexDistance(playerLocation, None, 0)
    heapq.heappush(priorityQ, vertexDistancePair)
    
    routeTable[playerLocation] = None
    currentVertex, lastVertex = None, None

    # main body of the algorithm
    while len(priorityQ) != 0:
        currentPair = heapq.heappop(priorityQ)
        currentVertex, lastVertex, distance = currentPair.vertex(), currentPair.father(), currentPair.distance()
        cellVisited.add(currentVertex)
        routeTable[currentVertex] = lastVertex
        for neighbor in mazeMap[currentVertex]:
            distanceViaCurrentVertex = distance + mazeMap[currentVertex][neighbor]
            addOrReplace(priorityQ, neighbor, distanceViaCurrentVertex, cellVisited, currentVertex)
        lastVertex = currentVertex

    routeTable[currentVertex] = lastVertex
    return routeTable

def addOrReplace(priorityQ, vertex, distance, cellVisited, lastVertex):
    """
    According to the dijkstra's algorithm, only those whose distance with inital vertex is higher 
    will be replace.
    Parameters:
                priorityQ -> The min heap that store the distance to update
                vertex -> vertex to add or to update
                distance
    Return:
                A updated min-heap
    """
    index = getOriginDistance(priorityQ, vertex)
    if index == None:
        if vertex not in cellVisited:
            heapq.heappush(priorityQ, VertexDistance(vertex, lastVertex, distance))
    else:
        if distance < priorityQ[index].distance():
            print("To be delated", priorityQ[index])
            del priorityQ[index]
            print("After delate", priorityQ[index])
            heapq.heappush(priorityQ, VertexDistance(vertex, lastVertex, distance))


def getOriginDistance(priorityQ, vertex):
    """
    Find the original distance of vertex in the graph,
    if it exists, return the corresponding index and the distance
    if it does not exist, return None, None
    """
    for index, element in enumerate(priorityQ):
        if element.vertex() == vertex:
            return index
    return None

def print_PQ(q):
    """
    This fonction is ONLY for debug
    """
    for item in q:
        print(str(item), end=' ')
    print()

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
    global ins
    routeTable = dijkstra(mazeMap, playerLocation, piecesOfCheese)
    ins = findShortestPath(routeTable, piecesOfCheese)

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
    global ins
    return ins[playerLocation]