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
        if(state.round <= 2) :
            return (random.randint(0,state.board.col), random.choice([ShapeConstant.CIRCLE, ShapeConstant.CROSS]))
        # Preparation
        currentTime = time()
        # Player piece shape and color
        self.shape = state.players[player_turn].shape
        self.color = state.players[player_turn].color  
        # The col and row needs to be reversed. 
        col = state.board.col
        row = state.board.row
        positionArray = self.getPositionArrayFromBoard(state.board)
        
        if( not os.path.exists('./reference_map.json')) : 
            self.getReferenceMap(row, col, 4)
        self.loadReferenceMap()

        # Initiates the reuslts 
        self.totalPositions = 0
        self.bestMove = (0,0) # Just a placeholder value ( Column, Shape and Color )
        self.bestMoveScore = float("-inf")

        # Minimax
        # print(positionArray)
        self.Minimax(self.color, positionArray, row, col, depth = self.depth)
        # self.totalPositions = 14**depth # Basic math; What it should be. Already confirmed
        # print("Time : ",time() - currentTime, "Seconds")
        return self.bestMove

    # Scoring System based on the number of streaks
    def getPositionScore(self, positionArray) : 
        def checkStreak(currentNode, positionArray, visited = [], streak = 2 ) :  
            streak_way = [(-1, 0), (0, -1), (0, 1), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]
            queue = {}
            # Preparation
            currentNodePiece = self.getPieceRepresentation(currentNode["value"])
            pieceShape = 1 if currentNodePiece[0] == ShapeConstant.CIRCLE else 3
            pieceColor = 1 if currentNodePiece[1] == ColorConstant.RED else 2 
            shapeNumber = 1 if self.shape == ShapeConstant.CIRCLE else 3
            colorNumber = 1 if self.color == ColorConstant.RED else 2 
            
            score = 0
            visited.append(currentNode)
            for move in streak_way :
                scoreIncrement = streak
                streakFlag = False
                if scoreIncrement == 4 :
                    scoreIncrement = float("inf")
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
                player_turn = self.depth % 2
                if value == pieceShape or value == pieceShape + 1 : 
                    streakFlag = True
                    if( pieceShape == shapeNumber ) :
                        score = score + 200 if scoreIncrement == float("inf") else score + scoreIncrement
                    else :
                        score = score - 200  if scoreIncrement == float("inf") else score - 10*scoreIncrement
                    

                if value == colorNumber or value == colorNumber + 2 : 
                    streakFlag = True
                    if(pieceColor == colorNumber) :
                        score = score + 200  if scoreIncrement == float("inf") else score + scoreIncrement
                    else :
                        score = score - 200  if scoreIncrement == float("inf") else score - scoreIncrement
                
                if(streakFlag) :
                    key = str(x) + "," + str(y)
                    queue[key] = value

            while len(queue) > 0 :
                key = list(queue.keys())[0]
                position = (int(key[0]), int(key[2]))
                nextNode = {"position" : position, "value" : queue.pop(key)}
                score += checkStreak(nextNode, positionArray, visited, streak + 1)
            
            return score

                

        totalScore = 0
        for x in range(len(positionArray)) : 
            row = positionArray[x]
            for y in range(len(row)) : 
                value = positionArray[x][y]
                totalScore += checkStreak(currentNode = {"position" : (x,y), "value" : value},  positionArray = positionArray )
                
        return totalScore

    # Uses Minimax  
    def getNextIterationScore(self, piece, nextColor, index, positionArray, row, col, alpha, beta, isMaximizing, depth) : 
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
                index = j/2 if j % 2 == 0 else (j-1)/2
                index = int(index)
                if(len(positionArray[index]) >= row) :
                    continue
                score = self.getNextIterationScore(piece, nextColor, index, positionArray, row, col, alpha, beta, isMaximizing, depth)

                # Compares the scores 
                maxScore = max(score, maxScore)
                if( score > maxScore ) :
                    maxScore = score
                if( maxScore > self.bestMoveScore  ) :
                    self.bestMoveScore = maxScore 
                    self.bestMove = (int(index), self.getPieceRepresentation(piece)[0])
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
                index = int(index)
                if(len(positionArray[index]) >= row) :
                    continue
                score = self.getNextIterationScore(piece, nextColor, index, positionArray, row, col, alpha, beta, isMaximizing, depth)

                # Compares the scores 
                minScore = min(score, minScore)
                beta = min(beta, minScore)
                if(minScore <= alpha) :
                    break 
            return minScore
