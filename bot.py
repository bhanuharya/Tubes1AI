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
import json
class Minimax:
    def __init__(self):
        # Need information of what the current player SHAPE is 
        self.isLearning = True # Used to train the bot and populate the Database JSON. Set to False if the bot is currently playing. 
        self.database = {} # The current database object to lookup positions 
        self.bestMove = (1, 2) # Just a placeholder value ( Column, Shape and Color )
        self.bestMoveScore = float("-inf")
        self.referenceMap = self.getReferenceMap(6,7, 4)
        self.totalPositions = 0
        pass

    def getReferenceMap(self, row, column, piecesVariation) :
        referenceMap = [[[] for j in range(row)] for i in range(column)]
        for i in range (column) : 
            for j in range(row) :
                for k in range (piecesVariation) : 
                    referenceMap[i][j].append(random.randint(2**36,2**64))
        # print(referenceMap)
        return referenceMap

    def hashPositionMap(self, positionArray) :
        # Definitely needs some check later on real implementation
        
        column = len(positionArray) 
        finalValue = 2**64 # Basically a 36 bit long integer will all 1s
        for i in range(column) :
            row = len(positionArray[i])
            for j in range(row): 
                pieceValue = positionArray[i][j]
                # print(self.referenceMap[i][j])
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

    def find(self, board, color):
        # [RETURN] : the choosen shape and column that the bot wants to play (choosen_col, choosen_shape)
        # choosen_col, choosen_shape = self.bot[player_turn].find(
        #     self.state, player_turn, self.config.thinking_time
        # )

        # Board [i][j] => Board pada row ke i, kolom ke j
        # PositionArray [i][j] => Board pada col ke i, row ke j; Position array only accounts for to filled space
        
        # best_movement = (random.randint(0, state.board.col), random.choice([ShapeConstant.CROSS, ShapeConstant.CIRCLE])) #minimax algorithm
        # return best_movement

        # self.thinking_time = time() + thinking_time
        col = board.col 
        row = board.row
        positionArray = self.getPositionArrayFromBoard(board)
        # print(self.referenceMap)
        print(positionArray)
        self.findAllPossiblePositions(positionArray, row, col, color, 4)
        print(self.totalPositions)
        print(self.bestMove)
        print(self.bestMoveScore)
        with open("database.json", "w") as outfile:
            json.dump(self.database, outfile)

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

    def findAllPossiblePositions(self, positionArray, row, column, color, depth = 3 ) : 
        
        if depth == 0 : 
            # # print(intialPosition)
            # global totalPositions, samples
            # totalPositions += 1
            # if( random.randint(0,10) > 8 ) : 
            #     samples.append(initialPosition)
            self.totalPositions +=1 
            score = self.getScore(positionArray)
            self.database[self.hashPositionMap(positionArray)] = score
            return self.getScore(positionArray)
    
        for j in range(col) : 
            nextColor = ColorConstant.RED if color == ColorConstant.BLUE else ColorConstant.BLUE
            # print(color, nextColor)
            # Get position with shape X
            pieceX = self.getPieceRepresentation(Piece(ShapeConstant.CROSS, color))
            positionArray[j].append(pieceX)
            hashValue = self.hashPositionMap(positionArray)
            # if( hashValue in self.database.keys()) :
            #     scoreX = self.database[hashValue]
            # else : 
            scoreX = self.findAllPossiblePositions(positionArray, row, column, nextColor, depth-1)
            # print(positionArray, nextColor, j, scoreX, pieceX)
            positionArray[j].pop()
            
            if( self.bestMoveScore < scoreX ) : 
                self.bestMoveScore = scoreX
                self.bestMove = ( j, pieceX )

            # Get position with shape Y 
            pieceY = self.getPieceRepresentation(Piece(ShapeConstant.CIRCLE, color))
            positionArray[j].append(pieceY)
            hashValue = self.hashPositionMap(positionArray)
            # if( hashValue in self.database.keys()) :    
            #     scoreY = self.database[hashValue]
            # else : 
            scoreY = self.findAllPossiblePositions(positionArray, row, column, nextColor, depth-1)
            positionArray[j].pop()
            if( self.bestMoveScore < scoreY ) : 
                self.bestMoveScore = scoreY
                self.bestMove = ( j, pieceY )
        #This should not been possible
        return self.bestMoveScore

# bestMove = None
# currentTurn = 0
# totalPositions = 0
# samples = []
row = 6
col = 7
board = Board(row, col)
minimax = Minimax()
minimax.find(board, ColorConstant.RED)

# def findAllPossiblePositions(intialPosition, row, column, color, depth = 3 ) : 
#     # print(color)
#     # print(initialPosition)
#     if depth == 0 : 
#         # print(intialPosition)
#         global totalPositions, samples
#         totalPositions += 1
#         if( random.randint(0,10) > 8 ) : 
#             samples.append(initialPosition)
#         return 
#     # nextMove = random.randint(0,1) + 1 if color == ColorConstant.RED  else ( 3 if color == ColorConstant.BLUE else -1 )
#     # randomColumn = random.randint(1,column)
#     # initialPosition[randomColumn].append(nextMove)
   
#     for i in range(column) :
#         for k in range(0,2) :
#             nextMove = k + 1 if color == ColorConstant.RED  else ( 3 if color == ColorConstant.BLUE else -1 )
#             # This is so stupid
#             colArray = initialPosition[i]
#             if( len(colArray) > 1 ) : 
#                 initialPosition[i][len(colArray)-1]  = nextMove
#             else :
#                 initialPosition[i].append(nextMove)
#             nextColor = ColorConstant.RED if color == ColorConstant.BLUE else ColorConstant.BLUE
#             findAllPossiblePositions(initialPosition, row, column, nextColor, depth-1)
#             # initialPosition[i].pop()



# def getMove(self) :
#     return random.randint(1,4)
        
        


# initialPosition = [[] for i in range(column)]
# color = ColorConstant.RED 
# print(initialPosition)
# findAllPossiblePositions(initialPosition, row, column, ColorConstant.RED, 2)
# print(totalPositions)
# print(samples)

#  Yeah this is a problem
# a = [1,2,3,4 ]
# b = a
# b.append(10)
# print(a)

# for i in range(7) : 
#     print(i)