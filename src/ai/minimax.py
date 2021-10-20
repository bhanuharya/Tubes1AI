import random, json, copy, os
from time import time

from src.constant import ShapeConstant, ColorConstant
from src.model import State, Board, Piece

from typing import Tuple, List


class Minimax:
    def __init__(self, isLearning = False):
        self.isLearning = isLearning # Used to train the bot and populate the Database JSON. Set to False if the bot is currently playing. 
        self.database = {} # The current database object to lookup positions 
        self.depth = 3

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
    
    def find(self, state, player_turn, thinking_time):
        if(state.round <= 4) :
            return (random.randint(0,state.board.col), random.choice([ShapeConstant.CIRCLE, ShapeConstant.CROSS]))
        # Preparation
        self.start_time = time()
        self.thinking_time = thinking_time

        # Player piece shape and color
        self.shape = state.players[player_turn].shape
        self.color = state.players[player_turn].color 
        self.pieceQuota = state.players[player_turn].quota 

        # Board
        self.col = state.board.col
        self.row = state.board.row
        positionArray = self.getPositionArrayFromBoard(state.board)
        if( not os.path.exists('./reference_map.json')) : 
            self.getReferenceMap(self.row, self.col, 4)
        self.loadReferenceMap()

        # Initiates the reuslts 
        self.totalPositions = 0
        self.bestMove = (0,0) # Just a placeholder value ( Column, Shape and Color )
        self.bestMoveScore = float("-inf")
        # Minimax
        
        # self.totalPositions = 14**depth # Basic math; What it should be. Already confirmed
        for depth in range(1, self.depth+1):
            self.database = {}
            if time() - self.start_time > self.thinking_time: 
                break
            successors = self.generateSucessors(positionArray)
            # print(successors, len(successors), depth)
            for successor in successors:
                score = self.Minimax(self.color, successor["position"], depth=depth)
                # print(successor, score, depth)
                if score > self.bestMoveScore:
                    
                    column = successor["column"]
                    piece = successor["piece"]
                    self.bestMoveScore = score
                    self.bestMove = (int(column), self.getPieceRepresentation(piece)[0])
            # print(self.bestMove, depth)
        return self.bestMove

    # Scoring System based on the number of streaks
    def getPositionScore(self, positionArray) : 
        score = 0
        for i in range(len(positionArray)) : 
            row = positionArray[i]
            for j in range(len(row)) : 
                currentValue = positionArray[i][j]
                position = (i,j)
                streak_way = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
               
                # Preparation
                currentNodePiece = self.getPieceRepresentation(currentValue)
                pieceShape = 1 if currentNodePiece[0] == ShapeConstant.CIRCLE else 3
                pieceColor = 1 if currentNodePiece[1] == ColorConstant.RED else 2 
                playerShape = 1 if self.shape == ShapeConstant.CIRCLE else 3
                playerColor = 1 if self.color == ColorConstant.RED else 2 
                
                for move in streak_way :
                    (x, y) = (position[0] + move[0], position[1] + move[1])
                    # Check if the moved position is available
                    if x < 0 or y < 0 :
                        continue
                    try :
                        value = positionArray[x][y]  
                    except IndexError :
                        continue

                    
                    colorStreak = True
                    shapeStreak = True
                    for streak in range(5) : 
                        scoreIncrement = streak
                        
                        player_turn = self.depth % 2
                        if shapeStreak and ( value == pieceShape or value == pieceShape + 1 ):
                            if( pieceShape == playerShape ) :
                                score = score + 2000 if scoreIncrement == 4 else score + scoreIncrement
                            else :
                                score = score - 5000  if scoreIncrement == 4 else score - 10*scoreIncrement
                        else :
                            shapeStreak = False 

                        if  colorStreak and ( value == pieceColor or value == pieceColor + 2 ) : 
                            if(pieceColor == playerColor ) :
                                score = score + 2000  if scoreIncrement == 4 else score + scoreIncrement
                            else :
                                score = score - 5000  if scoreIncrement == 4 else score - 10*scoreIncrement
                        else :
                            colorStreak = False
        return score

    def getTotalPiecesInBoard(self, positionArray) :
        total = 0
        for i in range(len(positionArray)) : 
            row = positionArray[i]
            for j in range(len(row)) :
                total += 1
        return total

    def generateSucessors(self, positionArray ) :
        successors = []
        for j in range(self.col*2) :
            piece = Piece(ShapeConstant.CROSS if j % 2 == 1 else ShapeConstant.CIRCLE , self.color)
            index = j/2 if j % 2 == 0 else (j-1)/2
            index = int(index)
            if(len(positionArray[index]) >= self.row or self.pieceQuota[piece.shape] <= 0 ) :
                continue
            piece = self.getNumberRepresentation(piece)
            positionArray[index].append(piece)
            hashValue = self.hashPositionMap(positionArray)
            successors.append({
                "position" : copy.deepcopy(positionArray), 
                "hashValue" : hashValue,
                "column" : index,
                "piece" : piece
            })
            positionArray[index].pop()
        
        return successors


    def Minimax(self, color, positionArray, alpha = float("-inf"), beta = float("inf"), isMaximizing = True, depth = 3):
        # Using Fail-Soft Alpha Beta
        if(depth <= 0) or time() - self.start_time >= self.thinking_time:
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
            for successor in self.generateSucessors(positionArray) :
                position = successor["position"]
                hashValue = successor["hashValue"]
                
                nextColor = ColorConstant.RED if color == ColorConstant.BLUE else ColorConstant.BLUE
                if( hashValue in self.database.keys()) :
                    score = self.database[hashValue]["score"]
                else : 
                    score = self.Minimax(nextColor, position, alpha, beta, not isMaximizing, depth-1)
                # Compares the scores 
                maxScore = max(score, maxScore)
                if( score > maxScore ) :
                    maxScore = score
                alpha = max(alpha, maxScore)
                if(maxScore >= beta) :
                    break 
            return maxScore
        else :
            minScore = float("inf")
            for successor in self.generateSucessors(positionArray) :
                position = successor["position"]
                hashValue = successor["hashValue"] 
                nextColor = ColorConstant.RED if color== ColorConstant.BLUE else ColorConstant.BLUE
                if( hashValue in self.database.keys()) :
                    score = self.database[hashValue]["score"]
                else : 
                    score = self.Minimax(nextColor, position, alpha, beta, not isMaximizing, depth-1)
                # Compares the scores 
                minScore = min(score, minScore)
                beta = min(beta, minScore)
                if(minScore <= alpha) :
                    break 
            return minScore
