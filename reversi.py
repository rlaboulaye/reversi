import sys
import numpy as np
from human_agent import HumanAgent

class Game(object):
    
    def __init__(self, size):
        self.max_size = 26
        if (size > self.max_size):
            sys.exit('Board dimension cannot exceed 26')
        self.size = size
        self.EMPTY = 0
        self.BLACK = 1
        self.WHITE = 2
        self.piece_dict = {0: '_', 1: 'B', 2: 'W'}
        self.initialize_board()
        self.players = {self.BLACK: HumanAgent(self.BLACK), self.WHITE: HumanAgent(self.WHITE)}
        self.play()

    def initialize_board(self):
        self.board = np.zeros((self.size, self.size))

    def play(self):
        available_slots = self.size ** 2
        ##
        self.board = np.array([[0,0,0,0],[0,2,1,0],[0,1,2,0],[0,0,0,0]])
        available_slots -= 4
        ##
        sys.stdout.write('Starting Game')
        turn = self.BLACK
        while (available_slots > 0):
            self.print_board()
            self.board = self.players[turn].get_move(self.board)
            available_slots -= 1
            turn = turn % 2 + 1
        self.print_board()
        self.declare_winner()

    def declare_winner(self):
        black_tiles = (self.board == self.BLACK).sum()
        white_tiles = (self.board == self.WHITE).sum()        
        if (black_tiles > white_tiles):
            output = '\n---BLACK WINS---\n'
        elif (white_tiles > black_tiles):
            output = '\n---WHITE WINS---\n'
        else:
            output = '\n---DRAW---\n'
        sys.stdout.write(output)

    def print_board(self):
        output = '\n'
        for i in range(self.size + 1):
            output += '\n'
            if (i == 0):
                output += ' '
            else:
                output += chr(i + 96)
            for j in range(self.size):
                if (i == 0):
                    output += ' ' + str(j + 1)
                else:
                    output += ' ' + self.piece_dict[self.board[i - 1, j]]
        sys.stdout.write(output)


g = Game(int(sys.argv[1]))
