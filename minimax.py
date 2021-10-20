import random
from time import time

from src.constant import ShapeConstant
from src.model import State

from typing import Tuple, List

# Added Code 
from src.constant import ColorConstant
from src.model import board
from src.mechanic import Game
import json 

###
#  Save a state of a in string representation 
#  The string representation is as follows : "A;B;C;D;E...n" where A-E indicates column 1-n and ; as their separation mark
#  Each column consist of 1-m rows, which will store representation of pieces in 1-4 counted from the bottom up 
#  String representation of each piece is as follows : 
#  1 : Red Circle 
#  2 : Blue Circle
#  3 : Red Cross 
#  4 : Blue Cross 
#  0 : Empty Column
#  Example : "1;0;21;23;0;2" indicates the following position in the board 
# | - | - | - | - | - | - |
# | - | - | - | - | - | - |
# | - | - | - | - | - | - |
# | - | - | - | - | - | - |
# | - | - | - | - | - | - |
# | - | - | 1 | 3 | - | - |
# | 1 | - | 2 | 2 | - | 2 |  
# The Minimax Result of a position will be saved in a seperate JSON file with the following format
# ! Problem, We might not know whether the current position come from a maximizing or a minimizing player. 
# The Idea is that if we know the heuristic Minimax Score of a position, we don't need to calculate it again. 
# The heuristic Minimax score is a different score from the score being spitted out by the 
# Position = (Min Score, maxScore, String Representation of The Board State )
# A Board State will be coded using a hashing function that sums the total of number in the string representation of the board.
# The Hashing function is used to minimize the ammount of search we need to do  
# All of the state with the same sum will be assigned to the same dictionary key. 
# The maximum array size to fit all of the calculated scores are nxm where n is the columns and m is the rows. 
# Each index will store a dictionary in this format :
# String Representation of the State : (Min Score, Max Score )
# The Maximum Size of the Database is 4^(n*m)
# To Cut off storage size for the database, we will remove all of the states that can be manually calculated using the Minimax Algorithm, 
# Which is all the states that can be reached using depth 3
# Dictionary will use a lot more space in memory even though the time needed is much smaller
###


class Minimax:
    def __init__(self):
        # Need information of what the current player SHAPE is 
        self.board = None
        self.isLearning = True # Used to train the bot and populate the Database JSON. Set to False if the bot is currently playing. 
        self.database = {} # The current database object to lookup positions 
        self.bestMove = (1, ShapeConstant.CROSS)
        self.bestMoveScore = float("-inf")
        # self.game = Game
        pass

    def loadDatabase(self) : 
        # Function to load the database from a JSON file that saves the positions that has been calculated by the AI 
        return 0

    def saveToDatabase(self) :
        with open('data.json', 'w') as result :
            json.dump(self.database, result)
        return 0
    
    def hashPosition(self, positionString) :
        sum = 0
        for i in positionString:
            if(i == ";") : 
                continue
            sum += int(i)
        return sum
    
    def getPositionString(self, board, numOfRows, numOfColumns) : 
        #  1 : Red Circle 
        #  2 : Blue Circle
        #  3 : Red Cross 
        #  4 : Blue Cross 
        #  0 : Empty Column
        #  Remove all of the unessesary 0s later 
        positionArray = [[] for i in range(numOfRows)]
        for row in range(numOfRows) :
            for piece in board[row] : 
                if( piece.Shape == ShapeConstant.CIRCLE and piece.color == ColorConstant.RED ) :
                    positionArray[row] = "1"
                elif( piece.Shape == ShapeConstant.CIRCLE and piece.color == ColorConstant.BLUE ) :
                    positionArray[row] = "2"
                elif( piece.Shape == ShapeConstant.CROSS and piece.color == ColorConstant.RED ) :
                    positionArray[row] = "3"
                elif( piece.Shape == ShapeConstant.CROSS and piece.color == ColorConstant.BLUE) :
                    positionArray[row] = "4"
                else : 
                    positionArray[row] = "0"
        positionString = ""
        for row in positionArray:
            for col in positionArray : 
                positionString += positionArray[row][col]
            positionString += ";"
        return (positionArray, positionString)
    
    def getNextMove(self, currentSuccessor, numOfColumns) :
        # Return The Shape and Column for the next move
        column = currentSuccessor % numOfColumns
        shape = ShapeConstant.CROSS
        # Still broken. 1 % 2 == 1 % 5 
        if(currentSuccessor % 2 == 1) :
            shape = ShapeConstant.CROSS
        else :
            shape = ShapeConstant.CIRCLE
        
        return ( shape, column )
        

    def find(self, state: State, n_player: int, thinking_time: float) -> Tuple[str, str]:
        # [RETURN] : the choosen shape and column that the bot wants to play (choosen_col, choosen_shape)
        # choosen_col, choosen_shape = self.bot[player_turn].find(
        #     self.state, player_turn, self.config.thinking_time
        # )
        
        # best_movement = (random.randint(0, state.board.col), random.choice([ShapeConstant.CROSS, ShapeConstant.CIRCLE])) #minimax algorithm
        # return best_movement

        self.thinking_time = time() + thinking_time
        positionArray, positionString = self.getPositionString(state.board)
        for i in range(state.board.col) :
            maxScore = float("-inf")
            if( positionString in self.database.keys()) : 
                maxScore = self.database[positionString].maxScore
            else :
                score = Minimax(positionArray)
                maxScore = max(score, maxScore)


        return self.bestMove


    def heuristicFunction(self, board) :
        return random.randint(-100,100)


    def Minimax(self, positionString,  alpha = float("-inf"), beta = float("inf"), isMaximizing = True, depth = 3):
        if(depth == 0) :
            return self.getScore(board)
        elif (isMaximizing) :
            for i in 10 : 
                maxScore = float("-inf")
                score = Minimax(board, alpha, beta, not isMaximizing, depth-1)
                maxScore = max(score, maxScore)
                alpha = max(alpha, maxScore)
                if(alpha >= beta) :
                    break 
                return maxScore
        else :
            for i in 10 : 
                minScore = float("inf")
                score = Minimax(board, alpha, beta, not isMaximizing, depth-1)
                minScore = min(score, minScore)
                beta = min(beta, minScore)
                if(alpha >= beta) :
                    break 
                return minScore
