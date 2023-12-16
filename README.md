# Chess Opening Trainer

This is a simple chess opening trainer using Stockfish evaluations to detect blunders in your first moves, and creating "puzzles" from them.

## Installation

You need to have Python 3 with `python-chess` installed:

```bash
$ pip install python-chess
```

Then get yourself a PGN with your games (google how to get that for Chess.com or Lichess.com game archive for example), and install Stockfish engine. If needed, modify this line in `process.py`:

```python
stockfish_path = '/usr/local/bin/stockfish'
```

Once you have the Python chess library and Stockfish, create a "blunder library":

```bash
$ python process.py mygames.pgn > games.js
```

## Usage

After you have a `games.js`, just open `trainer.html` in your browser!
Clicking "New problem" will pick a random situation from your games
library and let you try out different moves. Top 5 enginge choices are
considered "correct answers" and a blunder is defined as a move with
5 % or worse winning rate than top engine move (it's opening training).
