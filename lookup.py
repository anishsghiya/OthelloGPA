import random 
random.seed(42)

class TranspositionTable:
    def __init__(self, board):
        self.board_size = board.n
        self.state = board
        self.table = {}
        self.zobrist_table = [[random.getrandbits(64) for _ in range(self.board_size)] for _ in range(self.board_size)]

    def hash_key(self, state):
        # Use Zobrist hashing to create a hash value for the board state
        hash_value = 0
        for i in range(self.board_size):
            for j in range(self.board_size):
                if state[i][j] != 0:
                    hash_value ^= int(self.zobrist_table[i][j])
        return hash_value

    def lookup(self, state):
        key = self.hash_key(state)
        return self.table.get(key)

    def store(self, state, info):
        key = self.hash_key(state)
        self.table[key] = info