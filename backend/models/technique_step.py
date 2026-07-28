from typing import Iterable, Tuple

from pydantic import BaseModel, Field, model_validator

from helpers.get_location import get_cell_location


class CandidateChange(BaseModel):
    """A validated candidate-set transition for one unsolved cell."""

    position: Tuple[int, int] = Field(
        ..., description="Zero-based row and column indices"
    )
    location: str = Field(..., description="Human-readable cell location")
    eliminated: list[int] = Field(
        ..., description="Candidates present before but absent afterward"
    )
    old_candidates: list[int] = Field(
        ..., description="Complete candidate set before the step"
    )
    new_candidates: list[int] = Field(
        ..., description="Complete candidate set after the step"
    )

    @classmethod
    def from_sets(
        cls,
        position: Tuple[int, int],
        old_candidates: Iterable[int],
        new_candidates: Iterable[int],
    ) -> "CandidateChange":
        old = sorted(set(old_candidates))
        new = sorted(set(new_candidates))
        return cls(
            position=position,
            location=get_cell_location(*position),
            eliminated=sorted(set(old) - set(new)),
            old_candidates=old,
            new_candidates=new,
        )

    @model_validator(mode="after")
    def validate_transition(self) -> "CandidateChange":
        old = set(self.old_candidates)
        new = set(self.new_candidates)
        eliminated = set(self.eliminated)

        if new - old:
            raise ValueError("A removal step cannot introduce new candidates")
        if eliminated != old - new:
            raise ValueError(
                "Eliminated candidates must equal old_candidates - new_candidates"
            )
        if not eliminated:
            raise ValueError("A candidate change must eliminate at least one candidate")

        self.old_candidates = sorted(old)
        self.new_candidates = sorted(new)
        self.eliminated = sorted(eliminated)
        return self


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
