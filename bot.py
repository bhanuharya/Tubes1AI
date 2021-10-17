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
# def toPositionString(self, piece) :
#     if( piece.Shape == ShapeConstant.CIRCLE and piece.color == ColorConstant.RED ) :
#         return "1"
#     elif( piece.Shape == ShapeConstant.CIRCLE and piece.color == ColorConstant.BLUE ) :
#         return "2"
#     elif( piece.Shape == ShapeConstant.CROSS and piece.color == ColorConstant.RED ) :
#         return "3"
#     elif( piece.Shape == ShapeConstant.CROSS and piece.color == ColorConstant.BLUE) :
#         return "4"
#     else : 
#         return "0" # fix this 

######### CODE STARTS #########
import json, copy, os
from time import time
class Minimax:
    def __init__(self, isLearning):
        # Need information of what the current player SHAPE is 
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
        self.totalPositions = 0

        # For Debugging
        self.checkVariations = 0

        pass
    
    def saveToDatabase(self) :
        with open("database.json", "w") as outfile:
            json.dump(self.database, outfile, indent=1)

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
                    print(positionArray)
                finalValue = finalValue ^ value
        return finalValue

    def getPieceRepresentation(self, piece) :
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

    def getPositionArrayFromBoard(self, board) : 
        currentPosition = board.board 
        positionArray = [
            [] for j in range(board.col)
        ]
        for i in range(board.row) : 
            for j in range(board.col) : 
                piece = self.getPieceRepresentation(currentPosition[i][j])
                if(piece != 0) : 
                    positionArray[j].append(piece)
        return positionArray
    
    def getScore(self, positionArray) : 
        return random.randint(-200,200)
    
    def learn(self, board, depth) : 
        # Problem : Because the transition table already have the value for position x, the learn function doesn't go deep enough. 
        self.find(board, ColorConstant.RED, depth)
        # self.find(board, ColorConstant.RED, 3)
        # self.find(board, ColorConstant.RED, 4)
        # minimax.find(board, ColorConstant.RED, 4)
        # minimax.find(board, ColorConstant.RED, 5)
        # # minimax.find(board, ColorConstant.RED, 6)
        # 
        if(depth == 2) : 
            print(self.database)
            self.saveToDatabase()
        return 0

    def find(self, board, color, depth = 4):
        # [RETURN] : the choosen shape and column that the bot wants to play (choosen_col, choosen_shape)
        # choosen_col, choosen_shape = self.bot[player_turn].find(
        #     self.state, player_turn, self.config.thinking_time
        # )

        # Board [i][j] => Board pada row ke i, kolom ke j
        # PositionArray [i][j] => Board pada col ke i, row ke j; Position array only accounts for to filled space

        # Preparation
        currentTime = time()
        col = board.col 
        row = board.row
        positionArray = self.getPositionArrayFromBoard(board)

        # Initiates the reuslts 
        self.totalPositions = 0
        self.bestMove = (1, 2) # Just a placeholder value ( Column, Shape and Color )
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

    # Uses Minimax  
    def getPositionScore(self, piece, nextColor, index, positionArray, row, col, alpha, beta, isMaximizing, depth) : 
        j = index
        positionArray[j].append(piece)
        hashValue = self.hashPositionMap(positionArray)
        if( hashValue in self.database.keys()) :
            score = self.database[hashValue]["score"]
        else : 
            score = self.Minimax(nextColor, positionArray, row, col, alpha, beta, not isMaximizing, depth-1)
        positionArray[j].pop()
        return score

    def Minimax(self, color, positionArray, row = 6, col = 7, alpha = float("-inf"), beta = float("inf"), isMaximizing = True, depth = 3):
        # Using Fail-Soft Alpha Beta
        # print("Test")
        if(depth == 0) :
            score = self.getScore(positionArray)
            hashValue = self.hashPositionMap(positionArray)

            # Apparently the reference for the positions is linked with each other so i need to deep copy it 
            # Putting the actual position into the database is only for human comprehension purposes
            newPositionArray = copy.deepcopy(positionArray) if self.isLearning else positionArray

            # Save the evaluated position into the database 
            self.database[hashValue] = {"score" : score, "positionArray" : newPositionArray, "totalPositions" : self.totalPositions}

            return score
        elif (isMaximizing) :
            for j in range(col*2) : 
                maxScore = float("-inf")
                nextColor = ColorConstant.RED if color == ColorConstant.BLUE else ColorConstant.BLUE
                piece = self.getPieceRepresentation(Piece(ShapeConstant.CROSS if j % 2 == 1 else ShapeConstant.CIRCLE , color))
                print(piece) # The Piece Value 3 is never added to the database somehow
                index = j/2 if j % 2 == 0 else (j-1)/2
                if(index > row) :
                    continue
                score = self.getPositionScore(piece, nextColor, int(index), positionArray, row, col, alpha, beta, isMaximizing, depth)

                # Compares the scores 
                maxScore = max(score, maxScore)
                alpha = max(alpha, maxScore)
                if(maxScore >= beta) :
                    break 
            return maxScore
        else :
            for j in range(col*2) : 
                minScore = float("inf")
                nextColor = ColorConstant.RED if color == ColorConstant.BLUE else ColorConstant.BLUE
                piece = self.getPieceRepresentation(Piece(ShapeConstant.CROSS if j % 2 == 1 else ShapeConstant.CIRCLE , color))
                index = j/2 if j % 2 == 0 else (j-1)/2
                if(index >= row) :
                    continue
                score = self.getPositionScore(piece, nextColor, int(index), positionArray, row, col, alpha, beta, isMaximizing, depth)

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
            score = self.getScore(positionArray)
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
            piece = self.getPieceRepresentation(Piece(ShapeConstant.CROSS if j % 2 == 1 else ShapeConstant.CIRCLE , color))
            index = j/2 if j % 2 == 0 else (j-1)/2
            score = self.getPieceScore(piece, nextColor, int(index), positionArray, row, col, depth)
            bestScore = bestScore if score < bestScore else score

        return bestScore

row = 6
col = 7
for i in range(1, 3) : 
    board = Board(row, col)
    minimax = Minimax(True)
    minimax.learn(board, i)

        