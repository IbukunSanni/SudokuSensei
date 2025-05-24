from colorama import Fore, Style


class Cell:
    def __init__(self, value=0, is_initial=False):
        self.value = value  # 1-9 or 0 for empty
        self.is_initial = is_initial  # True if part of original puzzle
        self._candidates = set(range(1, 10)) if value == 0 else set()

    def is_solved(self):
        return self.value != 0

    def get_candidates(self):
        return self._candidates

    def set_candidates(self, new_candidates):
        if not isinstance(new_candidates, set):
            raise ValueError("Candidates must be a set")
        self._candidates = new_candidates

    def __repr__(self):
        if self.value == 0:
            return Fore.YELLOW + "." + Style.RESET_ALL
        elif self.is_initial:
            return Fore.WHITE + str(self.value) + Style.RESET_ALL
        else:
            return Fore.BLUE + str(self.value) + Style.RESET_ALL
