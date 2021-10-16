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
    def __init__(self):
        # Need information of what the current player SHAPE is 
        self.isLearning = True # Used to train the bot and populate the Database JSON. Set to False if the bot is currently playing. 
        self.database = {} # The current database object to lookup positions 
        self.bestMove = (1, 2) # Just a placeholder value ( Column, Shape and Color )
        self.bestMoveScore = float("-inf")
        
        self.totalPositions = 0
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

    def getReferenceMap(self, row, column, piecesVariation) :
        referenceMap = [[[] for j in range(row)] for i in range(column)]
        for i in range (column) : 
            for j in range(row) :
                for k in range (piecesVariation) : 
                    referenceMap[i][j].append(random.randint(2**36,2**64))
        with open("reference_map.json", "w") as outfile:
            json.dump(referenceMap, outfile)
        

    def hashPositionMap(self, positionArray) :
        # Definitely needs some check later on real implementation
        
        column = len(positionArray) 
        finalValue = 2**64 # Basically a 36 bit long integer will all 1s
        for i in range(column) :
            row = len(positionArray[i])
            for j in range(row): 
                pieceValue = positionArray[i][j]
                value = self.referenceMap[i][j][pieceValue-1]
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
    
    def learn(self) : 
        minimax.find(board, ColorConstant.RED, 3)
        minimax.find(board, ColorConstant.RED, 4)
        # minimax.find(board, ColorConstant.RED, 5)
        # # minimax.find(board, ColorConstant.RED, 6)
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

        # Load Reference Table
        if( not os.path.exists('./reference_map.json')) : 
            self.getReferenceMap(row, col, 4)
        self.loadReferenceMap()

        # Calculation
        self.findAllPossiblePositions(positionArray, row, col, color, depth)

        # Result
        print("Depth :", depth)
        print("Number of possible positions :",self.totalPositions)
        print("Best Move : ", self.bestMove)
        print("Score :",self.bestMoveScore)
        print("Time : ",time()- currentTime, "Seconds")
        print("Total positions in transition table :", len(self.database))


        return self.bestMove


    def Minimax(self, positionArray,  alpha = float("-inf"), beta = float("inf"), isMaximizing = True, depth = 3):
        if(depth == 0) :
            return self.getScore(positionArray)
        elif (isMaximizing) :
            for i in 10 : 
                maxScore = float("-inf")
                score = Minimax(positionArray, alpha, beta, not isMaximizing, depth-1)
                maxScore = max(score, maxScore)
                alpha = max(alpha, maxScore)
                if(alpha >= beta) :
                    break 
                return maxScore
        else :
            for i in 10 : 
                minScore = float("inf")
                score = Minimax(positionArray, alpha, beta, not isMaximizing, depth-1)
                minScore = min(score, minScore)
                beta = min(beta, minScore)
                if(alpha >= beta) :
                    break 
                return minScore

    # Problem : Everytime there is a jump, 
    def findAllPossiblePositions(self, positionArray, row, column, color, depth = 3 ) :
        if depth == 0 : 
            self.totalPositions +=1 
            score = self.getScore(positionArray)
            hashValue = self.hashPositionMap(positionArray)

            # Apparently the reference for the positions is linked with each other so i need to deep copy it 
            newPositionArray = copy.deepcopy(positionArray) if self.isLearning else positionArray

            # Save the evaluated position into the database 
            self.database[hashValue] = {"score" : score, "positionArray" : newPositionArray, "totalPositions" : self.totalPositions}

            return score
    
        for j in range(col) : 
            nextColor = ColorConstant.RED if color == ColorConstant.BLUE else ColorConstant.BLUE

            # Get position with shape X
            pieceX = self.getPieceRepresentation(Piece(ShapeConstant.CROSS, color))
            positionArray[j].append(pieceX)
            hashValue = self.hashPositionMap(positionArray)
            if( hashValue in self.database.keys()) :
                scoreX = self.database[hashValue]["score"]
            else : 
                scoreX = self.findAllPossiblePositions(positionArray, row, column, nextColor, depth-1)
            positionArray[j].pop()
            
            if( self.bestMoveScore < scoreX ) : 
                self.bestMoveScore = scoreX
                self.bestMove = ( j, pieceX ) #Fix Best Move Logic

            # Get position with shape Y 
            pieceY = self.getPieceRepresentation(Piece(ShapeConstant.CIRCLE, color))
            positionArray[j].append(pieceY)
            hashValue = self.hashPositionMap(positionArray)
            if( hashValue in self.database.keys()) :    
                scoreY = self.database[hashValue]['score']
            else : 
                scoreY = self.findAllPossiblePositions(positionArray, row, column, nextColor, depth-1)
            positionArray[j].pop()
            if( self.bestMoveScore < scoreY ) : 
                self.bestMoveScore = scoreY
                self.bestMove = ( j, pieceY )
        return self.bestMoveScore

# bestMove = None
# currentTurn = 0
# totalPositions = 0
# samples = []
row = 6
col = 7
board = Board(row, col)
minimax = Minimax()
minimax.learn()

        