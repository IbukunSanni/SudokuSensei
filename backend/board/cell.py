from colorama import Fore, Style


class Cell:
    def __init__(self, value=0, is_initial=False):
        self._value = value  # Private backing variable
        self.is_initial = is_initial
        self._candidates = set(range(1, 10)) if value == 0 else set()

    def is_solved(self):
        return self._value != 0

    # ✅ Getter for value
    def get_value(self):
        return self._value

    # ✅ Setter for value
    def set_value(self, new_value):
        if not isinstance(new_value, int) or not (0 <= new_value <= 9):
            raise ValueError("Value must be an integer between 0 and 9")
        self._value = new_value
        if new_value != 0:
            self._candidates = set()  # Clear candidates when solved

    # ✅ Getter for candidates
    def get_candidates(self):
        return self._candidates

    # ✅ Setter for candidates
    def set_candidates(self, new_candidates):
        if not isinstance(new_candidates, set):
            raise ValueError("Candidates must be a set")
        self._candidates = new_candidates

    def __repr__(self):
        if self._value == 0:
            return Fore.YELLOW + "." + Style.RESET_ALL
        elif self.is_initial:
            return Fore.WHITE + str(self._value) + Style.RESET_ALL
        else:
            return Fore.BLUE + str(self._value) + Style.RESET_ALL
