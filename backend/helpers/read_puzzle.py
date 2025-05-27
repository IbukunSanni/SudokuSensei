def read_puzzle(filename):
    board = []
    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            if len(line) == 9 and line.isdigit():
                row = [int(c) for c in line]
                board.append(row)
    return board
