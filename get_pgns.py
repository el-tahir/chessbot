import os
import re

def main():
    with open("input_games.pgn", "r") as f:
        content = f.read()

    games = content.strip().split("\n\n\n")

    if not os.path.exists("black_games"):
        os.makedirs("black_games")

    if not os.path.exists("white_games"):
        os.makedirs("white_games")

    game_index = 0

    for game in games:
        game_pgn = re.sub("\n{2,}", "\n\n", game.strip()) + "\n\n"
        if '[Black "EltahirAmin"]' in game:
            folder = "black_games"
        elif '[White "EltahirAmin"]' in game:
            folder = "white_games"
        else:
            continue

        with open(f"{folder}/game_{game_index}.pgn", "w") as output_file:
            output_file.write(game_pgn)

        game_index += 1

if __name__ == "__main__":
    main()
