import re

with open("Assignement 2/Stockfish_15_64-bit.commented.[2600].pgn", 'r') as f:

    # Read the file contents
    pgn = f.read()

    # Use regular expressions to extract the moves
    moves_regex = re.compile('\d+\.\s+(\S+)')
    moves = moves_regex.findall(pgn)

    # Print the moves
    for i, move in enumerate(moves):
        print(f"{i+1}. {move}")
