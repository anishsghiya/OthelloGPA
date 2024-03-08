# OthelloGPA
Game Playing Agent with dynamically changing search depth

## Description
This is a simple implementation of the Othello (Reversi) game. Othello is a classic board game for two players where the goal is to have the majority of discs turned to display your color at the end of the game.

## Features
- Player vs. Player (PvP) gameplay
- Standard Othello rules
- Command-line interface

## How to Play
1. Clone the repository to your local machine.
2. Navigate to the project directory.
3. Run the Othello game script.
4. Follow the on-screen instructions to make moves.
5. The game ends when there are no legal moves left for both players or the board is full.

## Sample Game
A sample Game is in the temp_output_allgames.txt

## How to Play
```python refree.py --player1 <AI or Me>```

## Me
My othello game agent employs the Minimax algorithm with alpha-beta pruning, enhanced by a transposition table present in ```lookup.py```and Zobrist hashing. Additionally, it dynamically adjusts the search depth based on the remaining time, optimizing the AI's decision-making process for a more challenging and efficient gameplay experience.

## Requirements
- Python 3.10.9

## Installation
```
git clone <repository_url>
cd OthelloGPA
python refree.py
```

## Credits
Author: Anish Ghiya
GitHub: anishsghiya
