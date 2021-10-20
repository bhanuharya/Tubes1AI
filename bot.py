# from sandbox.constants import *
import random

class ColorConstant:
    RED = "RED"
    BLUE = "BLUE"
    BLACK = "BLACK"


class ShapeConstant:
    CROSS = "X"
    CIRCLE = "O"
    BLANK = "-"

class Piece:
    """
    Class representation for Piece inside Board

    [ATTRIBUTES]
        shape: str -> Shape piece inside board
        color: str -> Color piece inside board
    """

    def __init__(self, shape: str, color: str):
        self.shape = shape
        self.color = color

    def __str__(self):
        if self.color == ColorConstant.RED:
            return colored.red(self.shape)
        elif self.color == ColorConstant.BLUE:
            return colored.blue(self.shape)
        elif self.color == ColorConstant.BLACK:
            return colored.green(self.shape)

    def __eq__(self, o: object) -> bool:
        return self.shape == o.shape and self.color == o.color
        
class Board:
    """
    Class representation class for Board used in game

    [ATTRIBUTES]
        row: int -> boards row shape
        col: int -> boards column shape
        board: 2D List -> board representation
    """

    def __init__(self, row: int, col: int):
        self.row = row
        self.col = col
        self.board = [
            [Piece(ShapeConstant.BLANK, ColorConstant.BLACK) for i in range(self.col)]
            for j in range(self.row)
        ]

######### CODE STARTS #########
import json, copy, os
from time import time
class Minimax:
    def __init__(self, isLearning):
        self.isLearning = isLearning # Used to train the bot and populate the Database JSON. Set to False if the bot is currently playing. 
        self.database = {} # The current database object to lookup positions 
        # if( not os.path.exists('./database.json')) : 
        #     self.saveToDatabase()
        # else :
        #     self.loadDatabase()

        # Load Reference Table
        if( not os.path.exists('./reference_map.json')) : 
            self.getReferenceMap(row, col, 4)
        self.loadReferenceMap()
        # self.depth = 4

        # For Debugging
        self.checkVariations = 0

        pass
    
    def saveToDatabase(self) :
        with open("database.json", "w") as outfile:
            json.dump(self.database, outfile)

    def loadDatabase(self) :  
        with open("database.json", "r") as json_file:
            self.database = json.load(json_file)
    
    def loadReferenceMap(self) : 
        with open("reference_map.json", "r") as json_file:
            self.referenceMap = json.load(json_file)

    def getReferenceMap(self, row, col, piecesVariation) :
        referenceMap = [[[] for j in range(row)] for i in range(col)]
        for i in range (col) : 
            for j in range(row) :
                for k in range (piecesVariation) : 
                    referenceMap[i][j].append(random.randint(2**36,2**64))
        with open("reference_map.json", "w") as outfile:
            json.dump(referenceMap, outfile)
        

    def hashPositionMap(self, positionArray) :
        # Definitely needs some check later on real implementation
        
        col = len(positionArray) 
        finalValue = 2**64 # Basically a 36 bit long integer will all 1s
        for i in range(col) :
            row = len(positionArray[i])
            for j in range(row): 
                pieceValue = positionArray[i][j]
                try : 
                    value = self.referenceMap[i][j][pieceValue-1]
                except IndexError : 
                    # print(positionArray)
                    pass
                finalValue = finalValue ^ value
        return finalValue

    def getNumberRepresentation(self, piece) :
        if( piece.shape == ShapeConstant.CIRCLE and piece.color == ColorConstant.RED ) :
            return 1
        elif( piece.shape == ShapeConstant.CIRCLE and piece.color == ColorConstant.BLUE ) :
            return 2
        elif( piece.shape == ShapeConstant.CROSS and piece.color == ColorConstant.RED ) :
            return 3
        elif( piece.shape == ShapeConstant.CROSS and piece.color == ColorConstant.BLUE) :
            return 4
        else :
            return 0

    def getPieceRepresentation (self, number) : 
        if( number == 1 ) :
            return ( ShapeConstant.CIRCLE, ColorConstant.RED )
        elif ( number == 2):
            return ( ShapeConstant.CIRCLE, ColorConstant.BLUE )
        elif ( number == 3):
            return ( ShapeConstant.CROSS, ColorConstant.RED )
        elif ( number == 4) :
            return ( ShapeConstant.CROSS, ColorConstant.BLUE)
        else :
            return 0

    def getPositionArrayFromBoard(self, board) : 
        currentPosition = board.board 
        positionArray = [
            [] for j in range(board.col)
        ]
        for i in range(board.row) : 
            for j in range(board.col) : 
                piece = self.getNumberRepresentation(currentPosition[i][j])
                if(piece != 0) : 
                    positionArray[j].append(piece)
        return positionArray
    
    
    def learn(self, board, shape, color, depth) : 
        # Problem : Because the transition table already have the value for position x, the learn function doesn't go deep enough. 
        self.find(board, shape, color, depth)
        # self.find(board, ColorConstant.RED, 3)
        # self.find(board, ColorConstant.RED, 4)
        # minimax.find(board, ColorConstant.RED, 4)
        # minimax.find(board, ColorConstant.RED, 5)
        # minimax.find(board, ColorConstant.RED, 6)
        # 
        # if(depth == 6) : 
            # print(self.database)
            # self.saveToDatabase()
        return 0

    def find(self, board, shape, color, depth = 4):

        # Preparation
        currentTime = time()
        # Player piece shape and color
        self.shape = shape
        self.color = color
        col = board.col 
        row = board.row
        positionArray = self.getPositionArrayFromBoard(board) 
        # positionArray = [[2, 2, 2, 2, 4], [3], [], [1], [], [1], []]
        # positionArray = [[2, 2, 2, 2, 4, 2, 1], [3], [], [1], [4], [1], []]
        # positionArray = [[2, 2], [3], [], [1, 2], [4], [], []]
        # positionArray = [[2, 2, 4, 3], [3], [], [1, 2], [4], [2], []]
        # positionArray = [[2, 2, 4, 3], [3], [2, 3], [1, 2], [4], [2], [2]]
        # positionArray = [[2, 2, 3], [3, 4], [], [1, 2], [4], [4], []]
        positionArray = [[2, 3, 2], [1, 4], [], [], [], [3], []]
        

        # Initiates the reuslts 
        self.totalPositions = 0
        self.bestMove = (0,0) # Just a placeholder value ( Column, Shape and Color )
        self.bestMoveScore = float("-inf")

        # Calculation
        # self.findAllPossiblePositions(color, positionArray, row, col, depth)
        # Minimax
        self.Minimax(color, positionArray, row, col, depth = depth)
        self.totalPositions = 14**depth # Basic math; What it should be. Already confirmed

        # Result
        print("Depth :", depth)
        print("Number of possible positions :",self.totalPositions)
        print("Best Move : ", self.bestMove)
        print("Score :",self.bestMoveScore)
        print("Time : ",time()- currentTime, "Seconds")
        print("Total positions in transition table :", len(self.database))
        # print("Variations : ", self.checkVariations)


        return self.bestMove

    def getPositionScore(self, positionArray) : 
        def checkStreak(currentNode, positionArray, visited = [], streak = 2 ) :  
            streak_way = [(-1, 0), (0, -1), (0, 1), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]
            queue = {}
            # print("visited", visited)
            
            # Preparation
            currentNodePiece = self.getPieceRepresentation(currentNode["value"])
            pieceShape = 1 if currentNodePiece[0] == ShapeConstant.CIRCLE else 3
            pieceColor = 1 if currentNodePiece[1] == ColorConstant.RED else 2 
            shapeNumber = 1 if self.shape == ShapeConstant.CIRCLE else 3
            colorNumber = 1 if self.color == ColorConstant.RED else 2 
            
            score = 0
            visited.append(currentNode)
            # print(positionArray, currentNode["position"])
            for move in streak_way :
                scoreIncrement = streak
                streakFlag = False
                if scoreIncrement == 4 :
                    scoreIncrement = float("inf")
                # print(currentNode["position"] + move)
                (x, y) = (currentNode["position"][0] + move[0], currentNode["position"][1] + move[1])
                if x < 0 or y < 0 :
                    continue
                found = False
                for position in visited:
                    if( x == position["position"][0] and y == position["position"][1]) :
                        found = True 
                        break 
                if(found) :
                    continue
                try :
                    value = positionArray[x][y]
                    
                except IndexError :
                    continue
                # print("nextPosition : ", x,y)
                if value == pieceShape or value == pieceShape + 1 : 
                    streakFlag = True
                    if( pieceShape == shapeNumber ) :
                        # score = float("inf") if scoreIncrement == float("inf") else score + scoreIncrement
                        score = score + 200 if scoreIncrement == float("inf") else score + scoreIncrement
                    else :
                        # score = float("-inf") if scoreIncrement == float("inf") else score - scoreIncrement
                        score = score - 200 if scoreIncrement == float("inf") else score - scoreIncrement
                    

                if value == colorNumber or value == colorNumber + 2 : 
                    streakFlag = True
                    if(pieceColor == colorNumber) :
                        score = score + 200 if scoreIncrement == float("inf") else score + 5*scoreIncrement
                    else :
                        score = score - 200 if scoreIncrement == float("inf") else score - 5*scoreIncrement
                
                # print(value, score)
                if(streakFlag) :
                    # print(score)
                    key = str(x) + "," + str(y)
                    queue[key] = value

            while len(queue) > 0 :
                key = list(queue.keys())[0]
                position = (int(key[0]), int(key[2]))
                nextNode = {"position" : position, "value" : queue.pop(key)}
                # print(queue)
                # print(nextNode)
                score += checkStreak(nextNode, positionArray, visited, streak + 1)
            
            # print("End Score", score)
            return score

                

        totalScore = 0
        for x in range(len(positionArray)) : 
            row = positionArray[x]
            for y in range(len(row)) : 
                value = positionArray[x][y]
                totalScore += checkStreak(currentNode = {"position" : (x,y), "value" : value},  positionArray = positionArray )
                
        # print(positionArray, totalScore)
        return totalScore

    # Uses Minimax  
    def getNextIterationScore(self, piece, nextColor, index, positionArray, row, col, alpha, beta, isMaximizing, depth) : 
        j = index
        positionArray[j].append(piece)
        hashValue = self.hashPositionMap(positionArray)
        
        if( hashValue in self.database.keys()) :
            score = self.database[hashValue]["score"]
        else : 
            # print(nextColor, positionArray)
            score = self.Minimax(nextColor, positionArray, row, col, alpha, beta, not isMaximizing, depth-1)
        positionArray[j].pop()
        return score

    def Minimax(self, color, positionArray, row = 6, col = 7, alpha = float("-inf"), beta = float("inf"), isMaximizing = True, depth = 3):
        # Using Fail-Soft Alpha Beta
        if(depth == 0) :
            score = self.getPositionScore(positionArray)
            hashValue = self.hashPositionMap(positionArray)

            # Apparently the reference for the positions is linked with each other so i need to deep copy it 
            # Putting the actual position into the database is only for human comprehension purposes
            newPositionArray = copy.deepcopy(positionArray) if self.isLearning else positionArray

            # Save the evaluated position into the database 
            self.database[hashValue] = {"score" : score, "positionArray" : newPositionArray, "totalPositions" : self.totalPositions}

            return score
        elif (isMaximizing) :
            maxScore = float("-inf")
            for j in range(col*2) : 
                nextColor = ColorConstant.RED if color == ColorConstant.BLUE else ColorConstant.BLUE
                piece = self.getNumberRepresentation(Piece(ShapeConstant.CROSS if j % 2 == 1 else ShapeConstant.CIRCLE , color))
                # print(piece) # The Piece Value 3 is never added to the database somehow
                index = j/2 if j % 2 == 0 else (j-1)/2
                if(index > row) :
                    continue
                score = self.getNextIterationScore(piece, nextColor, int(index), positionArray, row, col, alpha, beta, isMaximizing, depth)

                # Compares the scores 
                maxScore = max(score, maxScore)
                if( score > maxScore ) :
                    maxScore = score
                if( maxScore > self.bestMoveScore  ) :
                    self.bestMoveScore = maxScore 
                    self.bestMove = (int(index), self.getPieceRepresentation(piece))
                alpha = max(alpha, maxScore)
                if(maxScore >= beta) :
                    break 
            return maxScore
        else :
            minScore = float("inf")
            for j in range(col*2) : 
                nextColor = ColorConstant.RED if color == ColorConstant.BLUE else ColorConstant.BLUE
                piece = self.getNumberRepresentation(Piece(ShapeConstant.CROSS if j % 2 == 1 else ShapeConstant.CIRCLE , color))
                index = j/2 if j % 2 == 0 else (j-1)/2
                if(index >= row) :
                    continue
                score = self.getNextIterationScore(piece, nextColor, int(index), positionArray, row, col, alpha, beta, isMaximizing, depth)

                # Compares the scores 
                minScore = min(score, minScore)
                beta = min(beta, minScore)
                if(minScore <= alpha) :
                    break 
            return minScore

    
    # Used for the findAllPossiblePositions method
    def getPieceScore(self, piece, nextColor, index, positionArray, row, col, depth) : 
        j = index
        positionArray[j].append(piece)
        

        hashValue = self.hashPositionMap(positionArray)
        if( hashValue in self.database.keys()) :
            score = self.database[hashValue]["score"]
        else : 
            score = self.findAllPossiblePositions(nextColor, positionArray, row, col, depth-1)
        positionArray[j].pop()
        return score


    def findAllPossiblePositions(self, color, positionArray, row, col,  depth = 3 ) :
        # print(positionArray)
        if depth == 0 : 
            # self.totalPositions +=1 
            score = self.getPositionScore(positionArray)
            hashValue = self.hashPositionMap(positionArray)
            # if len(positionArray[0]) > 0 and positionArray[0][0] == 1 :
            #     self.checkVariations += 1

            # Apparently the reference for the positions is linked with each other so i need to deep copy it 
            # Putting the actual position into the database is only for human comprehension purposes
            newPositionArray = copy.deepcopy(positionArray) if self.isLearning else positionArray

            # Save the evaluated position into the database 
            self.database[hashValue] = {"score" : score, "positionArray" : newPositionArray, "totalPositions" : self.totalPositions}

            return score
        
        bestScore = float('-inf')
        for j in range(col*2) : 
            nextColor = ColorConstant.RED if color == ColorConstant.BLUE else ColorConstant.BLUE
            piece = self.getNumberRepresentation(Piece(ShapeConstant.CROSS if j % 2 == 1 else ShapeConstant.CIRCLE , color))
            index = int(j/2 if j % 2 == 0 else (j-1)/2)
            if(len(positionArray[index]) == row) : 
                continue
            score = self.getPieceScore(piece, nextColor, index, positionArray, row, col, depth)
            if score > bestScore :
                bestScore = score
                # self.bestMove = 

        return bestScore
row = 6
col = 7
shape = ShapeConstant.CROSS
color = ColorConstant.BLUE
for i in range(1, 7) : 
    board = Board(row, col)
    minimax = Minimax(True)
    minimax.learn(board, shape, color, i)

        