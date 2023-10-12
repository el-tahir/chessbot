"""
Some example strategies for people who want to create a custom, homemade bot.
"""

from __future__ import annotations
import chess
from chess.engine import PlayResult
import random
from engine_wrapper import MinimalEngine
from typing import Any

import joblib

number_to_square = {
    1: 'a1',  2: 'a2',  3: 'a3',  4: 'a4',  5: 'a5',  6: 'a6',  7: 'a7',  8: 'a8',
    9: 'b1', 10: 'b2', 11: 'b3', 12: 'b4', 13: 'b5', 14: 'b6', 15: 'b7', 16: 'b8',
   17: 'c1', 18: 'c2', 19: 'c3', 20: 'c4', 21: 'c5', 22: 'c6', 23: 'c7', 24: 'c8',
   25: 'd1', 26: 'd2', 27: 'd3', 28: 'd4', 29: 'd5', 30: 'd6', 31: 'd7', 32: 'd8',
   33: 'e1', 34: 'e2', 35: 'e3', 36: 'e4', 37: 'e5', 38: 'e6', 39: 'e7', 40: 'e8',
   41: 'f1', 42: 'f2', 43: 'f3', 44: 'f4', 45: 'f5', 46: 'f6', 47: 'f7', 48: 'f8',
   49: 'g1', 50: 'g2', 51: 'g3', 52: 'g4', 53: 'g5', 54: 'g6', 55: 'g7', 56: 'g8',
   57: 'h1', 58: 'h2', 59: 'h3', 60: 'h4', 61: 'h5', 62: 'h6', 63: 'h7', 64: 'h8'
}


def chess_square_to_number(square: str) -> int:
    file = square[0]
    rank = int(square[1])
    file_dict = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8}
    return (file_dict[file] - 1) * 8 + rank

def chess_move_to_tuple(move):
  start_square = chess_square_to_number(move[:2])
  end_square = chess_square_to_number(move[2:])
  return (start_square, end_square)

def chess_moves_to_tuples(moves):
    """
    Converts a list of chess moves in the form of strings to a list of tuples
    representing the same moves as (start_square, end_square) where each square
    is represented by its corresponding number from 1 to 64.

    Parameters:
    moves (List[str]): A list of chess moves in the form of strings, e.g.
        ["d7d5", "c7c5", "b8c6", "g8f6"].

    Returns:
    List[Tuple[int, int]]: A list of tuples representing the same moves as
        (start_square, end_square) where each square is represented by its
        corresponding number from 1 to 64.
    """
    result = []
    for move in moves:
        result.append(chess_move_to_tuple(move))
    return result

model = joblib.load('final_model_chess.joblib')



class ExampleEngine(MinimalEngine):
    pass


# Strategy names and ideas from tom7's excellent eloWorld video

class Eltahir(ExampleEngine):
    def search(self, board: chess.Board, *args: Any) -> PlayResult:
        moves = []

        with chess.engine.SimpleEngine.popen_uci("stockfish\stockfish-windows-2022-x86-64-avx2.exe") as engine:
            result = engine.analyse(board, chess.engine.Limit(depth=5), multipv=10)
            for json in result:
                moves.append(json["pv"][0].uci())
        
        print(moves)
        
        candidates = chess_moves_to_tuples(moves)
        
        likelihoods = model.predict(candidates)
        sorted_candidates = sorted(candidates, key=lambda x: likelihoods[candidates.index(x)], reverse=False)
        final_move = number_to_square[sorted_candidates[0][0]] + number_to_square[sorted_candidates[0][1]]

        print("move chosen: " + final_move)
        return PlayResult(chess.Move.from_uci(final_move), None)

class RandomMove(ExampleEngine):
    def search(self, board: chess.Board, *args: Any) -> PlayResult:
        return PlayResult(random.choice(list(board.legal_moves)), None)


class Alphabetical(ExampleEngine):
    def search(self, board: chess.Board, *args: Any) -> PlayResult:
        moves = list(board.legal_moves)
        moves.sort(key=board.san)
        return PlayResult(moves[0], None)


class FirstMove(ExampleEngine):
    """Gets the first move when sorted by uci representation"""
    def search(self, board: chess.Board, *args: Any) -> PlayResult:
        moves = list(board.legal_moves)
        moves.sort(key=str)
        return PlayResult(moves[0], None)
