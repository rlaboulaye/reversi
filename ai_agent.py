import numpy as np

from agent import Agent

class Node(object):

    def __init__(self, board, depth, max_depth, player_role):
        self.MIN = 1
        self.MAX = 0
        self.role = depth % 2
        self.depth = depth
        self.board = board
        self.max_depth = max_depth
        self.player_role = player_role
        self.opponent_role = (player_role % 2) + 1

    def get_utility(self, turn_number):
        if (self.depth >= self.max_depth):
            return self.estimate_utility(self.board)
        if (turn_number < 5):
            valid_moves = Agent.get_initial_valid_moves(self.board)
        else:
            if (self.role == self.MAX):
                valid_moves = Agent.get_valid_moves(self.board, self.player_role)
            else:                
                valid_moves = Agent.get_valid_moves(self.board, self.opponent_role)
        if (not np.any(valid_moves)):
            board = np.copy(self.board)
            child = Node(board, self.depth + 1, self.max_depth, self.player_role)
            return child.get_utility(turn_number + 1)
        moves = []
        for i in range(valid_moves.shape[0]):
            for j in range(valid_moves.shape[1]):
                if (valid_moves[i,j]):
                    moves.append([i,j])
        if self.role == self.MIN:
            self.best_utility = 1000000
        else:
            self.best_utility = -1000000
        for move in moves:
            board = np.copy(self.board)
            if (self.role == self.MAX):
                Agent.update_board(board, move, self.player_role)
            else:                
                Agent.update_board(board, move, self.opponent_role)
            child = Node(board, self.depth + 1, self.max_depth, self.player_role)
            utility = child.get_utility(turn_number + 1)
            if self.is_better(utility):
                self.best_move = move
        return self.best_utility

    def estimate_utility(self, board):
        player_piece_count = (board == self.player_role).sum()
        opponent_piece_count = (board == self.opponent_role).sum()
        return player_piece_count / (player_piece_count + opponent_piece_count)

    def is_better(self, utility):
        if self.role == self.MIN:
            if (utility < self.best_utility):
                self.best_utility = utility
                return True
        else:
            if (utility > self.best_utility):
                self.best_utility = utility
                return True
        return False



class AIAgent(Agent):

    def __init__(self, role):
        super(AIAgent, self).__init__(role)
        self.max_depth = 5

    def move(self, board, turn_number):
        if (turn_number < 5):
            valid_moves = Agent.get_initial_valid_moves(board)
        else:
            valid_moves = Agent.get_valid_moves(board, self.role)
        if (not np.any(valid_moves)):
            return False
        board_cp = np.copy(board)
        root = Node(board_cp, 0, self.max_depth, self.role)
        root.get_utility(turn_number)
        move = root.best_move
        Agent.update_board(board, move, self.role)
        return True
