import numpy as np

from agent import Agent

class Node(object):

    def __init__(self, move, board, depth, max_depth, player_role, alphabeta, order):
        self.MIN = 1
        self.MAX = 0
        self.role = depth % 2
        self.depth = depth
        self.move = move
        self.board = board
        self.max_depth = max_depth
        self.player_role = player_role
        self.opponent_role = (player_role % 2) + 1
        self.alphabeta = alphabeta
        self.order = order

    def get_utility(self, turn_number):
        if (self.depth >= self.max_depth):
            return self.estimate_utility(self.move, self.board, turn_number)
        if self.role == self.MIN:
            self.best_utility = 1000000
        else:
            self.best_utility = -1000000
        if (turn_number < 5):
            valid_moves = Agent.get_initial_valid_moves(self.board)
        else:
            if (self.role == self.MAX):
                valid_moves = Agent.get_valid_moves(self.board, self.player_role)
            else:                
                valid_moves = Agent.get_valid_moves(self.board, self.opponent_role)
        if (not np.any(valid_moves)):
            board = np.copy(self.board)
            child = Node(None, board, self.depth + 1, self.max_depth, self.player_role, self.best_utility, self.order)
            return child.get_utility(turn_number + 1)
        moves = []
        for i in range(valid_moves.shape[0]):
            for j in range(valid_moves.shape[1]):
                if (valid_moves[i,j]):
                    moves.append([i,j])
        if self.order:
            moves = self.order_moves(moves, self.board, turn_number)
        for move in moves:
            if (self.role == self.MIN):
                if (self.alphabeta >= self.best_utility):
                    break
            else:
                if (self.alphabeta <= self.best_utility):
                    break
            board = np.copy(self.board)
            if (self.role == self.MAX):
                Agent.update_board(board, move, self.player_role)
            else:                
                Agent.update_board(board, move, self.opponent_role)
            child = Node(move, board, self.depth + 1, self.max_depth, self.player_role, self.best_utility, self.order)
            utility = child.get_utility(turn_number + 1)
            if self.is_better(utility):
                self.best_move = move
        return self.best_utility

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

    def order_moves(self, moves, board, turn_number):
        ordered_moves = []
        for move in moves:
            board_cp = np.copy(board)
            if (self.role == self.MAX):
                Agent.update_board(board_cp, move, self.player_role)
            else:                
                Agent.update_board(board_cp, move, self.opponent_role)
            utility = self.estimate_utility(move, board_cp, turn_number)
            ordered_moves.append([move[0], move[1], utility])
        reverse_factor = self.role == self.MAX
        ordered_moves.sort(key=lambda x: x[2], reverse=reverse_factor)
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
        root = Node(None, board_cp, 0, self.max_depth, self.role, 1000000, True)
        root.get_utility(turn_number)
        move = root.best_move
        Agent.update_board(board, move, self.role)
        return True
