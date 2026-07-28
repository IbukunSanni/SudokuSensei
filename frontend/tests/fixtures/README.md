# Image-import fixtures

`sudoku-clean.svg` is the deterministic clean-grid baseline. Its expected
81-character puzzle is:

```text
530070000600195000098000060800060003400803001700020006060000280000419005000080079
```

Manual browser verification on 2026-07-28 recognized all 30 clues and all 51
blank cells correctly in approximately 46 seconds after grid detection,
perspective normalization, cell padding, blank detection, and nine row-level
OCR passes.

This is not a representative accuracy claim. Add photographed fixtures with
rotation, perspective distortion, shadows, blur, handwriting, and partial crops
before using image import accuracy as a release metric.
