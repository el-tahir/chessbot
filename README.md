# Chess Move Prediction Project

This project aims to predict the next chess move made by a player given a specific board position. The dataset used to train the model is derived from a collection of PGN (Portable Game Notation) files containing the player's games. The project uses Python for data processing and machine learning model training.

## Project Structure

The project consists of three main Python scripts and a Jupyter Notebook:

1. `get_pgns.py`: This script is responsible for splitting the input games from the `input_games.pgn` file into separate PGN files for black and white games.
2. `get_csv.py`: This script is responsible for converting the PGN files into a CSV format that can be used for model training. The output CSV files contain information about each move and the top 10 moves recommended by Stockfish.
3. `main.ipynb`: This Jupyter Notebook loads the dataset, preprocesses the data, trains a machine learning model, and evaluates the model's performance.
4. `final_model_chess.joblib`: This file contains the trained model saved after executing the Jupyter Notebook.

## Installation Requirements

To run this project, you need to have the following packages installed:

- Python 3.7 or higher
- pandas
- numpy
- scikit-learn
- chess
- python-chess
- joblib

You can install these packages using pip:

```bash
pip install pandas numpy scikit-learn chess python-chess joblib
```

Additionally, you need to have [Stockfish](https://stockfishchess.org/download/) installed on your system. Replace `YOUR_PATH_TO_STOCKFISH_HERE` in `get_csv.py` with the path to your installed Stockfish executable.

## Usage

1. Run `get_pgns.py` to split the input games from the `input_games.pgn` file into separate PGN files for black and white games. This will create two directories: `black_games` and `white_games`.

```bash
python get_pgns.py
```

2. Run `get_csv.py` to convert the PGN files into CSV files (`black_df_100.csv` and `white_df_100.csv`). These CSV files contain the required information for model training.

```bash
python get_csv.py
```

3. Open `main.ipynb` using Jupyter Notebook and run all the cells. This will preprocess the data, train a machine learning model, and evaluate the model's performance. The trained model will be saved as `final_model_chess.joblib`.

```bash
jupyter notebook main.ipynb
```

## Model Evaluation

The model's performance is evaluated using two metrics:

1. Pure Accuracy: The proportion of times the top predicted move matches the target move.
2. Random Selection Accuracy: The proportion of times a randomly selected move from the top candidates matches the target move.

After running the `main.ipynb` notebook, you will see the comparison of these two accuracies.

## Deployment on Lichess

The model was trained on a sample of games played by [@EltahirAmin](https://lichess.org/@/EltahirAmin) and has been deployed on Lichess as a bot, [@EltahirAminBot](https://lichess.org/@/EltahirAminBot). The bot utilizes the [lichess-bot](https://github.com/ShailChoksi/lichess-bot) repository for integration with the Lichess API.

You can play against the bot at the following link:

[https://lichess.org/@/EltahirAminBot](https://lichess.org/@/EltahirAminBot)

To deploy your own version of the bot, follow the instructions in the [lichess-bot](https://github.com/lichess-bot-devs/lichess-bot) repository. After setting up the lichess-bot, replace the engine with the `final_model_chess.joblib` file and configure the bot to use your custom-trained model instead of the default engine.

Please note that the performance of the bot may vary depending on the quality of the training data and the model's ability to generalize to new positions.
