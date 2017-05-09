import numpy as np

class Agent(object):

    def __init__(self, role):
        self.role = role
        self.opponent = self.role % 2 + 1
        self.role_strs = {1: 'Black', 2: 'White'}
        self.role_str = self.role_strs[role]

    def move(self, board, turn_number):
        pass

    def get_initial_valid_moves(board):
        validity = np.zeros((board.shape[0], board.shape[1]), dtype=bool)
        dim = board.shape[0]
        for i in range(int(dim / 2) - 1, int(dim / 2) + 1):
            for j in range(int(dim / 2) - 1, int(dim / 2) + 1):
                if (board[i,j] == 0):
                    validity[i,j] = True
        return validity

    def get_valid_moves(board, role):
        validity = np.zeros((board.shape[0], board.shape[1]), dtype=bool)
        for i in range(board.shape[0]):
            for j in range(board.shape[1]):
                if (board[i,j] == 0):
                    if (Agent.can_claim(board, role, i, j)):
                        validity[i,j] = True
        return validity

    def can_claim(board, role, i, j):
        opponent = role % 2 + 1
        for x_dif in range(-1,2):
            for y_dif in range(-1,2):
                if (not (x_dif == 0 and y_dif == 0)):
                    x = x_dif + i
                    y = y_dif + j
                    if ((x >= 0 and x < board.shape[0]) and (y >= 0 and y < board.shape[1])):
                        if (board[x,y] == opponent):
                            while(True):
                                x += x_dif
                                y += y_dif
                                if ((x >= 0 and x < board.shape[0]) and (y >= 0 and y < board.shape[1])):
                                    if (board[x,y] == opponent):
                                        continue
                                    elif (board[x,y] == role):
                                        return True
                                break
        return False

    def update_board(board, move, role):
        opponent = role % 2 + 1
        board[move[0], move[1]] = role
        for x_dif in range(-1,2):
            for y_dif in range(-1,2):
                if (not (x_dif == 0 and y_dif == 0)):
                    x = x_dif + move[0]
                    y = y_dif + move[1]
                    if ((x >= 0 and x < board.shape[0]) and (y >= 0 and y < board.shape[1])):
                        if (board[x,y] == opponent):
                            if (Agent.walk_board(board, x, y, x_dif, y_dif, role, opponent)):
                                board[x,y] = role

    def walk_board(board, x, y, x_dif, y_dif, role, opponent):
        x += x_dif
        y += y_dif
        if ((x >= 0 and x < board.shape[0]) and (y >= 0 and y < board.shape[1])):
            if (board[x,y] == opponent):
                if Agent.walk_board(board, x, y, x_dif, y_dif, role, opponent):
                    board[x,y] = role
                    return True
            elif (board[x,y] == role):
                return True
            else:
                return False



