# Lab 6: Catch all cheeses using genetic algorithm
# Gene represents the order to visit in meta graph
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
import random
import numpy as np
import math
from collections import OrderedDict
###############################
# Please put your global variables here
bestWeight = sys.maxsize
bestPath = []
metaGraphPath = {}
instruction = []
counter = 0
SCORE_NONE = -1 # Used to initialize the score for each individual
metaGraph = {}

class Life(object):
      """
      Individual class
      """
      def __init__(self, aGene = None):
            self.gene = aGene
            self.score = SCORE_NONE


class Population(object):
      """
      Population class
      """
      def __init__(self, aCrossRate, aMutationRage, aLifeCount, aGeneLenght, aMatchFun = lambda life : 1):
            self.croessRate = aCrossRate
            self.mutationRate = aMutationRage
            self.lifeCount = aLifeCount
            self.geneLenght = aGeneLenght
            self.matchFun = aMatchFun                 # match function
            self.lives = []                           # all individuals
            self.best = None                          # the individual whose score is highest
            self.generation = 1
            self.crossCount = 0
            self.mutationCount = 0
            self.bounds = 0.0                         # sum of score, used to calculate probability

            self.initPopulation()


      def initPopulation(self):
            """
            Initialize population
            """
            self.lives = []
            for i in range(self.lifeCount):
                gene = [ x for x in range(self.geneLenght) ] 
                random.shuffle(gene)
                life = Life(gene)
                self.lives.append(life)


      def judge(self):
            """
            evaluate, calculate each individual's score
            """
            self.bounds = 0.0
            self.best = self.lives[0]
            for life in self.lives:
                life.score = self.matchFun(life)
                self.bounds += life.score
                if self.best.score < life.score:
                    self.best = life


      def cross(self, parent1, parent2):
            """
            cross the gene
            """
            index1 = random.randint(0, self.geneLenght - 1)
            index2 = random.randint(index1, self.geneLenght - 1)
            tempGene = parent2.gene[index1:index2]   # gene segement to be crossed
            newGene = []
            p1len = 0
            for g in parent1.gene:
                  if p1len == index1:
                        newGene.extend(tempGene)     # add the segment of gene
                        p1len += 1
                  if g not in tempGene:
                        newGene.append(g)
                        p1len += 1
            self.crossCount += 1
            return newGene


      def  mutation(self, gene):
            """
            Mutate
            """
            index1 = random.randint(0, self.geneLenght - 1)
            index2 = random.randint(0, self.geneLenght - 1)

            newGene = gene[:]       # create a new gene sequence
            newGene[index1], newGene[index2] = newGene[index2], newGene[index1]
            self.mutationCount += 1
            return newGene


      def getOne(self):
            """
            Select an individual 
            """
            r = random.uniform(0, self.bounds)
            for life in self.lives:
                  r -= life.score
                  if r <= 0:
                        return life

            raise Exception("Selection error", self.bounds)


      def newChild(self):
            """
            produce new child
            """
            parent1 = self.getOne()
            rate = random.random()

            # cross according to the possibility
            if rate < self.croessRate:
                  # cross
                  parent2 = self.getOne()
                  gene = self.cross(parent1, parent2)
            else:
                  gene = parent1.gene

            # mutate according to the possibility
            rate = random.random()
            if rate < self.mutationRate:
                  gene = self.mutation(gene)

            return Life(gene)


      def next(self):
            """
            generate new generation
            """
            self.judge()
            newLives = []
            newLives.append(self.best)            # put the best individual in next generation
            while len(newLives) < self.lifeCount:
                  newLives.append(self.newChild())
            self.lives = newLives
            self.generation += 1

class TSP:
    def __init__(self, metaGraph, playerLocation,aLifeCount = 200):
        self.playerLocation = playerLocation
        self.metaGraph = metaGraph
        self.initCitys(metaGraph)
        self.lifeCount = aLifeCount
        self.ga = Population(aCrossRate = 0.6, 
                aMutationRage = 0.05, 
                aLifeCount = self.lifeCount, 
                aGeneLenght = len(self.cities), 
                aMatchFun = self.matchFun())


    def initCitys(self, metaGraph):
        """
        Put all vertices in cities
        """
        self.cities = []
        for vertex in metaGraph:
            self.cities.append(vertex)
        

    def distance(self, order):
        index1 = order[1]
        # print(self.playerLocation, self.cities[index1])
        distance = metaGraph[self.playerLocation][self.cities[index1]]
        for i in range(1, len(self.cities) - 1):
            index1, index2 = order[i], order[i + 1]
            city1, city2 = self.cities[index1], self.cities[index2]
            # distance += math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)
            distance += self.metaGraph[city1][city2]

        return distance


    def matchFun(self):
        return lambda life: 1.0 / self.distance(life.gene)


    def run(self, n = 0):
        while n > 0:
            self.ga.next()
            # distance = self.distance(self.ga.best.gene)
            gene = self.ga.best.gene
            # print (("%d : %f -- route:%s") % (self.ga.generation, distance, gene))
            n -= 1
        return gene


def preprocessing(mazeMap, mazeWidth, mazeHeight, playerLocation, opponentLocation, piecesOfCheese, timeAllowed):
    global metaGraphPath, instruction, metaGraph
    metaGraph, metaGraphPath = getMetaGraph(mazeMap, playerLocation, piecesOfCheese)
    orderCal = {}
    for index, vertex in enumerate(metaGraph.keys()):
        orderCal[index] = vertex
    # print("orderCal", orderCal)

    metaGraphWithoutStart = {}
    for vertex in metaGraph:
        if vertex == (0, 0):
            continue
        metaGraphWithoutStart[vertex] = metaGraph[vertex]

    tsp = TSP(metaGraphWithoutStart, playerLocation)
    order = tsp.run(80)
    order = [x + 1 for x in order]
    order.insert(0, 0)
    # print("order in index:", order)
    order = [orderCal[x] for x in order]
    # print("order in vertex:", order)
    for i in range(1, len(order)):
        instruction.append(metaGraphPath[order[i - 1]][order[i]])
    # raise KeyboardInterrupt
    

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




# Here is the code for dijkstra algorithm to be used for a metagraph
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

# Here is the code to get a metagraph
def getMetaGraph(mazeMap, playerLocation, piecesOfCheese):
    """
    To get the metagraph of the maze and store all the locations of cheeses
    """
    metaGraph = OrderedDict()
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

def allVisited(metaGraph, cellVisited):
    """
    To judge if all vertices have been visited
    """
    for vertex in metaGraph.keys():
        if vertex not in cellVisited:
            return False
    return True