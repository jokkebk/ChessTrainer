import chess.pgn
import chess.engine
import sys, json

stockfish_path = '/usr/local/bin/stockfish'

def evaluate_game(game):
    engine = chess.engine.SimpleEngine.popen_uci(stockfish_path)

    players = (game.headers['Black'], game.headers['White'])

    board = game.board()
    moves = list(game.mainline_moves())
    for move in moves[:6]: # First 10 moves only
        # Print the current player
        current_player = players[board.turn]
        current_color = "White" if board.turn else "Black"
        #print(f"Current player: {current_player} ({current_color})")

        # Analyze the position for top engine variations
        info = engine.analyse(board, chess.engine.Limit(time=0.1), multipv=5)
        #print("Top engine variations:")
        #for i, variation in enumerate(info, start=1):
        #    # Calculate winning probability 
        #    prob = 1 / (1 + 10 ** (-variation["score"].white().score() / 400))
        #    print(f"Option {i}: Move {variation['pv'][0]}, Evaluation: {prob:.2%}")
        best_prob = 1 / (1 + 10 ** (-info[0]["score"].white().score() / 400))

        # Store FEN of board position before move
        fen = board.fen()

        # Make the actual move and analyze
        board.push(move)
        actual_move_info = engine.analyse(board, chess.engine.Limit(time=0.1))
        actual_prob = 1 / (1 + 10 ** (-actual_move_info["score"].white().score() / 400))

        #print(f"\nActual move: {move}, Evaluation: {actual_prob:.2%}")
        #print(board.turn, actual_prob, best_prob)

        # If move's winning probability is significantly lower than the top variation, print a warning
        if (board.turn == chess.WHITE and actual_prob > best_prob + 0.05) or \
            (board.turn == chess.BLACK and actual_prob < best_prob - 0.05):
            # Create a dict with fen and alternate moves
            d = {
                "fen": fen,
                "players": players,
                "result": game.headers["Result"],
                "moves": [ ]
            }

            for i, variation in enumerate(info, start=1):
                # Calculate winning probability 
                prob = 1 / (1 + 10 ** (-variation["score"].white().score() / 400))
                d["moves"].append({
                    "move": variation['pv'][0].uci(),
                    "evaluation": prob
                })

            # Save worst to last
            d["moves"].append({
                "move": move.uci(),
                "evaluation": actual_prob
            })
            
            # Print JSON of the dict
            print(json.dumps(d), end=',\n')
            break

    engine.quit()

def list_games_from_pgn(file_path):
    with open(file_path) as pgn:
        games = 0

        print('const games = [')
        while True:
            game = chess.pgn.read_game(pgn)
            if game is None:
                break

            white = game.headers["White"]
            black = game.headers["Black"]
            result = game.headers["Result"]

            #print(f"White: {white}, Black: {black}, Result: {result}")
            evaluate_game(game)

        print('];')

list_games_from_pgn(sys.argv[1])