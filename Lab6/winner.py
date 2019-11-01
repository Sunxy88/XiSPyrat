import numpy as np
import random

INF = float("inf")
MOVE_DOWN = 'D'
MOVE_LEFT = 'L'
MOVE_RIGHT = 'R'
MOVE_UP = 'U'
DIRECTION = {
    (0, -1): MOVE_DOWN,
    (-1, 0): MOVE_LEFT ,
    (0, 1): MOVE_UP,
    (1, 0): MOVE_RIGHT,
}

INVERSE_DIRECTION = {
    MOVE_DOWN: (0, -1),
    MOVE_LEFT: (-1, 0),
    MOVE_UP: (0, 1),
    MOVE_RIGHT: (1, 0)
}

originCheeses = []
path = []
metaGraph = {}
left, right = 0, 1

def preprocessing(mazeMap, mazeWidth, mazeHeight, playerLocation, opponentLocation, piecesOfCheese, timeAllowed):
    global metaGraph, path, originCheeses
    originCheeses = piecesOfCheese[:]
    metaGraph = getMetaGraph(mazeMap, piecesOfCheese, playerLocation)
    metaGraphWithoutStart = {}
    for vertex in metaGraph:
        if vertex == playerLocation:
            continue
        metaGraphWithoutStart[vertex] = metaGraph[vertex]
    tsp = TSP(metaGraphWithoutStart, playerLocation)
    path = tsp.run(170)
    path.insert(0, playerLocation)
    # print("Metagraph in preprocessing", metaGraph)
    # print("Cheeses", piecesOfCheese)
    # print("Path", path)



def turn(mazeMap, mazeWidth, mazeHeight, playerLocation, opponentLocation, playerScore, opponentScore, piecesOfCheese, timeAllowed):
    global left, right
    # print("counter", right)
    # print("Start:", path[left], "End:", path[right], "Player location:", playerLocation)
    # print("Test1", metaGraph[path[left]])
    # print("Test2", metaGraph[path[left]][path[right]])
    # print("Test3", metaGraph[path[left]][path[right]][1][playerLocation])
    move = metaGraph[path[left]][path[right]][1][playerLocation]
    nextLocation = tuple(np.add(playerLocation, INVERSE_DIRECTION[move]))
    if nextLocation == path[right]:
        left = right
        right += 1
        while right + 1 < len(path) and path[right] not in piecesOfCheese:
            right += 1
        # print("counter", counter)
    return move



class Life(object):
      """
      Individual class
      """
      def __init__(self, aGene = None):
            self.gene = aGene
            self.score = -1


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
    def __init__(self, metaGraph, playerLocation, aLifeCount = 200):
        self.playerLocation = playerLocation
        self.metaGraph = metaGraph
        self.initCitys()
        self.lifeCount = aLifeCount
        self.ga = Population(aCrossRate = 0.7, 
                aMutationRage = 0.05, 
                aLifeCount = self.lifeCount, 
                aGeneLenght = len(self.cities), 
                aMatchFun = self.matchFun())


    def initCitys(self):
        """
        Put all vertices in cities
        """
        self.cities = []
        for vertex in self.metaGraph:
            self.cities.append(vertex)
        

    def distance(self, order):
        index1 = order[0]
        # print("order", order)
        # print("cities", self.cities)
        # print(self.playerLocation, self.cities[index1])
        # print("Metagraph in TSP", self.metaGraph)
        # print("player location:", self.playerLocation, "city:", self.cities[index1])
        distance = metaGraph[self.playerLocation][self.cities[index1]][0]       # Here is a trick, initilize the distance is the distance between first city and player location
        # print("distance in TSP", distance)
        for i in range(1, len(self.cities) - 1):
            index1, index2 = order[i], order[i + 1]
            city1, city2 = self.cities[index1], self.cities[index2]
            distance += self.metaGraph[city1][city2][0]

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
        gene = [self.cities[x] for x in gene]
        return gene


def getMetaGraph(mazeMap, piecesOfCheese, playerLocation):
    # Like this: metaGraph[start][end][0] means the distance between start and end, 
    # metaGraph[start][end][1] means the instruction in the path from start to end
    metaGraph = {}
    metaGraph[playerLocation] = {}
    routeTable = dijkstra(playerLocation, mazeMap)
    for cheese in piecesOfCheese:
        metaGraph[playerLocation][cheese] = (routeTable[cheese][1], getInstructoins(routeTable, cheese))
    # metaGraphPath = {}
    for start in piecesOfCheese:
        metaGraph[start] = {}
        # metaGraphPath[start] = {}
        routeTable = dijkstra(start, mazeMap)
        # print(routeTable)
        for destination in piecesOfCheese:
            metaGraph[start][destination] = (routeTable[destination][1], getInstructoins(routeTable, destination))
            # metaGraphPath[start][destination] = findShortesPath(routeTable, destination)
    return metaGraph
    

def dijkstra(initalVertex, mazeMap):
    """
    Get a routing table from inital vertex to all other vetex by using Dijkstra Algorithm
    """
    notVisit = []
    routetable = {}
    for vertex in mazeMap:
        notVisit.append(vertex)
        routetable[vertex] = (None, INF)
    routetable[initalVertex] = (None, 0)

    while len(notVisit) > 0:
        toVisit, distanceToVisit = None, INF
        for vertex in notVisit:
            if routetable[vertex][1] < distanceToVisit:
                toVisit, distanceToVisit = vertex, routetable[vertex][1]

        for neighbor in mazeMap[toVisit]:
            if routetable[neighbor][1] > distanceToVisit + mazeMap[toVisit][neighbor]:
                routetable[neighbor] = (toVisit, distanceToVisit + mazeMap[toVisit][neighbor])
        
        notVisit.remove(toVisit)
    
    return routetable


def findShortesPath(routetable, destination):
    currentVertex = destination
    path = []
    # origin = ()
    while currentVertex != None:
        path.insert(0, currentVertex)
        if routetable[currentVertex][0] == None:
            # origin = currentVertex
            break
        currentVertex = routetable[currentVertex][0]
    # path.insert(0, currentVertex)
    return path


def getInstructoins(routeTable, destination):
    path = findShortesPath(routeTable, destination)
    # print(path)
    instruction = {}
    for i in range(len(path) - 1):
        move = tuple(np.subtract(path[i + 1], path[i]))
        instruction[path[i]] = DIRECTION[move]
    return instruction
