# SudokuSensei Roadmap

This roadmap treats SudokuSensei as both a useful teaching product and a
deliberate path toward senior software engineering and graphics engineering.
Work from top to bottom. Avoid adding advanced techniques until the foundation
and solver event model are trustworthy.

## Current capabilities

- [x] Solve with Naked/Hidden Singles, Naked/Hidden Pairs, Naked Triples, and X-Wing.
- [x] Validate puzzle format, solvability, and solution uniqueness.
- [x] Expose full-solve, single-step, health, and candidate APIs.
- [x] Display candidates and identify candidates removed by a solving step.
- [x] Provide API integration tests and technique-level backend tests.
- [x] Track local development processes and cleanly restart both applications.

## P0 - Establish a trustworthy engineering baseline

### Consolidate the architecture

- [ ] Make `StepByStepSolver` the only production solver orchestration path.
- [ ] Remove or archive the unused `solver_service`, `frontend_solver`, and
      `advanced_solver`; decide whether the CLI still justifies `enhanced_solver`.
- [ ] Move all request/response models from `api/routes.py` into one model module.
- [ ] Remove the duplicate validators in `api/validators.py` and keep one
      validation implementation.
- [ ] Split `page.js` into focused components/hooks for puzzle state, playback,
      controls, and technique explanations.
- [ ] Move component-specific inline styles into co-located CSS Modules; keep
      `globals.css` limited to reset, typography, and design tokens.

Acceptance criteria:

- There is one solver registry and one definition of every API schema.
- No production module imports a legacy solver.
- No React component exceeds roughly 200 lines without a documented reason.

### Make solver state explicit

- [ ] Define typed domain objects for `Position`, `CandidateSet`,
      `CandidateChange`, `SolvedCell`, and `SolvingStep`.
- [ ] Give every step complete before/after candidate data instead of placeholder
      empty `old_candidates` and `new_candidates`.
- [ ] Separate pure board mutations from explanation formatting and API
      serialization.
- [ ] Add board invariants: solved cells have no candidates, unsolved cells never
      have impossible candidates, and every emitted elimination matches the
      before/after state.
- [ ] Replace domain-layer `print()` calls with structured logging at the
      application boundary.

Acceptance criteria:

- A step can be replayed from its input state to reproduce its output state.
- Candidate-removal explanations are derived from recorded state changes.
- Solver tests can run without producing console noise.

### Repository and tooling hygiene

- [ ] Ignore `.dev-processes.json`, server logs, caches, and build artifacts.
- [ ] Stop tracking generated `frontend/server.*.log` files.
- [ ] Normalize source files to UTF-8 and repair mojibake in comments and UI text.
- [ ] Replace the manually pinned runtime-only requirements file with
      `pyproject.toml` or separate runtime/dev dependency groups.
- [ ] Add Ruff for Python linting/formatting and keep ESLint for the frontend.
- [ ] Add GitHub Actions for backend tests, frontend lint, and production build.
- [ ] Add pre-commit hooks for formatting, linting, and accidental generated files.

Acceptance criteria:

- A fresh clone can install, test, build, and run from documented commands.
- CI performs the same checks expected locally and passes on the default branch.

## P1 - Build correctness and senior-level testing habits

### Strengthen automated verification

- [ ] Convert print-heavy demonstration tests into small arrange/act/assert tests.
- [ ] Add parameterized tests covering rows, columns, and boxes for every technique.
- [ ] Add negative tests proving techniques do not activate on near-miss patterns.
- [ ] Add property-based tests for board and candidate invariants with Hypothesis.
- [ ] Create a versioned puzzle corpus with expected solutions and technique traces.
- [ ] Add contract tests for `/candidates`, `/solve-step`, and `/solve`.
- [ ] Add Playwright tests for entering a puzzle, toggling candidates, applying a
      step, inspecting removals, and navigating backward/forward.
- [ ] Measure coverage, then target meaningful branch coverage rather than a
      percentage alone.

### Improve algorithm design and performance

- [ ] Profile solution validation and candidate propagation before optimizing.
- [ ] Use minimum-remaining-values selection in backtracking uniqueness checks.
- [ ] Benchmark easy, hard, expert, invalid, and non-unique puzzle datasets.
- [ ] Record technique runtime, iteration count, allocations, and candidate changes.
- [ ] Document time/space complexity and correctness reasoning for each technique.
- [ ] Add Swordfish only after X-Wing has complete positive, negative, and
      invariant tests.
- [ ] Build a puzzle generator that proves uniqueness and grades difficulty from
      the logical techniques required.

Acceptance criteria:

- Benchmarks are reproducible and stored separately from unit tests.
- Each optimization includes before/after measurements.
- New techniques include an explanation, invariant tests, and visualization data.

## P2 - Turn the solver into a strong teaching product

- [ ] Show the relevant row, column, or box for each technique, not only focus cells.
- [ ] Convert each solver step into a visual timeline with `prepare`, `focus`,
      `explain`, `remove`, `place`, and `settle` phases.
- [ ] Animate candidate removal as a before -> emphasized -> crossed-out -> after
      sequence instead of immediately replacing the board state.
- [ ] Animate solved values only after the logical cause has been shown.
- [ ] Keep animation state separate from solver state so pause, replay, and seeking
      never rerun or mutate the solver.
- [ ] Group removal explanations by cause and unit to avoid overwhelming users.
- [ ] Add pause, play, speed, scrubber, restart, and jump-to-technique controls.
- [ ] Let users inspect why a candidate exists before showing why it is removed.
- [ ] Add a "hint" mode that reveals progressively: unit -> pattern -> explanation ->
      result.
- [ ] Add keyboard navigation, screen-reader labels, non-color indicators, and
      contrast checks.
- [ ] Make the board responsive without losing candidate legibility.
- [ ] Persist a puzzle and playback position locally without persisting stale steps.
- [ ] Add a short lesson and worked example for every supported technique.

Acceptance criteria:

- A learner can explain the reason for a removal without reading backend terminology.
- Every solving step can be replayed deterministically at different animation speeds.
- Reduced-motion preferences replace motion with equivalent static state changes.
- The interface remains usable with keyboard-only input and at 200% zoom.
- Visual states are understandable without relying on color alone.

### Remove puzzle-entry friction with image import

- [x] First add paste/import for common 81-character and nine-line puzzle formats;
      this is the cheapest high-reliability alternative to manual cell entry.
- [ ] Add drag-and-drop, file-picker, clipboard-paste, and mobile camera inputs.
- [ ] Define an image-import pipeline with explicit stages: decode, orient, crop,
      detect grid, perspective-correct, split 81 cells, recognize digits, validate,
      and review.
- [ ] Use computer vision to detect the outer quadrilateral and apply a perspective
      transform before attempting digit recognition.
- [ ] Remove grid lines and normalize each cell with grayscale, adaptive thresholding,
      centering, and consistent padding.
- [ ] Establish a simple OCR baseline, but measure it on Sudoku images rather than
      assuming general document OCR will be accurate enough.
- [ ] Evaluate a small digit classifier exported to ONNX for recognizing only
      `blank` and digits `1-9`; run inference locally in the browser when practical.
- [ ] Return per-cell confidence and preprocessing/debug thumbnails from recognition.
- [ ] Add a mandatory review screen that highlights low-confidence or conflicting
      cells and allows fast keyboard correction before importing the puzzle.
- [ ] Validate the recognized grid for duplicate clues and solution feasibility before
      enabling solve or hint actions.
- [ ] Keep uploaded images on-device by default and clearly disclose any future
      server-side processing before upload.
- [ ] Build a labeled evaluation set containing screenshots, printed puzzles,
      perspective distortion, shadows, blur, handwriting, and partial crops.
- [ ] Track grid-detection success, per-cell digit accuracy, whole-puzzle accuracy,
      correction count, processing latency, and import abandonment rate.

Acceptance criteria:

- Recognition never silently accepts a low-confidence or invalid puzzle.
- Users can correct an imported puzzle without returning to manual 81-cell entry.
- Accuracy and latency are reported against a versioned, reproducible image dataset.
- The UI remains responsive while recognition runs in a worker.

## P3 - Create a graphics-engineering track inside the project

### Build a renderer-independent model

- [ ] Define a render scene containing cells, glyphs, candidates, highlights,
      eliminations, and animation timestamps.
- [ ] Keep solver state, playback state, and rendering state separate.
- [ ] Define a renderer interface so DOM, Canvas 2D, and future WebGL renderers
      consume the same scene.
- [ ] Add deterministic visual-state fixtures for renderer testing.

### Implement a Canvas 2D renderer

- [ ] Render the grid, values, candidate glyphs, and highlights on `<canvas>`.
- [ ] Handle device-pixel ratio correctly for sharp lines and text.
- [ ] Implement coordinate transforms, resizing, hit testing, and keyboard focus.
- [ ] Build a time-based animation loop using `requestAnimationFrame` and delta time.
- [ ] Interpolate candidate-removal and cell-solve transitions with easing functions.
- [ ] Compare DOM and Canvas performance using the same dense step trace.

### Progress to GPU rendering

- [ ] Learn the graphics pipeline by drawing the board with WebGL2 primitives.
- [ ] Batch/instance cell backgrounds and borders instead of issuing per-cell draws.
- [ ] Build a glyph atlas or signed-distance-field text renderer for digits.
- [ ] Write vertex and fragment shaders for focus, elimination, and solve effects.
- [ ] Add GPU timing where available and track CPU frame time, GPU frame time,
      draw calls, buffer uploads, and memory.
- [ ] Maintain a 60 FPS frame budget under a documented stress scenario.
- [ ] Explore WebGPU only after the WebGL2 renderer is measured and understood.

Acceptance criteria:

- The DOM and graphics renderers produce equivalent semantic states.
- Renderer benchmarks include hardware/browser context and reproducible inputs.
- Graphics work explains tradeoffs in batching, text rendering, precision, memory,
      synchronization, and accessibility.

## P4 - Practice senior engineering beyond implementation

- [ ] Write Architecture Decision Records for solver consolidation, step-event
      schema, renderer abstraction, and Canvas/WebGL adoption.
- [ ] Publish an API contract and versioning/deprecation policy.
- [ ] Add structured request IDs, error logging, latency metrics, and solver metrics.
- [ ] Define performance budgets and service-level objectives appropriate to the app.
- [ ] Add deployment, rollback, configuration, and troubleshooting documentation.
- [ ] Add dependency/security scanning and document threat boundaries.
- [ ] Create small releases with changelogs instead of accumulating one large branch.
- [ ] For each major feature, write a short design note covering goals, non-goals,
      alternatives, risks, rollout, and verification.
- [ ] Review completed work with a retrospective: what failed, what evidence changed
      the design, and what should become a reusable engineering rule.

## Deferred until evidence supports them

- [ ] Batch parallelism: add only after benchmarks show a real batch workload.
- [ ] Monitoring dashboard: add after meaningful metrics and operational questions exist.
- [ ] Machine learning: do not add until there is a concrete task where deterministic
      algorithms are insufficient and an evaluation dataset exists.

## Definition of done

A roadmap item is complete only when:

- behavior and non-goals are documented;
- implementation has focused automated tests;
- lint, tests, and production build pass;
- performance-sensitive work includes measurements;
- user-facing behavior includes accessibility and error states;
- documentation reflects the final design;
- generated files and unrelated changes are not included in the commit.
