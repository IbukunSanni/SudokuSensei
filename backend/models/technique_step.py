class TechniqueStep:
    def __init__(
        self,
        technique,
        description,
        focus_cells,  # now always required, always a list
        value=None,
        eliminations=None,
        extra=None,
    ):
        """
        technique: str -- Name of the solving technique (e.g., "Naked Single")
        description: str -- Human-readable explanation
        focus_cells: list of (row, col) -- List of all cells directly involved, usually length 1 for singles
        value: int -- The value placed (if any)
        eliminations: list of dicts -- Each {candidate: [cell, ...]}, eliminated in this step
        extra: Optional, for additional technique-specific info
        """
        self.technique = technique
        self.description = description
        self.focus_cells = focus_cells
        self.value = value
        self.eliminations = eliminations or []
        self.extra = extra

    def to_dict(self):
        return {
            "technique": self.technique,
            "description": self.description,
            "focus_cells": self.focus_cells,
            "value": self.value,
            "eliminations": self.eliminations,
            "extra": self.extra,
        }
