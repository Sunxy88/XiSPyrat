# Lab 5: Catch all cheeses using greedy strategy
# Copyright: Xi SONG 01/10/2019
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
import sys
import heapq
import numpy as np
###############################
# Please put your global variables here
bestWeight = sys.maxsize
bestPath = []
metaGraphPath = {}
instruction = []
counter = 0

def getMetaGraph(mazeMap, playerLocation, piecesOfCheese):
    """
    To get the metagraph of the maze and store all the locations of cheeses
    """
    metaGraph = {}
    metaGraphPath = {}
    metaGraph[playerLocation] = {}
    metaGraphPath[playerLocation] = {}
    for target in piecesOfCheese:
        metaGraph[target] = {}
        metaGraphPath[target] = {}
        metaGraph[playerLocation][target], metaGraphPath[playerLocation][target] = getPath(mazeMap, playerLocation, target)
        metaGraph[target][playerLocation] = metaGraph[playerLocation][target]
        metaGraphPath[target][playerLocation] = metaGraphPath[playerLocation][target]
    for source in piecesOfCheese:
        for target in piecesOfCheese:
            if source == target:
                continue
            metaGraph[source][target], metaGraphPath[source][target] = getPath(mazeMap, source, target)
            metaGraph[target][source] = metaGraph[source][target]
    return metaGraph, metaGraphPath

def printMetaGraphPath(metaGraphPath):
    """
    For Test ONLY
    """
    for source in metaGraphPath:
        print(source, metaGraphPath[source])
        for target in metaGraphPath[source]:
            print(metaGraphPath[source][target])

def shortestEdgeConnectedToThisVertex(metaGraph, playerLocation, cellVisited):
    """
    Get the shortest edge connected to this vertex
    """
    smallestWeight = sys.maxsize
    for target in metaGraph[playerLocation]:
        if metaGraph[playerLocation][target] < smallestWeight and target not in cellVisited:
            smallestTarget = target
            smallestWeight = metaGraph[playerLocation][target]
    return smallestTarget

def shortestOrderOfCheese(metaGraph, playerLocation):
    """
    Get the order of the piece of cheese to get
    """
    cellVisited = set()
    cellVisited.add(playerLocation)
    currentLocation = playerLocation
    order = [playerLocation]
    while not allVisited(metaGraph, cellVisited):
        currentLocation = shortestEdgeConnectedToThisVertex(metaGraph, currentLocation, cellVisited)
        order.append(currentLocation)
        cellVisited.add(currentLocation)
    return order

def allVisited(metaGraph, cellVisited):
    """
    To judge if all vertices have been visited
    """
    for vertex in metaGraph.keys():
        if vertex not in cellVisited:
            return False
    return True
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
    global metaGraphPath, instruction
    metaGraph, metaGraphPath = getMetaGraph(mazeMap, playerLocation, piecesOfCheese)
    order = shortestOrderOfCheese(metaGraph, playerLocation)
    # print("order:", order)
    for i in range(1, len(order)):
        instruction.append(metaGraphPath[order[i - 1]][order[i]])
    # for item in instruction:
    #     print(item)
    # raise KeyboardInterrupt

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
    global counter
    # move = instruction[counter][playerLocation]
    # if tuple(np.add(playerLocation, DIRECTION_TO_CALCULATION[move])) not in instruction[counter].keys():
    if playerLocation not in instruction[counter].keys():
        # print(instruction[counter])
        counter += 1
        # print(instruction[counter])
    move = instruction[counter][playerLocation]
    return move


class VertexDistance:
    """
    A class created to simpolify the utilization of heapq.heappush()
    """

    def __init__(self, currentVertex, lastVertex, distance):
        """
        Generate a new instance to be stored in priority queue
        Parameter:
                    Three elementary data used to finish the algorithm
        """
        self.__vertex = currentVertex
        self.__father = lastVertex
        self.__distance = distance
    
    def __lt__(self, anotherVertexDistance):
        """
        For the heapq.heappush()
        """
        return self.__distance < anotherVertexDistance.distance()

    def __str__(self):
        """
        For debug
        """
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


def findShortestPath(mazeMap, routeTable, destination):
    """
    According to the route table, find the shortest path
    Parameters: routeTable -> route table
                destination -> the destination of this shortest path

    Return: A list filled with instructions from the beginning to the destination
            The summary of the weight of this path
    """
    instructions = {}
    sumWeight = 0
    currentVertex = destination
    while routeTable[currentVertex] != None:
        sumWeight += mazeMap[routeTable[currentVertex]][currentVertex]
        move = calMove(routeTable[currentVertex], currentVertex)
        instructions[routeTable[currentVertex]] = move
        currentVertex = routeTable[currentVertex]

    return sumWeight, instructions

def dijkstra(mazeMap, playerLocation, destination):
    """
    According to Dijkstra's algorithm, fill the route table
    Parameters:
                mazeMap -> The weighted graph
                playerLocation -> Initial vertex
                destination -> Destination
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
            # print("To be delated", priorityQ[index])
            del priorityQ[index]
            # print("After delate", priorityQ[index])
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

def getPath(mazeMap, playerLocation, destination):
    routeTable = dijkstra(mazeMap, playerLocation, destination)
    return findShortestPath(mazeMap, routeTable, destination)
