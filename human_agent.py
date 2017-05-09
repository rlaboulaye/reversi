import sys
import numpy as np

from agent import Agent

class HumanAgent(Agent):

    def __init__(self, role):
        super(HumanAgent, self).__init__(role)

    def move(self, board, turn_number):
        if (turn_number < 5):
            valid_moves = Agent.get_initial_valid_moves(board)
        else:
            valid_moves = Agent.get_valid_moves(board, self.role)
        if (not np.any(valid_moves)):
            return False
        self.prompt()
        invalid = True
        while(invalid):
            move = sys.stdin.readline()
            coor = self.get_coordinates(move, board.shape[0])
            if (coor != None and valid_moves[coor[0], coor[1]]):
                invalid = False
            else:
                self.prompt_invalid()
        Agent.update_board(board, coor, self.role)
        return True
    
    def get_coordinates(self, move, dim):
        if (len(move) < 4 and len(move) > 1):
            try:
                row = ord(move[0]) - 97
            except:
                return None
            if (row < 0 or row >= dim):
                return None
            try:
                col = int(move[1:]) - 1
            except:
                return None
            if (col < 0 or col >= dim):
                return None
            return [row, col]

    def prompt(self):
        sys.stdout.write('\n' + self.role_str + ' Player\nPlease enter the coordinates of your next move (i.e. b3):\n')

    def prompt_invalid(self):
        sys.stdout.write('\n Please enter valid coordinates (i.e. a2):\n')
