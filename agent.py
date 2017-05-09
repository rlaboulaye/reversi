import numpy as np

class Agent(object):

    def __init__(self, role):
        self.role = role
        self.opponent = self.role % 2 + 1
        self.role_strs = {1: 'Black', 2: 'White'}
        self.role_str = self.role_strs[role]

    def get_move(self, board):
        pass

    def get_valid_moves(self, board):
        validity = np.zeros((board.shape[0], board.shape[1]), dtype=bool)
        for i in range(board.shape[0]):
            for j in range(board.shape[1]):
                if (board[i,j] == 0):
                    if (self.can_claim(board, i, j)):
                        validity[i,j] = True
        return validity

    def can_claim(self, board, i, j):
        for x_dif in range(-1,2):
            for y_dif in range(-1,2):
                if (not (x_dif == 0 and y_dif == 0)):
                    x = x_dif + i
                    y = y_dif + j
                    if ((x >= 0 and x < board.shape[0]) and (y >= 0 and y < board.shape[1])):
                        if (board[x,y] == self.opponent):
                            while(True):
                                x += x_dif
                                y += y_dif
                                if ((x >= 0 and x < board.shape[0]) and (y >= 0 and y < board.shape[1])):
                                    if (board[x,y] == self.opponent):
                                        continue
                                    elif (board[x,y] == self.role):
                                        return True
                                break
        return False

    def update_board(self, board, move):
        board[move[0], move[1]] = self.role
        for x_dif in range(-1,2):
            for y_dif in range(-1,2):
                if (not (x_dif == 0 and y_dif == 0)):
                    x = x_dif + move[0]
                    y = y_dif + move[1]
                    if ((x >= 0 and x < board.shape[0]) and (y >= 0 and y < board.shape[1])):
                        if (board[x,y] == self.opponent):
                            if (self.walk_board(board, x, y, x_dif, y_dif)):
                                board[x,y] = self.role

    def walk_board(self, board, x, y, x_dif, y_dif):
        x += x_dif
        y += y_dif
        if ((x >= 0 and x < board.shape[0]) and (y >= 0 and y < board.shape[1])):
            if (board[x,y] == self.opponent):
                if walk_board(board, x, y, x_dif, y_dif):
                    board[x,y] = self.role
                    return True
            elif (board[x,y] == self.role):
                return True
            else:
                return False



