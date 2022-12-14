# Leela Zero against Other Top Chess Engines

In 2017 AlphaZero revolutionized modern chess engines by defeating 
the World Champion, Stockfish 8. Today, we look at how well Leela Zero,
the open source version of AlphaZero, does against modern chess engines.
You can run the code yourself, read the paper "Final Paper.pdf",
look through the PowerPoint at "RL Chess Final Presentation.pptx", or
watch a brief YouTube discussion of the results at https://youtu.be/OkPG3JSmUQE.

## How to run the code

You will need to install any chess engines onto your PC that you
want to play against each other. Then, you will need to refer to
their paths in the read_engines.py file and delete my paths.

After that, you can play games between engines using either the 
ChessGame class defined in play_single_game.py or the functions
defined in play_multiple_games.py. You can define the number of
seconds per move and the initial board position for your games.

Once a game finishes, its pgn file will be stored in the pgn-files
directory. You can then upload this pgn file to your favorite chess
UCI to see these games play out in real time. You can also save an
evaluation plot in the pgn-files directory based on your input arguments.

You can draw two stacked bar charts of the results by running code as
seen in stacked_bar_chart.py.

