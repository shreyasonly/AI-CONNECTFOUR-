
# Connect Four Game

## Description
This is a Python implementation of the classic game Connect Four. The game allows two players to take turns dropping colored discs into a vertically suspended grid. The objective is to connect four of one's own discs of the same color in a row, column, or diagonal before your opponent does.

## Features
- Supports different player types: AI, random, or human.
- Customizable time limit for AI players.
- Graphical user interface (GUI) using Tkinter.

## How to Play
1. Clone or download the repository to your local machine.
2. Navigate to the directory containing the game files.
3. Run the `ConnectFour.py` script with Python, providing the player types as command-line arguments. For example:
   ```
   python ConnectFour.py human ai
   ```
4. Follow the instructions displayed in the terminal or GUI to make your moves.
5. Enjoy the game!

## Command-Line Arguments
- `player1`: Type of player for player 1 (options: ai, random, human).
- `player2`: Type of player for player 2 (options: ai, random, human).
- `--time`: Optional argument to specify the time limit for AI players (in seconds).

Example usage:
```
python ConnectFour.py ai ai --time 3
```

## Requirements
- Python 3.x
- Tkinter library (usually included in standard Python installations)




