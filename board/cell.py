class Cell:
    def __init__(self, value=0):
        self.value = value  # 1-9 or 0 for empty
        self.candidates = set(range(1, 10)) if value == 0 else set()

    def is_solved(self):
        return self.value != 0

    def __repr__(self):
        return str(self.value) if self.value != 0 else "."
