import numpy as np
import tkinter as tk
import copy

"""
Board class.

Board data:
  1=X, -1=O, 0=empty
  first dim is column , 2nd is row:
     pieces[1][7] is the square in column 2,
     at the opposite end of the board in row 8.


Squares are stored and manipulated as (x,y) tuples. 
x is the column, y is the row.
"""

# def read_input_file(file_path):
#     with open(file_path, 'r') as file:
#         # Read player (any character)
#         player = file.readline().strip()
#         if player=="X":
#             player = 1
#         else:
#             player = -1

#         # Read remaining play times
#         remaining_playtime, opponent_remaining_playtime = file.readline().split()

#         # Read the current state of the board
#         board = [file.readline().strip() for _ in range(12)]

#     return player, remaining_playtime, opponent_remaining_playtime, board

# def convert_board_to_numbers(board):
#     # Create a new list to represent the numerical board
#     numerical_board = []

#     for row in board:
#         numerical_row = []
#         for el in row:
#             if el == '.':
#                 numerical_row.append(0)
#             elif el == 'X':
#                 numerical_row.append(1)
#             elif el == 'O':
#                 numerical_row.append(-1)
#         numerical_board.append(numerical_row)

#     return numerical_board

def convert_board_to_numbers(row):
    # Create a new list to represent the numerical row
    numerical_row = []
    num_x, num_o = 0, 0
    for el in row:
        if el == '.':
            numerical_row.append(0)
        elif el == 'X':
            numerical_row.append(1)
            num_x += 1
        elif el == 'O':
            numerical_row.append(-1)
            num_o += 1
    return np.array(numerical_row)

def read_input_file(file_path):
    with open(file_path, 'r') as file:
        # Read player (any character)
        player_char = file.readline().strip()
        player = 1 if player_char == 'X' else -1

        # Read remaining play times
        remaining_playtime, opponent_remaining_playtime = map(float, file.readline().split())

        # Read the current state of the board
        board = np.array([convert_board_to_numbers(file.readline().strip()) for _ in range(12)])

    return player, remaining_playtime, opponent_remaining_playtime, board


# class ReversiGUI(tk.Tk):
#     def __init__(self, reversi_game):
#         super().__init__()

#         self.title("Reversi Game")
#         self.geometry("400x400")

#         self.reversi_game = reversi_game

#         self.create_board()

#     def create_board(self):
#         for row in range(self.reversi_game.n):
#             for col in range(self.reversi_game.n):
#                 piece = self.reversi_game[row][col]
#                 piece_label = tk.Label(self, text=self.get_piece_display(piece))
#                 piece_label.grid(row=row, column=col, padx=5, pady=5)

#         count_label = tk.Label(self, text=self.get_count_display())
#         count_label.grid(row=self.reversi_game.n, column=0, columnspan=self.reversi_game.n, pady=10)

#     def get_piece_display(self, piece):
#         if piece == 1:
#             return 'X'
#         elif piece == -1:
#             return 'O'
#         else:
#             return '-'

#     def get_count_display(self):
#         return f"X: {self.reversi_game.count(1)}  |  O: {self.reversi_game.count(-1)}"

class ReversiGame(object):
    # list of all 8 directions on the board, as (x,y) offsets
    __directions = [(1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1,
                                                                          1),
                    (0, 1)]

    def __init__(self, board, n):
        """Set up initial board configuration."""

        # Board Size n * n
        self.n = n

        # Create the empty board array.
        self.pieces = np.zeros((self.n, self.n), dtype=np.int)

        # Set up the initial 4 pieces.
        self.pieces = board
    # add [][] indexer syntax to the Board
    def __getitem__(self, index):
        return self.pieces[index]

    # def set_pieces(self, pieces=None):
    #     """
    #     set pieces, if pieces is None, then do nothing. by im0qianqian
    #     这里有两种拷贝方法，第一种是使用 np.copy 创建一个新对象然后将新对象的引用交给 self.pieces，好处是即使中途某处代码修改了 board 也不好影响其他部分运行，坏处是效率低
    #     另一种方法是使用 np.copyto 将 pieces 直接拷贝到 self.pieces 中而不用新创建对象，好处是速度快，坏处是代码其他逻辑若修改了 board，可能造成不好的影响

    #     嗯～一般情况下代码其他地方应该不会做修改，所以我们目前采用 copyto，预期浪费空间不如利用起来

    #     2019.4.12 更改为 np.copy，我天真了
    #     """
    #     if pieces is not None:
    #         self.pieces = np.copy(pieces)
    #         # np.copyto(self.pieces, pieces)

    # def display(self):
    #     """Display the board."""

    #     # print the column labels as letters on the bottom of the board
    #     print("   ", end=" ")
    #     for x in range(self.n):
    #         print(x, '', end=" ")  # prints 'a', 'b', etc.
    #     print("")
    #     print("\t" + "-" * 3 * self.n)
    #     for x in range(self.n):
    #         print(x+1, "|", end="\t")  # print the row #
    #         for y in range(self.n):
    #             piece = self[x][y]  # get the piece to print
    #             if piece == -1:
    #                 print("X", end="\t" if y == self.n - 1 else "\t")
    #             elif piece == 1:
    #                 print("O", end="\t" if y == self.n - 1 else "\t")
    #             else:
    #                 print("-" if y == self.n - 1 else "- ", end="\t")
    #         # Display the # of pieces for each color to the right of the board
    #         if x == self.n // 2:
    #             print("|X: " + str(self.count(1)))
    #         elif x == self.n // 2 - 1:
    #             print("|O: " + str(self.count(-1)))
    #         else:
    #             print("|")
    #     print("   " + "-" * 3 * self.n)

    # def display(self):
    #     """Display the board."""
    #     reversi_gui = ReversiGUI(self)
    #     reversi_gui.mainloop()
        # column_labels = '  ' + ' '.join(map(str, range(self.n)))
        # horizontal_line = '\t' + '-' * (4 * self.n + 1)
        
        # print(column_labels)
        # print(horizontal_line)

        # for x in range(self.n):
        #     row_label = str(x + 1)
        #     row_data = '|'.join(self._get_display_piece(self[x][y]) for y in range(self.n))
        #     print(f"{row_label} | {row_data} | {self._get_display_count(x)}")

        # print(horizontal_line)

    # def _get_display_piece(self, piece):
    #     """Get the display representation of a piece."""
    #     if piece == 1:
    #         return ' X '
    #     elif piece == -1:
    #         return ' O '
    #     else:
    #         return ' - '

    def _get_display_count(self, x):
        """Get the display representation of the count."""
        if x == self.n // 2:
            return f"| X: {self.count(1)}"
        elif x == self.n // 2 - 1:
            return f"| O: {self.count(-1)}"
        else:
            return '|'

    # def count(self, color):
    #     """Counts the # pieces of the given color (1 for white, -1 for black, 0 for empty spaces)"""
    #     print(np.count_nonzero(self.pieces == color))
    #     return np.count_nonzero(self.pieces == color)

    def count(self, color):
        """Counts the # pieces of the given color
        (1 for X, -1 for O, 0 for empty spaces)"""
        count = sum(1 for row in self for piece in row if piece == color)
        return count
    
    # def count(self, color):
    #     """Counts the # pieces of the given color
    #     (1 for X, -1 for O, 0 for empty spaces)"""
    #     count = 0
    #     for y in range(self.n):
    #         for x in range(self.n):
    #             if self[x][y] == color:
    #                 count += 1
    #     print(count)
    #     return count
    # def get_squares(self, color):
    #     """Gets coordinates (x, y pairs) for all pieces on the board of the given color."""
    #     indices = np.where(self.pieces == color)
    #     print(indices)
    #     if len(indices[0]) == 0:
    #         return []  # No elements with the specified color
    #     return list(zip(indices[1], indices[0]))


    def get_squares(self, color):
        """Gets coordinates (x,y pairs) for all pieces on the board of the given color.
        (1 for white, -1 for black, 0 for empty spaces)"""

        squares = []
        for y in range(self.n):
            for x in range(self.n):
                if self[x][y] == color:
                    squares.append((x, y))
        return squares

    # def get_legal_moves(self, color):
    #     """Returns all the legal moves for the given color."""
    #     all_moves = np.array([self.get_moves_for_square(square) for square in self.get_squares(color)])
    #     return list(set(all_moves.flatten()))

    def get_legal_moves(self, color):
        """Returns all the legal moves for the given color.
        (1 for white, -1 for black
        """
        moves = set()  # stores the legal moves.

        # Get all the squares with pieces of the given color.
        for square in self.get_squares(color):
            # Find all moves using these pieces as base squares.
            newmoves = self.get_moves_for_square(square)
            # Store these in the moves set.
            moves.update(newmoves)

        return list(moves)

    def get_moves_for_square(self, square):
        """Returns all the legal moves that use the given square as a base.
        That is, if the given square is (3,4) and it contains a black piece,
        and (3,5) and (3,6) contain white pieces, and (3,7) is empty, one
        of the returned moves is (3,7) because everything from there to (3,4)
        is flipped.
        """
        (x, y) = square

        # determine the color of the piece.
        color = self[x][y]

        # skip empty source squares.
        if color == 0:
            return None

        # search all possible directions.
        moves = []
        for direction in self.__directions:
            move = self._discover_move(square, direction)
            if move:
                moves.append(move)

        # return the generated move list
        return moves

    def execute_move(self, move, color):
        """Perform the given move on the board; flips pieces as necessary.
        color gives the color pf the piece to play (1=white,-1=black)
        """

        # Much like move generation, start at the new piece's square and
        # follow it on all 8 directions to look for a piece allowing flipping.

        # Add the piece to the empty square.
        flips = (flip for direction in self.__directions
                 for flip in self._get_flips(move, direction, color))

        for x, y in flips:
            self[x][y] = color

    def _discover_move(self, origin, direction):
        """ Returns the endpoint for a legal move, starting at the given origin,
        moving by the given increment."""
        x, y = origin
        color = self[x][y]
        flips = []

        for x, y in ReversiGame._increment_move(origin, direction, self.n):
            if self[x][y] == 0:
                if flips:
                    return x, y
                else:
                    return None
            elif self[x][y] == color:
                return None
            elif self[x][y] == -color:
                flips.append((x, y))

    def _get_flips(self, origin, direction, color):
        """ Gets the list of flips for a vertex and direction to use with the
        execute_move function """
        # initialize variables
        flips = [origin]

        for x, y in ReversiGame._increment_move(origin, direction, self.n):
            if self[x][y] == 0:
                return []
            elif self[x][y] == -color:
                flips.append((x, y))
            elif self[x][y] == color:
                return flips

        return []

    # # @staticmethod
    
    # def _increment_move(move, direction, n):
    #     """ Generator expression for incrementing moves """
    #     current_move = list(map(sum, zip(move, direction)))
    #     while all(map(lambda x: 0 <= x < n, current_move)):
    #         yield current_move
    #         current_move = list(map(sum, zip(current_move, direction)))
    
    @staticmethod
    def _increment_move(move, direction, n):
        """ Generator expression for incrementing moves """
        move = list(map(sum, zip(move, direction)))
        # print(move)
        while all(map(lambda x: 0 <= x < n, move)):
            yield move
            move = list(map(sum, zip(move, direction)))

    # def is_game_over(board):
    #     # Check if the board is full or if one player has no legal moves
    #     if not any(0 in row for row in board) or (len(generate_legal_moves(board, True)) == 0 and len(generate_legal_moves(board, False)) == 0):
    #         return True
    #     return False
        
# class ReversiLogic(object):
#     __directions = [(1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1)]

#     def __init__(self, player, board_curr_state):
#         # self.n = board_size
#         self.player = player
#         self.game = board_curr_state  # Reference to the ReversiGame instance
#         self.temp_game = board_curr_state

#     def minimax_alpha_beta(self, depth, maximizing_player, alpha, beta):
#         if depth == 0 : #or self.game.is_game_over():
#             return self.evaluate_board(), None

#         legal_moves = self.temp_game.get_legal_moves(self.player)
#         best_move = None

#         if maximizing_player:
#             max_eval = float('-inf')
#             for move in legal_moves:
#                 print(move, self.player)
#                 self.temp_game = self.temp_game.execute_move(move, self.player)
#                 eval, _ = self.minimax_alpha_beta(depth - 1, False, alpha, beta)
#                 self.temp_game.undo_move(move, self.player)

#                 if eval > max_eval:
#                     max_eval = eval
#                     best_move = move

#                 alpha = max(alpha, eval)
#                 if beta <= alpha:
#                     break  # Beta cut-off

#             return max_eval, best_move
#         else:
#             min_eval = float('inf')
#             for move in legal_moves:
#                 print(move, -self.player)
#                 self.temp_game.execute_move(move, -self.player)
#                 eval, _ = self.minimax_alpha_beta(depth - 1, True, alpha, beta)
#                 self.temp_game.undo_move(move, -self.player)

#                 if eval < min_eval:
#                     min_eval = eval
#                     best_move = move

#                 beta = min(beta, eval)
#                 if beta <= alpha:
#                     break  # Alpha cut-off

#             return min_eval, best_move

#     def evaluate_board(self):
#         # Simple evaluation function (count the difference in pieces)
#         return self.temp_game.count(1) - self.temp_game.count(-1)

# class ReversiLogic(object):
#     def __init__(self, player, board_curr_state):
#         self.player = player
#         self.game = board_curr_state  # Reference to the ReversiGame instance

#     def minimax_alpha_beta(self, depth, maximizing_player, alpha, beta):
#         if depth == 0 :#or self.game.is_game_over():
#             return self.evaluate_board(), None
#         print(self.evaluate_board())
#         legal_moves = self.game.get_legal_moves(self.player)
#         # print(legal_moves)
#         best_move = None

#         if maximizing_player:
#             max_eval = float('-inf')
#             for move in legal_moves:
#                 print(move)
#                 temp_game = copy.deepcopy(self.game)
#                 temp_game.execute_move(move, self.player)
#                 # temp_game.display()
#                 eval, _ = self.minimax_alpha_beta(depth - 1, False, alpha, beta)

#                 if eval > max_eval:
#                     max_eval = eval
#                     best_move = move

#                 alpha = max(alpha, eval)
#                 if beta <= alpha:
#                     break  # Beta cut-off

#             return max_eval, best_move
#         else:
#             min_eval = float('inf')
#             for move in legal_moves:
#                 temp_game = copy.deepcopy(self.game)
#                 temp_game.execute_move(move, -self.player)
#                 eval, _ = self.minimax_alpha_beta(depth - 1, True, alpha, beta)

#                 if eval < min_eval:
#                     min_eval = eval
#                     best_move = move

#                 beta = min(beta, eval)
#                 if beta <= alpha:
#                     break  # Alpha cut-off

#             return min_eval, best_move

#     def evaluate_board(self):
#         # Simple evaluation function (count the difference in pieces)
#         return self.game.count(1) - self.game.count(-1)

class MinMaxAgent:
    def __init__(self, color, search_depth):
        self.color = color
        self.search_depth = search_depth
    # def minimax_alpha_beta(self, depth, maximizing_player, alpha, beta, current_game=None):
    #     if current_game is None:
    #         current_game = self.game

    #     if depth == 0:  # or current_game.is_game_over():
    #         return self.evaluate_board(), None
    #     current_game.display()
    #     legal_moves = current_game.get_legal_moves(self.player)
    #     best_move = None

    #     if maximizing_player:
    #         max_eval = float('-inf')
    #         for move in legal_moves:
    #             current_game.execute_move(move, self.player)
    #             eval, _ = self.minimax_alpha_beta(depth - 1, False, alpha, beta, current_game)

    #             if eval > max_eval:
    #                 max_eval = eval
    #                 best_move = move

    #             alpha = max(alpha, eval)
    #             if beta <= alpha:
    #                 break  # Beta cut-off

    #             current_game.undo_move(move, self.player)

    #         return max_eval, best_move
    #     else:
    #         min_eval = float('inf')
    #         for move in legal_moves:
    #             current_game.execute_move(move, -self.player)
    #             eval, _ = self.minimax_alpha_beta(depth - 1, True, alpha, beta, current_game)

    #             if eval < min_eval:
    #                 min_eval = eval
    #                 best_move = move

    #             beta = min(beta, eval)
    #             if beta <= alpha:
    #                 break  # Alpha cut-off

    #             current_game.undo_move(move, -self.player)

    #         return min_eval, best_move
        
    def minimax_alpha_beta(self, game, depth, alpha, beta, player):
        if depth == 0 or not game.get_legal_moves(player):
            return None, game.evaluate_board()

        best_move = None
        avail_moves = game.get_legal_moves(player)

        if player < 0:
            best_score = float('-inf')
            for move in avail_moves:
                new_game = copy.deepcopy(game)
                new_game.execute_move(move, player)
                _, value = self.minimax_alpha_beta(new_game, depth - 1, alpha, beta, -player)

                if value > best_score:
                    best_score = value
                    best_move = move

                alpha = max(alpha, best_score)
                if beta <= alpha:
                    break

        elif player > 0:
            best_score = float('inf')
            for move in avail_moves:
                new_game = copy.deepcopy(game)
                new_game.execute_move(move, player)
                _, value = self.minimax_alpha_beta(new_game, depth - 1, alpha, beta, -player)

                if value < best_score:
                    best_score = value
                    best_move = move

                beta = min(beta, best_score)
                if beta <= alpha:
                    break

        return best_move, best_score
    

    def evaluate_board(self):
        # Simple evaluation function (count the difference in pieces)
        return self.count(1) - self.count(-1)
    
    def make_move(self, game):
        """Make a random valid move"""
        _, best_move = self.minimax_alpha_beta(game, self.search_depth, float('-inf'), float('inf'), self.color)
        return best_move

