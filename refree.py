from logic import ReversiGame, read_input_file
from v_main import write_output
from lookup import TranspositionTable
import random
import copy
import time
import argparse
import random

def initialize_board(file_path):
    player, remaining_playtime, opponent_remaining_playtime, initial_board = read_input_file(file_path)
    board = ReversiGame(initial_board, 12)

    return player, remaining_playtime, opponent_remaining_playtime, board


def reverse_numerical_to_board(numerical_row):
    # Create a new list to represent the board row with characters
    board_row = []
    for num in numerical_row:
        if num == 0:
            board_row.append('.')
        elif num == 1:
            board_row.append('X')
        elif num == -1:
            board_row.append('O')
    return board_row

def print_board(game_state, my_time_left, opponent_time_left, player, extracomments=''):
    file_path = 'temp_output.txt'
    file_path_all_games = 'temp_output_allgames.txt'

    with open(file_path, 'w') as file, open(file_path_all_games, 'a') as all_games_file:
        if player == 1:
            player_str = 'X'
        elif player == -1:
            player_str = 'O'

        file.write(player_str + '\n')
        file.write(f'{opponent_time_left} {my_time_left}\n')  # Add a newline character and time left information
        for row in range(game_state.n):
            file.write(''.join(reverse_numerical_to_board(game_state[row])) + '\n')  # Add a newline character

        # Write the same information to the all_games_file
        all_games_file.write(extracomments + '\n')
        all_games_file.write(player_str + '\n')
        all_games_file.write(f'{opponent_time_left} {my_time_left}\n')  # Add a newline character and time left information
        for row in range(game_state.n):
            all_games_file.write(''.join(reverse_numerical_to_board(game_state[row])) + '\n')  # Add a newline character

        all_games_file.write('\n')  # Add an extra newline to separate consecutive game states


def is_game_over(board, player):
    print("Checking is game_over: ", len(board.get_legal_moves(player)),board.get_legal_moves(-player)==0)
    if (len(board.get_legal_moves(player))==0 and len(board.get_legal_moves(-player))==0) or board.count(player)==0 or board.count(0)==0:
        return True
    
    return False

def reverse_coordinates(move_str):
    # Assuming move_str is a string like 'c4' or 'a1'
    col_str, row_str = move_str[0], move_str[1:]
    row = int(row_str) - 1
    col = ord(col_str) - ord('a')
    return row, col

def apply_move(board, output_file):
    with open(output_file, 'r') as file:
        move = file.read().strip()
        if move == 'None':
            return None
        return reverse_coordinates(move)
    
def get_winner(board, player):
    count_player1 = board.count(player)
    count_player2 = board.count(-player)
    return  count_player1, count_player2

# def referee():
#     # Initialize the game
#     file_path = 'input.txt'
#     # Create or overwrite the temp_output_allgames.txt file
#     with open('temp_output_allgames.txt', 'w'):
#         pass  # This just creates an empty file

#     player, my_remaining_playtime, opponent_time_left, board = initialize_board(file_path)
#     current_player = 'Me'

#     print_board(board, my_remaining_playtime, opponent_time_left, player, f"#######\tGame Starts\t######\n {'AI' if current_player == 'Me' else 'Me'} is playing on the following board")

#     while not is_game_over(board, player):
#         if len(board.get_legal_moves(player)) != 0:
#             print(f"{current_player} turn, {file_path}")
#             my_time_left, opponent_time_left = write_output(file_path, 'output.txt', current_player)
#             # my_time_left = my_remaining_playtime - time_elapsed
            

#             move = apply_move(board, 'output.txt')

#             if move is not None:
#                 row, col = move
#                 board.execute_move((row, col), player)
#                 print(my_time_left, opponent_time_left)
#                 print_board(board, my_time_left, opponent_time_left, -player, f"{'AI' if current_player == 'Me' else 'Me'} is playing on the following board")
#                 current_player = 'AI' if current_player == 'Me' else 'Me'
#                 file_path = 'temp_output.txt'
#                 player = -player
#             else:
#                 print_board(board, my_time_left, opponent_time_left, -player, f"Same Board as above because no possible moves were available\n{'AI' if current_player == 'Me' else 'Me'} is playing on the following board")

#                 current_player = 'AI' if current_player == 'Me' else 'Me'
#                 file_path = 'temp_output.txt'
#                 player = -player
#         else:
#             # Switch to the other player for the next turn
#             current_player = 'AI' if current_player == 'Me' else 'Me'
#             file_path = 'temp_output.txt'
#             player = -player


#     # Print the final state of the board
#     # print_board(board, my_time_left, opponent_time_left, -player)

#     # Determine the winner
#     count_player1, count_player2 = get_winner(board, -player)
#     print(f"Count of player1 and player2: ", count_player1, count_player2)

def parse_args():
    parser = argparse.ArgumentParser(description='Reversi Game Referee')
    parser.add_argument('--player1', type=str, choices=['AI', 'Me'], default='Me', help='Specify the player for O')
    return parser.parse_args()

# def referee():
#     args = parse_args()

#     # Initialize the game
#     file_path = 'input.txt'
#     # Create or overwrite the temp_output_allgames.txt file
#     with open('temp_output_allgames.txt', 'w'):
#         pass  # This just creates an empty file

#     player1, my_remaining_playtime1, opponent_time_left1, board = initialize_board(file_path)
#     # player2, my_remaining_playtime2, opponent_time_left2, _ = initialize_board(file_path)

#     # Assign players based on command-line arguments
#     if args.player1 == 'Me':
#         current_player1 = 'Me'
#     else:
#         current_player1 = 'AI'

#     print_board(board, my_remaining_playtime1, opponent_time_left1, player1, f"#######\tGame Starts\t######\n {current_player1} is playing on the following board")

#     while not is_game_over(board, player1):
#         if len(board.get_legal_moves(player1)) != 0:
#             print(f"{current_player1} turn, {file_path}")
#             my_time_left, opponent_time_left = write_output(file_path, 'output.txt', current_player1)
#             move = apply_move(board, 'output.txt')

#             if move is not None:
#                 row, col = move
#                 board.execute_move((row, col), player1)
#                 print_board(board, my_time_left, opponent_time_left, -player1, f"{current_player1} is playing on the following board")
#             else:
#                 print_board(board, my_time_left, opponent_time_left, -player1, f"Same Board as above because no possible moves were available\n{current_player1} is playing on the following board")

#             current_player1, current_player2 = current_player2, current_player1
#             player1, player2 = player2, player1
#             my_remaining_playtime1, my_remaining_playtime2 = my_remaining_playtime2, my_remaining_playtime1
#             opponent_time_left1, opponent_time_left2 = opponent_time_left2, opponent_time_left1
#             file_path = 'temp_output.txt'
#         else:
#             # Switch to the other player for the next turn
#             file_path = 'temp_output.txt'
#             player1, my_remaining_playtime1, opponent_time_left1, board = initialize_board(file_path)
#             print_board(board, my_remaining_playtime1, opponent_time_left1, -player1, f"{current_player1} is playing on the following board")
#             current_player1, current_player2 = current_player2, current_player1
#             player1, player2 = player2, player1

#     # Print the final state of the board
#     print_board(board, my_remaining_playtime1, opponent_time_left1, -player1)

#     # Determine the winner
#     count_player1, count_player2 = get_winner(board, -player1)
#     print(f"Count of player1 and player2: ", count_player1, count_player2)

# # Run the game with the example players
# referee()


def referee():
    args = parse_args()
    # Initialize the game
    file_path = 'input.txt'
    # Create or overwrite the temp_output_allgames.txt file
    with open('temp_output_allgames.txt', 'w'):
        pass  # This just creates an empty file

    player, my_remaining_playtime, opponent_time_left, board = initialize_board(file_path)
    if args.player1 == 'Me':
        current_player = 'Me'
    else:
        current_player = 'AI'
    # current_player = 'Me'

    print_board(board, my_remaining_playtime, opponent_time_left, player, f"#######\tGame Starts\t######\n {current_player} is playing on the following board")

    while not is_game_over(board, player):
        if len(board.get_legal_moves(player)) != 0:
            print(f"{current_player} turn, {file_path}")
            my_time_left, opponent_time_left = write_output(file_path, 'output.txt', current_player)
            move = apply_move(board, 'output.txt')

            if move is not None:
                row, col = move
                board.execute_move((row, col), player)
                print_board(board, my_time_left, opponent_time_left, -player, f"{'AI' if current_player == 'Me' else 'Me'} is playing on the following board")
            else:
                print_board(board, my_time_left, opponent_time_left, -player, f"Same Board as above because no possible moves were available\n{'AI' if current_player == 'Me' else 'Me'} is playing on the following board")

            current_player = 'AI' if current_player == 'Me' else 'Me'
            file_path = 'temp_output.txt'
            player = -player
        else:
            # Switch to the other player for the next turn
            file_path = 'temp_output.txt'
            player, my_time_left, opponent_time_left, board = initialize_board(file_path)
            print_board(board, my_time_left, opponent_time_left, -player, f"{'AI' if current_player == 'Me' else 'Me'} is playing on the following board")
            current_player = 'AI' if current_player == 'Me' else 'Me'
            
            player = -player

    # Print the final state of the board
    print_board(board, my_time_left, opponent_time_left, -player)

    # Determine the winner
    count_player1, count_player2 = get_winner(board, -player)
    print(f"Count of player1 and player2: ", count_player1, count_player2)

# Run the game with the example players
referee()

