from logic import ReversiGame, read_input_file
from lookup import TranspositionTable
import random
import copy
import time

"""
Author: Anish Ghiya
"""



def generate_diagonal_rows(board):
    """Generate an array of all diagonal rows starting from (0,0) to (game.n-1, 0) and (0, game.n-1).

    Args:
        board: The game board.

    Returns:
        A list containing all diagonal rows.
    """
    n = board.n
    diagonals = []

    # Iterate over rows
    for i in range(n):
        diagonal_row = [board[i - j][j] for j in range(i + 1)]
        diagonals.append(diagonal_row)

    # Iterate over columns
    for j in range(1, n):
        diagonal_row = [board[n - 1 - k][j + k] for k in range(n - j)]
        diagonals.append(diagonal_row)

    return diagonals

def generate_diagonals_from_corner(board):
    """Generate an array of all diagonals starting from the corner (0, n-1) and iterate through (0, n-2), (n-2, 0), and so on.

    Args:
        board: The game board.

    Returns:
        A list containing all diagonal rows.
    """
    n = board.n
    diagonals = []

    # Iterate over columns
    for start_col in range(n - 1, -1, -1):
        diagonal_row = [board[k][start_col + k] for k in range(min(n - start_col, n))]
        diagonals.append(diagonal_row)

    # Iterate over rows
    for start_row in range(1, n ):
        diagonal_row = [board[start_row + k][k] for k in range(min(n - start_row, n))]
        diagonals.append(diagonal_row)

    return diagonals

def count_diagonal_with_corner(diagonals, player):
    reversed_diagonals = list(reversed(diagonals))
    count = 0
    corner_owned = 0
    if diagonals[0][0]==player:
        corner_owned+=1
        for diagonal in diagonals:
            if all(element == player for element in diagonal):
                count += len(diagonal)
            else: 
                break

    if reversed_diagonals[0][0]==player:
        corner_owned+=1
        for diagonal in reversed_diagonals:
            if all(element == player for element in diagonal):
                count += len(diagonal)
            else: 
                break
    return corner_owned, count

def get_control_corners(game, player):
    corners = [(0, 0), (0, game.n-1), (game.n-1, 0), (game.n-1, game.n-1)]
    return max(0, sum(game[x][y] * player for x, y in corners))

def calculate_edges_control(game, player):
    """
    Calculate the control of edges for a given player.

    Args:
    - game (ReversiGame): The Reversi game instance.
    - player (int): The player for whom to calculate the edges control.

    Returns:
    - int: The control of edges for the specified player.
    """
    n = game.n
    control = 0

    # Check top edge
    control += sum(game[x][0] == player for x in range(n))

    # Check bottom edge
    control += sum(game[x][n - 1] == player for x in range(n))

    # Check left edge
    control += sum(game[0][y] == player for y in range(n))

    # Check right edge
    control += sum(game[n - 1][y] == player for y in range(n))

    return control

def calculate_edge_stability(game, player):
    """Calculate the stability of a given player on all tiles of the game."""
    left_score, top_score, bottom_score, right_score = 0, 0, 0, 0
    own_count, other_count = 0, 0
    n = game.n

    # Left Edge Stability
    for i in range(1, n - 2):
        if game[i][0] == 0:  # Assuming 0 represents an EMPTY cell
            for offset in [(0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1)]:
                x, y = i + offset[0], 0 + offset[1]
                if 0 <= x < n and 0 <= y < n:
                    if game[x][y] == player:
                        own_count += 1
                    elif game[x][y] == -player:
                        other_count += 1

            if own_count >= 4:
                left_score -= 3
            elif other_count >= 4:
                left_score += 3

            own_count, other_count = 0, 0

    # Top Edge Stability
    for j in range(1, n - 2):
        if game[0][j] == 0:
            for offset in [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0)]:
                x, y = 0 + offset[0], j + offset[1]
                if 0 <= x < n and 0 <= y < n:
                    if game[x][y] == player:
                        own_count += 1
                    elif game[x][y] == -player:
                        other_count += 1

            if own_count >= 4:
                top_score -= 3
            elif other_count >= 4:
                top_score += 3

            own_count, other_count = 0, 0

    # Bottom Edge Stability
    for j in range(1, n - 2):
        if game[n - 1][j] == 0:
            for offset in [(1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0)]:
                x, y = n - 1 + offset[0], j + offset[1]
                if 0 <= x < n and 0 <= y < n:
                    if game[x][y] == player:
                        own_count += 1
                    elif game[x][y] == -player:
                        other_count += 1

            if own_count >= 4:
                bottom_score -= 3
            elif other_count >= 4:
                bottom_score += 3

            own_count, other_count = 0, 0

    # Right Edge Stability
    for i in range(1, n - 2):
        if game[i][n - 1] == 0:
            for offset in [(0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1)]:
                x, y = i + offset[0], n - 1 + offset[1]
                if 0 <= x < n and 0 <= y < n:
                    if game[x][y] == player:
                        own_count += 1
                    elif game[x][y] == -player:
                        other_count += 1

            if own_count >= 4:
                right_score -= 3
            elif other_count >= 4:
                right_score += 3

            own_count, other_count = 0, 0

    return left_score + top_score + bottom_score + right_score

def evaluate_board(game, my_player, player):
    diagonals = generate_diagonal_rows(game)
    diagonals2 = generate_diagonals_from_corner(game)

    corner_owned, count = count_diagonal_with_corner(diagonals, my_player)
    corner_owned2, count2 = count_diagonal_with_corner(diagonals2, my_player)
    corner_owned_opp, count_opp = count_diagonal_with_corner(diagonals, -my_player)
    corner_owned2_opp, count2_opp = count_diagonal_with_corner(diagonals2, -my_player)

    stable_pieces = count + count2 - count_opp - count2_opp
    
    
    piece_count = game.count(my_player)
    opp_piece_count = game.count(-my_player)
    parity = (piece_count - opp_piece_count)/(piece_count + opp_piece_count)
    
    mobility = len(game.get_legal_moves(my_player)) - len(game.get_legal_moves(-my_player))
                       
    control_corners = corner_owned + corner_owned2 - corner_owned_opp - corner_owned2_opp
    control_edges = calculate_edges_control(game, my_player)
    # control_edges_stability = calculate_edge_stability(game, my_player)
    # stability = calculate_stability(game)

    # Weights for each feature
    weights = {
        'parity': 40,
        'mobility': 10,
        'control_corners': 30,
        'control_edges': 20,
        #'control_edges_stability': 5,
        'stable_pieces':50
        # 'stability': 4
    }

    evaluation = (
        weights['parity'] * parity +
        weights['mobility'] * mobility +
        weights['control_corners'] * control_corners +
        weights['control_edges'] * control_edges +
        # weights['control_edges_stability'] * control_edges_stability + 
        weights['stable_pieces' ]* stable_pieces
        # weights['stability'] * stability
    )

    return evaluation

def max_player(game, depth, alpha, beta, my_player, player, transposition_table):
    entry = transposition_table.lookup(game)
    # print(entry)
    if entry:
        return entry['best_move'], entry['score']

    best_score = float('-inf')
    legal_moves = game.get_legal_moves(player)
    best_move = None

    if depth == 0 or len(legal_moves) == 0:
        score = evaluate_board(game, my_player, player)
        transposition_table.store(game, {'best_move': None, 'score': score, 'depth': depth})
        return None, score

    for move_max in legal_moves:
        max_game = copy.deepcopy(game)
        max_game.execute_move(move_max, player)

        _, score = min_player(max_game, depth - 1, alpha, beta, my_player, -player, transposition_table)

        if score > best_score:
            best_score = score
            best_move = move_max

        alpha = max(alpha, score)

        if beta <= alpha:
            break

    transposition_table.store(game, {'best_move': best_move, 'score': best_score, 'depth': depth})
    return best_move, best_score

def min_player(game, depth, alpha, beta, my_player, player, transposition_table):
    entry = transposition_table.lookup(game)
    if entry:
        return entry['best_move'], entry['score']

    best_score = float('inf')
    legal_moves = game.get_legal_moves(player)

    if depth == 0 or len(legal_moves) == 0:
        score = evaluate_board(game, my_player, player)
        transposition_table.store(game, {'best_move': None, 'score': score, 'depth': depth})
        return None, score

    for move_min in legal_moves:
        min_game = copy.deepcopy(game)
        min_game.execute_move(move_min, player)

        _, score = max_player(min_game, depth - 1, alpha, beta, my_player, -player, transposition_table)

        if score < best_score:
            best_score = score
            best_move = move_min

        beta = min(beta, score)

        if beta <= alpha:
            break

    transposition_table.store(game, {'best_move': best_move, 'score': best_score, 'depth': depth})
    return best_move, best_score

def negamax(game, depth, alpha, beta, my_player, player, transposition_table):
    entry = transposition_table.lookup(game)
    if entry and entry['depth'] >= depth:
        if entry['type'] == 1:
            return entry['best_move'], entry['score']

    legal_moves = game.get_legal_moves(player)

    if depth == 0 or len(legal_moves) == 0:
        return None, evaluate_board(game, my_player, player)

    best_move = None
    best_score = float('-inf')

    for move in legal_moves:
        next_game = copy.deepcopy(game)
        next_game.execute_move(move, player)

        _, score = negamax(next_game, depth - 1, -beta, -alpha, my_player, -player, transposition_table)

        score = -score

        if score > best_score:
            best_score = score
            best_move = move

        alpha = max(alpha, score)

        if beta <= alpha:
            break

    transposition_table.store(game, {'best_move': best_move, 'score': best_score, 'depth': depth, 'type': 1})

    return best_move, best_score

def negascout(game, depth, alpha, beta, my_player, player, transposition_table):
    entry = transposition_table.lookup(game)
    if entry and entry['depth'] >= depth:
        return entry['best_move'], entry['score']

    legal_moves = game.get_legal_moves(player)

    if depth == 0 or len(legal_moves) == 0:
        return None, evaluate_board(game, my_player, player)

    best_move = None
    best_score = float('-inf')

    first_move = True

    for move in legal_moves:
        next_game = copy.deepcopy(game)
        next_game.execute_move(move, player)

        if first_move:
            _, score = negamax(next_game, depth - 1, -beta, -alpha, my_player, -player, transposition_table)
        else:
            _, score = negamax(next_game, depth - 1, -alpha - 1, -alpha, my_player, -player, transposition_table)
            if alpha < score < beta:
                _, score = negamax(next_game, depth - 1, -beta, -score, my_player, -player, transposition_table)

        score = -score

        if score > best_score:
            best_score = score
            best_move = move

        alpha = max(alpha, score)

        if beta <= alpha:
            break

        first_move = False

    transposition_table.store(game, {'best_move': best_move, 'score': best_score, 'depth': depth, 'type': 1})

    return best_move, best_score

def make_best_move(board, my_player, player, remaining_playtime, transposition_table):
    if remaining_playtime <= 1:
        legal_moves = board.get_legal_moves(player)
        best_move = random.choice(legal_moves)
        return best_move
    elif remaining_playtime >= 275:
        depth = 6
    elif remaining_playtime >= 150:
        depth = 5
    elif remaining_playtime >= 50:
        depth = 4
    elif remaining_playtime <= 5:
        depth = 1
    else:
        depth = 3
    
    alpha = float('-inf')
    beta = float('inf')


    start_time = time.time()
    best_move, best_score_max_player = max_player(board, depth, alpha, beta, my_player, player, transposition_table)
    end_time_max_player = time.time()
    time_taken_max_player = end_time_max_player - start_time
    print(f"Time taken by max_player: {time_taken_max_player} seconds")

    # best_move, best_score = max_player(board, depth, alpha, beta, player, transposition_table)
    # best_move, best_score = negascout(board, depth, alpha, beta, player, transposition_table)

    # print(best_move_max_player,best_move_negascout)
    return best_move, time_taken_max_player

def random_player(board, my_player, player, transposition_table):
    depth = 1
    alpha = float('-inf')
    beta = float('inf')
    start_time = time.time()
    best_move, best_score_max_player = max_player(board, depth, alpha, beta, my_player, player, transposition_table)
    end_time_max_player = time.time()
    time_taken_max_player = end_time_max_player - start_time
    print(f"Time taken by max_player: {time_taken_max_player} seconds")

    # legal_moves = board.get_legal_moves(player)
    # print(legal_moves == [])
    # if legal_moves == []:
    #     return None
    
    # best_move = legal_moves[random.randint(0, len(legal_moves)-1)]
    return best_move

def write_output(file_path, out_file_path, who_playing):
    player, remaining_playtime, oppnent_remaining_playtime, initial_board = read_input_file(file_path)
    board = ReversiGame(initial_board, 12)

    if who_playing=='Me':
    
        transposition_table = TranspositionTable(board)
        # print(transposition_table.zobrist_table)
        
        best_move, time_taken_max_player = make_best_move(board, player, player, remaining_playtime, transposition_table)

        # transposition_table = TranspositionTable(board)
        # best_move_negascout = make_best_move(board, player, player, remaining_playtime, transposition_table,  'negascout')

        # print(best_move_minmax, best_move_negascout)

    else:
        print("Random_player is playing")
        start_time = time.time()
        transposition_table = TranspositionTable(board)
        best_move = random_player(board, player, player, transposition_table)
        end_time_max_player = time.time()
        time_taken_max_player = end_time_max_player - start_time
        print(f"Time taken by max_player: {time_taken_max_player} seconds")

    with open(out_file_path, 'w') as file:
        if best_move==None:
            file.write("None")
        else: 
            file.write(chr(best_move[1] + ord('a')) + str(best_move[0] + 1))

    return remaining_playtime - time_taken_max_player, oppnent_remaining_playtime

# if __name__ == '__main__':
#     file_path = 'input.txt'
#     player, remaining_playtime, opponent_remaining_playtime, initial_board = read_input_file(file_path)

#     board = ReversiGame(initial_board, 12)
#     transposition_table = TranspositionTable(board)
#     # print(transposition_table.zobrist_table)
    
#     best_move_minmax = make_best_move(board, player, player, remaining_playtime, transposition_table,  'minmax')

#     transposition_table = TranspositionTable(board)
#     best_move_negascout = make_best_move(board, player, player, remaining_playtime, transposition_table,  'negascout')

#     print(best_move_minmax, best_move_negascout)
#     file_path = 'output.txt'
#     with open(file_path, 'w') as file:
#         file.write(chr(best_move[1] + ord('a')) + str(best_move[0] + 1))