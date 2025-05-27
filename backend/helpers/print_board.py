from colorama import Fore, Style, init

init(autoreset=True)  # This resets color after each print so it doesn't bleed


def print_input_puzzle(board):
    for i, row in enumerate(board):
        if i % 3 == 0 and i != 0:
            print("-" * 21)
        row_str = ""
        for j, num in enumerate(row):
            if j % 3 == 0 and j != 0:
                row_str += " | "
            if num != 0:
                row_str += Fore.WHITE + str(num) + Style.RESET_ALL + " "
            else:
                row_str += Fore.BLUE + "." + Style.RESET_ALL + " "
        print(row_str)
