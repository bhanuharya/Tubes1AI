# from os import PRIO_PGRP
import os
from pickle import NONE
import random
from time import time
# from model import player, state

from src.constant import ShapeConstant
# from src.model import State
# from src.utility import is_out, is_win, is_full, place

from typing import Tuple, List
from src.utility import *
from src.model import Piece, Board, State


class LocalSearch:
    def __init__(self):
        pass

    def find(self, state: State, n_player: int, thinking_time: float) -> Tuple[str, str]:
        self.thinking_time = time() + thinking_time
        self.board = state.board
        global_max = []
        global_max.append(LocalSearch.globalMax(self.board, n_player))

        # print(global_max)
        # print(global_max[0][0])
        # print(global_max[0][1])
        # if (global_max[0][0] == 0):
        #     col = random.randint(0, state.board.col)
        #     shape = random.choice([ShapeConstant.CROSS, ShapeConstant.CIRCLE])
        #     #putus callnya?
        #     #iyaa kayanya
        #     #shape juga di random
        # elif(global_max[0][0] > 0):
        col = global_max[0][2]
        shape = global_max[0][1]

        best_movement = (col, shape) #minimax algorithm

        return best_movement


    """
    1. Cek setiap kolom yang row nya 1 kotak di atas row piece paling tinggi yang sudah terisi di kolom tersebut 
    2. Di kolom tersebut menetapkan nilai pattern streak yang paling tinggi dengan mengecek ke 4 arah (horizontal, vertical bawah, gradien +, gradien -)
    3. Simpan titik dan piece (shape or color) yang memiliki nilai tertinggi (Local Max)
    4. Dari local max yang tersedia dari setiap kolom, kita pilih kolom yang memiliki nilai paling besar (global max)
W
WS
    """

    def local_max(board: Board, n_player: int, row: int, col: int) -> List:
        streak_way = [(-1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        # Arah atas tidak di cek karena sudah pasti kosong

        if n_player == 0:
            player_set= [GameConstant.PLAYER1_SHAPE, GameConstant.PLAYER1_COLOR]
            p_piece = GameConstant.PLAYER1_SHAPE
            p_color = GameConstant.PLAYER1_COLOR
        elif n_player == 1:
            player_set= [GameConstant.PLAYER2_SHAPE, GameConstant.PLAYER2_COLOR]
            p_piece = GameConstant.PLAYER2_SHAPE
            p_color = GameConstant.PLAYER2_COLOR
         

    
        # 5 arah (horizontal, vertical bawah, gradien +, gradien -)
        sevenWay = []
        fourWay = []
        priorMax = ()
        arr_priorMax = []
        for piece in player_set:
            
            #pengecekan arah
            for row_ax, col_ax in streak_way:
                mark = 0
                row_ = row + row_ax
                col_ = col + col_ax
                for _ in range(GameConstant.N_COMPONENT_STREAK - 1):
                    # print(board)
                    if (row_ < 0 or row_ >= board.row or col_ < 0 or col_ >= board.col):
                        mark += 0
                        break

                    shape_condition = (
                        piece == p_piece
                        and piece != board[row_, col_].shape
                    )
                    color_condition = (
                        piece == p_color
                        and piece != board[row_, col_].color
                    )
                    if shape_condition or color_condition:
                        mark = 0
                        break
            
                    row_ += row_ax
                    col_  += col_ax
                    mark += 1
                sevenWay.append(mark)
                

            #fourWay = horizontal, vertical, gradien +, gradien -
            fourWay.append(sevenWay[1] + sevenWay[2]) #Horizontal
            fourWay.append(sevenWay[0]) #Vertical
            fourWay.append(sevenWay[3] + sevenWay[6]) #Diagonal +
            fourWay.append(sevenWay[4] + sevenWay[5]) #Diagonal -
            maks = max(fourWay)
            priorMax = (maks, piece, col, row)
            arr_priorMax.append(priorMax)
        # print(sevenWay)
        # print(arr_priorMax)
        
            
        if arr_priorMax[0][0] >= arr_priorMax[1][0]:
            # print(arr_priorMax[0])
            return(arr_priorMax[0])
        elif arr_priorMax[0][0] < arr_priorMax[1][0]:
            prioL  = ( arr_priorMax[1][0],random.choice([ShapeConstant.CROSS, ShapeConstant.CIRCLE]),arr_priorMax[1][2] )
            # print(prioL)
            return(prioL)


    def globalMax(board: Board, n_player: int) -> Tuple[int,str,int, ]:
        # rows = 5
        res = []
        resValue = [None] * 7
        temp = [0]
        for cols in range(7):
            rows = 5
            found = False
            while (rows >= 0 and found == False):
                piece = board[rows, cols]
                # print(piece.shape)
                if (piece.shape == ShapeConstant.BLANK):
                    found = True
                # elif(piece.shape == ShapeConstant.CROSS or piece.shape == ShapeConstant.CIRCLE):
                #     print(piece.shape)
                else:
                    rows -= 1
            res.append(LocalSearch.local_max(board, n_player,rows, cols))
        # print(res)
        for i in range(len(res)):
            resValue[i]= res[i][0]
        for i in range(len(res)):
            if resValue[i] > temp[0]:
                temp[0] = resValue[i]
                
            # elif resValue[i] == temp[0]:
            #     if res[i][1] == GameConstant.PLAYER1_COLOR :
            #         if temp[1] == GameConstant.PLAYER1_SHAPE:
            #             temp[0] = res[i]

        i = 0
        find = False
        while(i < len(res) and find == False):
            if(temp[0] == res[i][0]):
                find = True
            i += 1
        
        idx = i-1      

        # if res[idx][0] == 0:
        #     idx  = random.randint(0, 6)

        #col dan shape
        # print("")
        # print(res[idx])
        return res[idx]

"""

1. check setiap kolom, apakah ada kesamaan pola dari segala arah
2. Hitung nilai dari bobot kesamaan pola dari segala arah
3. Nilai yang paling tinggi diambil (col, shape)


"""