# Lab2: Implement BFS to get only one peace of cheese with the 
# implementation of queue structure. 
# ATTENTION: In a maze without mud -> An unweighted graph
# Copyright: Xi SONG 14/09/2019
# TODO: 思考每次轮到我的turn时如何保存上一回合的状态

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


###############################
# Please put your global variables here
ins = []    # Instructions used to guide rat

class Q:
    """
    A simple implementation of Queue structure
    """
    def __init__(self, origin = []):
        """
        Create an queue.
        Parameter: origin -> the original list for the queue and default is an empty list
        """
        self.data = origin[:]
        self.head = 0
    
    def isEmpty(self):
        """
        If the queue is emtpy return True
        Else return False
        """
        return len(self.data) == 0

    def push(self, element):
        """
        Push an element
        Parameter: element -> element to be pushed
        Exception: if the element to be pushed is not corresponding with the first element in 
        the list, raise a TypeError
        """
        if not self.isEmpty() and not isinstance(element, type(self.data[0])):
            raise TypeError
        
        self.data.append(element)

    def pop(self):
        """
        Pop an element
        Return: the fist added element of this queue
        """
        if self.isEmpty() or self.head == len(self.data):
            raise Exception("Queue is EMPTY!")

        firstElement = self.data[self.head]
        self.head += 1
        return firstElement


# Calculate the direction according to player location and next location
def calMove(playerLocation, nextLocation):
    move_vector = tuple(numpy.subtract(nextLocation, playerLocation))
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
    instructions = []
    currentVertex = piecesOfCheese[0]
    
    while routeTable[currentVertex]:
        move = calMove(routeTable[currentVertex], currentVertex)
        instructions.insert(0, move)
        currentVertex = routeTable[currentVertex]

    return instructions


def BFS(mazeMap, playerLocation, piecesOfCheese):
    """
    Fill in a route table using BFS
    Parameters: mazeMap -> a unweighted graph
                playerLocation -> the start vertex
                piecesOfCheese -> destination of the shortest path(Should be only one)
    Return: A route table
    """
    if len(piecesOfCheese) > 1:
        raise Exception("Piece of cheese should be 1")

    # Route table 
    routeTable = {}
    # Queue to implemente BFS
    toolQueue = Q()

    toolQueue.push((playerLocation, None))

    while piecesOfCheese[0] not in list(routeTable.keys): # no need to calculate the shortest paths to all vertices
        currentVertex = toolQueue.pop()
        # Add vertex and its father node to the route table
        if currentVertex[0] not in list(routeTable.keys):
            routeTable[currentVertex[0]] = currentVertex[1]
        else:
            continue
    
        for neighbor in mazeMap[currentVertex[0]]:
            toolQueue.push((neighbor, currentVertex[0]))
    
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
    routeTable = BFS(mazeMap, playerLocation, piecesOfCheese)
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
    
    pass
