# Author: Kiersten Page
# Date due: March 30th, 2020
# Purpose: Implement the GRAPH-SEARCH Algorithm with A* Search Strategy for
# solving the 15-puzzle problem as described below. Use sum of Manhattan distances of tiles from
# their goal positions as heuristic function.
# Interpreter: python 3.7
import math
import copy

class Node:
    def __init__(self, puzzle, depth, moves, fValues, hVal, fVal):
        self.puzzle = puzzle # array representing "tile" locations
        self.depth = depth # node depth, equal to the gVal
        self.moves = moves # list of left, right up, down moves
        self.fValues = fValues # list of fvalues of current and previous nodes
        self.hVal = hVal # sum of manhattan distances to goal state
        self.hVal = fVal  # sum of previous moves and estimated future moves

    def calculateF(self, goalNode):
        # calculate f(n)
        self.hVal = 0
        # this portion of the code calculates the h(n) value
        for i in range(0, 16):
            for j in range(4):
                for k in range(4):
                    if int(self.puzzle[j][k]) == i:
                        x1, y1 = j, k
                    if int(goalNode.puzzle[j][k]) == i:
                        x2, y2 = j, k

            self.hVal += math.fabs(x1 - x2)
            self.hVal += math.fabs(y1 - y2)
        # calculation of f(n)
        self.fval = self.depth + self.hVal

    def checkIfIn(self, nodeList):
        #check to see if a node is already in a list, if node is in list, return True, else, return False
        if len(nodeList) == 0:
            return False
        for node in nodeList:
            if self.isEqual(node):
                # node is already in the nodeList, don't add
                return True
        return False

    def isEqual(self, node):
        # will check if a two nodes are equal
        # can be used to compare to goal node, or check if node is already in the frontier/explored set
        # if nodes are equal, return true, else, return false
        for i in range(4):
            for j in range(4):
                if self.puzzle[i][j] != node.puzzle[i][j]:
                    return False
                else:
                    continue
        return True

    def locateBlank(self):
        # locate the position of the blank space
        for i in range(4):
            for j in range(4):
                if self.puzzle[i][j] == "0":
                    return i, j
                else:
                    continue
        return True

    def shuffle(self, x, y, i, j):
        # shift the blank space to its new coordinate
        # x and y represent the original coordinates of the blank space
        # i and j represent the new coordinates of the blank space

        self.puzzle[x][y] = self.puzzle[i][j]
        self.puzzle[i][j] = "0"

    def updateNode(self, goalNode, move):
        # update a new node's depth, fval, fvalues, and moves
        self.depth += 1 #update depth
        self.calculateF(goalNode)
        self.fValues.append(self.fval) #update list of f(n) values
        self.moves.append(move) #update list of moves

def graphSearch():
    # initialize the frontier using the initial state of the problem
    frontier = [] # array of states to be explore
    explored = [] # array of explored states, initialized to be empty
    generatedNodes = 0 # keep track of how many nodes are generated

    # setup the start and goal nodes
    startFile = open("input.txt", "r")
    startNode = Node(readFile(startFile), 0, [], [], 0, 0)
    goalNode = Node(readFile(startFile), 0, [], [], 0, 0)
    # adjust start nodes hval, fval, and fval list
    startNode.calculateF(goalNode)
    startNode.fValues.append(startNode.fval)
    # add start node to the frontier
    frontier.append(startNode)

    while(True):
        #check if the frontier is empty. If it is, write to output file and return false for failure
        if frontier == []:
            outFile = open("outputFile.txt", "w")
            outFile.write("There is no solution to the puzzle")
            outFile.close()
            startFile.close()
            return False

        currNode = frontier.pop(0) # take the next node out of the frontier to expand

        # check if currNode is equal to the goal node and return solution if equal
        if currNode.isEqual(goalNode):
            writeFile(startNode, goalNode, currNode.depth, currNode.moves, currNode.fValues, generatedNodes)
            startFile.close()
            return True

        # if not equal, then add the node to the explored set
        explored.append(currNode)
        # expand the node, add new nodes to frontier if not already in frontier or explored
        a, b = currNode.locateBlank()
        # shuffles puzzle up
        if a != 0:
            newNode1 = copy.deepcopy(currNode)
            newNode1.shuffle(a, b, a - 1, b)
            if(newNode1.checkIfIn(frontier) or newNode1.checkIfIn(explored)):
                pass
            else:
                newNode1.updateNode(goalNode, "U")
                generatedNodes += 1
                if len(frontier) == 0:
                    frontier.append(newNode1)
                else:
                    index = insertPoint(newNode1.fval, frontier)
                    frontier.insert(index, newNode1)
        # shuffles puzzle down
        if a != 3:
            newNode2 = copy.deepcopy(currNode)
            newNode2.shuffle(a, b, a + 1, b)
            if(newNode2.checkIfIn(frontier) or newNode2.checkIfIn(explored)):
                pass
            else:
                newNode2.updateNode(goalNode, "D")
                generatedNodes += 1
                if len(frontier) == 0:
                    frontier.append(newNode2)
                else:
                    index = insertPoint(newNode2.fval, frontier)
                    frontier.insert(index, newNode2)
        # shuffles puzzle left
        if b != 0:
            newNode3 = copy.deepcopy(currNode)
            newNode3.shuffle(a, b, a, b - 1)
            if(newNode3.checkIfIn(frontier) or newNode3.checkIfIn(explored)):
                pass
            else:
                newNode3.updateNode(goalNode, "L")
                generatedNodes += 1
                if len(frontier) == 0:
                    frontier.append(newNode3)
                else:
                    index = insertPoint(newNode3.fval, frontier)
                    frontier.insert(index, newNode3)
        # shuffles puzzle right
        if b != 3:
            newNode4 = copy.deepcopy(currNode)
            newNode4.shuffle(a, b, a, b + 1)
            if(newNode4.checkIfIn(frontier) or newNode4.checkIfIn(explored)):
                pass
            else:
                newNode4.updateNode(goalNode, "R")
                generatedNodes += 1
                if len(frontier) == 0:
                    frontier.append(newNode4)
                else:
                    index = insertPoint(newNode4.fval, frontier)
                    frontier.insert(index, newNode4)
    return 0

def readFile(file):
    # this function reads in the starting file, and then returns an array representing the start, or goal node
    array = []
    count = 0
    for line in file:
        if count == 4:
            break
        array.append(line.split())
        count += 1
    return array

def insertPoint(fval, frontier):
    # this function finds and returns the location in the frontier where a node should be added
    # depending on its f(n) value
    for i in range(len(frontier)):
        if fval < frontier[i].fval:
            return i
        if i == len(frontier) - 1:
            return i

def writeFile(startNode, goalNode, depth, moves, fvals, numNodes):
    # write the solution to an output file with the respective name
    outFile = open("Output.txt", "w")
    outFile.write("***************************")
    outFile.write("\n")
    for line in startNode.puzzle:
        for num in line:
            outFile.write(str(num))
            outFile.write(" ")
        outFile.write("\n")
    outFile.write("\n")
    for line in goalNode.puzzle:
        for num in line:
            outFile.write(str(num))
            outFile.write(" ")
        outFile.write("\n")
    outFile.write("\n")
    outFile.write(str(depth))
    outFile.write("\n")
    outFile.write(str(numNodes))
    outFile.write("\n")
    for action in moves:
        outFile.write(str(action))
        outFile.write(" ")
    outFile.write("\n")
    for val in fvals:
        outFile.write(str(val))
        outFile.write(" ")
    outFile.close()
    return 0

graphSearch()
