import chess
import chess.engine
import chess.pgn
import os
import pandas as pd
import numpy as np

# STOCKFISH_PATH = STOCKFISH_PATH

STOCKFISH_PATH = "YOUR_PATH_TO_STOCKFISH_HERE"

# Define column names for the data frame
cols = ['Move', 'From_Square', 'Target_Square', 'Piece_Moved', 'Piece_Captured', 'Is_Check', 'FEN', 'Top_10_Moves']


def get_top_moves(fen, n=10):
    """
    Get top n moves for a given FEN.

    :param fen: FEN of the board position
    :param n: Number of top moves to return
    :return: List of top n moves
    """
    # Set up the chess board from the FEN
    board = chess.Board(fen)

    # Create an instance of the Stockfish chess engine
    with chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH) as engine:

        # Run the engine analysis for the given position
        result = engine.analyse(board, chess.engine.Limit(depth=5), multipv=n)

        moves = []
        for json in result:
            moves.append(json["pv"][0].uci())

    return moves


def get_standard(move, board):
    """
    Get a standard representation of a move.

    :param move: The move to get the standard representation for
    :param board: The current board position
    :return: The standard representation of the move
    """
    prev_piece = board.piece_at(move.from_square)
    return ("" if prev_piece.symbol() == 'p' or prev_piece.symbol() == 'P' else prev_piece.symbol()) + move.uci()[2:]


def get_df_from_pgn(file_path, color='black'):
    """
    Create a data frame with game data from a PGN file.

    :param file_path: Path to the PGN file
    :param color: Color of the player to analyze (default is 'black')
    :return: Data frame containing the game data
    """
    pgn = open(file_path)

    df = pd.DataFrame(columns=cols)

    game = chess.pgn.read_game(pgn)

    board = game.board()

    game.mainline_moves()

    i = 0

    for move in game.mainline_moves():
        prev_piece = board.piece_at(move.from_square)
        post_piece = board.piece_at(move.to_square)
        old_fen = board.fen()
        board.push(move)
        if (i % 2 != 0) and (color == 'black') or (i % 2 == 0) and (color == 'white'):
            new_row = pd.Series({
                'Move': move.uci(),
                'From_Square': chess.square_name(move.from_square),
                'Target_Square': chess.square_name(move.to_square),
                'Piece_Moved': prev_piece,
                'Piece_Captured': post_piece,
                'Is_Check': board.is_check(),
                'FEN': old_fen,
                'Top_10_Moves': get_top_moves(old_fen)
            }, name=i, index=df.columns)

            df = df.append(new_row)

        i += 1

    return df


def create_data_frames(folder_path, color='black', number_of_games=100):
    """
    Create data frames with game data from PGN files in a folder.

    :param folder_path: Path to the folder containing PGN files
    :param color: Color of the player
    to analyze (default is 'black')
    :param number_of_games: Number of games to analyze (default is 100)
    :return: Data frame containing the game data
    """
    df = pd.DataFrame(columns=cols)

    # List all files in the folder
    files = os.listdir(folder_path)

    x = 0

    # Loop through each file and open it
    for file in files:
        file_path = os.path.join(folder_path, file)

        x += 1

        if x == number_of_games:
            break

        # Check if it's a file and not a directory
        if os.path.isfile(file_path):
            # Open and read the file
            df = pd.concat([df, get_df_from_pgn(file_path, color)])

    return df

def main():
    number_of_games = 100
    black_folder_path = r"black_games"
    black_df = create_data_frames(black_folder_path, 'black', number_of_games)

    white_folder_path = r"white_games"
    white_df = create_data_frames(white_folder_path, 'white', number_of_games)

    black_df.to_csv('black_df_100.csv', index=False)
    white_df.to_csv('white_df_100.csv', index=False)

if __name__ == '__main__':
    main()
    


