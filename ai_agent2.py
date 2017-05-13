import numpy as np

from agent import Agent
from time import time

class Node(object):

    def __init__(self, move, board, depth, max_depth, player_role):
        self.depth = depth
        self.move = move
        self.board = board
        self.max_depth = max_depth
        self.player_role = player_role
        self.opponent_role = (player_role % 2) + 1

    def get_max(self, turn_number, beta, order=True):
        if (self.depth >= self.max_depth):
            return self.estimate_utility(self.move, self.board, turn_number)
        min_val = -1000000
        if (turn_number < 5):
            valid_moves = Agent.get_initial_valid_moves(self.board)
        else:
            valid_moves = Agent.get_valid_moves(self.board, self.player_role)
        if (not np.any(valid_moves)):
            board = np.copy(self.board)
            child = Node(None, board, self.depth + 1, self.max_depth, self.player_role)
            return child.get_min(turn_number + 1, min_val, order)
        moves = []
        for i in range(valid_moves.shape[0]):
            for j in range(valid_moves.shape[1]):
                if (valid_moves[i,j]):
                    moves.append([i,j])
        if order:
            moves = self.order_moves(moves, self.board, turn_number)
        for move in moves:
            if (beta <= min_val):
                break
            board = np.copy(self.board)
            Agent.update_board(board, move, self.player_role)
            child = Node(move, board, self.depth + 1, self.max_depth, self.player_role)
            utility = child.get_min(turn_number + 1, min_val, order)
            if (utility > min_val):
                min_val = utility
                self.best_move = move
        return min_val

    def get_min(self, turn_number, alpha, order=True):
        if (self.depth >= self.max_depth):
            return self.estimate_utility(self.move, self.board, turn_number)
        max_val = 1000000
        if (turn_number < 5):
            valid_moves = Agent.get_initial_valid_moves(self.board)
        else:
            valid_moves = Agent.get_valid_moves(self.board, self.opponent_role)
        if (not np.any(valid_moves)):
            board = np.copy(self.board)
            child = Node(None, board, self.depth + 1, self.max_depth, self.player_role)
            return child.get_max(turn_number + 1, max_val, order)
        moves = []
        for i in range(valid_moves.shape[0]):
            for j in range(valid_moves.shape[1]):
                if (valid_moves[i,j]):
                    moves.append([i,j])
        if order:
            moves = self.order_moves(moves, self.board, turn_number, maximize=False)
        for move in moves:
            if (alpha >= max_val):
                break
            board = np.copy(self.board)
            Agent.update_board(board, move, self.opponent_role)
            child = Node(move, board, self.depth + 1, self.max_depth, self.player_role)
            utility = child.get_max(turn_number + 1, max_val, order)
            if (utility < max_val):
                max_val = utility
                self.best_move = move
        return max_val

    def order_moves_deprecated(self, moves, board, turn_number):
        ordered_moves = []
        for move in moves:
            board_cp = np.copy(board)
            if (self.role == self.MAX):
                Agent.update_board(board_cp, move, self.player_role)
            else:                
                Agent.update_board(board_cp, move, self.opponent_role)
            if (self.role == self.MIN):
                root = Node(move, board_cp, 0, 1, self.player_role, 1000000, False)
            else:
                root = Node(move, board_cp, 1, 2, self.player_role, -1000000, False)
            utility = root.get_utility(turn_number)
            ordered_moves.append([move[0], move[1], utility])
        reverse_factor = self.role == self.MAX
        ordered_moves.sort(key=lambda x: x[2], reverse=reverse_factor)
        return ordered_moves

    def order_moves(self, moves, board, turn_number, maximize=True):
        ordered_moves = []
        for move in moves:
            board_cp = np.copy(board)
            if (maximize):
                Agent.update_board(board_cp, move, self.player_role)
            else:                
                Agent.update_board(board_cp, move, self.opponent_role)
            utility = self.estimate_utility(move, board_cp, turn_number)
            ordered_moves.append([move[0], move[1], utility])
        ordered_moves.sort(key=lambda x: x[2], reverse=maximize)
        return ordered_moves

    def estimate_utility(self, move, board, turn_number):
        utility = 0
        utility += self.get_ratio(board)
        if (self.move != None):
            utility += self.get_corner_boost(move, board)
            utility += self.get_corner_adjacent_penalty(move, board)
            #utility += self.get_edge_penalty(move, board, turn_number)
        return utility

    def get_ratio(self, board):
        player_piece_count = (board == self.player_role).sum()
        opponent_piece_count = (board == self.opponent_role).sum()
        return player_piece_count / (player_piece_count + opponent_piece_count)

    def get_corner_boost(self, move, board):
        value = 0
        if self.is_corner(move, board):
            value = 1
        return value

    def get_corner_adjacent_penalty(self, move, board):
        value = 0
        if ((move[0] < 2 and move[1] < 2) or 
                (move[0] < 2 and move[1] >= board.shape[1] - 2) or
                (move[0] >= board.shape[0] - 2 and move[1] < 2) or
                (move[0] >= board.shape[0] - 2 and move[1] >= board.shape[1] - 2)):
            if not self.is_corner(move, board):
                value = -.35
        return value

    def get_edge_penalty(self, move, board, turn_number):
        value = 0
        if (turn_number < (board.shape[0] * board.shape[1] / 2)):
            if (move[0] == 0 or move[1] == 0 or move[0] == (board.shape[0] - 1) or move[1] == (board.shape[1] - 1)):
                if not self.is_corner(move, board):
                    value = -.1
        return value

    def is_corner(self, move, board):
        if ((move[0] == 0 and move[1] == 0) or 
                (move[0] == 0 and move[1] == board.shape[1]) or
                (move[0] == board.shape[0] and move[1] == 0) or
                (move[0] == board.shape[0] and move[1] == board.shape[1])):
            return True
        return False


class AIAgent(Agent):

    def __init__(self, role):
        super(AIAgent, self).__init__(role)
        self.max_depth = 6

    def move(self, board, turn_number):
        start_time = time()
        if (turn_number < 5):
            valid_moves = Agent.get_initial_valid_moves(board)
        else:
            valid_moves = Agent.get_valid_moves(board, self.role)
        if (not np.any(valid_moves)):
            return False
        board_cp = np.copy(board)
        root = Node(None, board_cp, 0, self.max_depth, self.role)
        root.get_max(turn_number, 1000000, order=False)
        move = root.best_move
        Agent.update_board(board, move, self.role)
        time_elapsed = time() - start_time
        print('\nElapsed Time: ', time_elapsed)
        return True
