"""
Test the step-by-step solver that applies one technique at a time.
"""

from services.step_by_step_solver import step_by_step_solver


def print_grid(grid, title="Grid"):
    """Print a Sudoku grid with title."""
    print(f"\n{title}:")
    print("+-------+-------+-------+")
    for i, row in enumerate(grid):
        print("|", end=" ")
        for j, cell in enumerate(row):
            print(cell if cell != 0 else ".", end=" ")
            if j % 3 == 2 and j < 8:
                print("|", end=" ")
        print("|")
        if i % 3 == 2 and i < 8:
            print("+-------+-------+-------+")
    print("+-------+-------+-------+")


def print_step_details(step, step_index):
    """Print detailed information about a solving step."""
    step_type = step.get("step_type", "unknown")

    # Different formatting based on step type
    if step_type == "constraint_elimination":
        print(f"\n{'─'*60}")
        print(f"⚙️  CONSTRAINT PROPAGATION")
        print(f"{'─'*60}")
        print(f"📋 {step['description']}")
        print(f"💡 {step['explanation']}")

        if step.get("candidate_changes"):
            print(f"🔍 Constraint eliminations: {len(step['candidate_changes'])}")
            # Group eliminations by affected cells
            affected_cells = set()
            for change in step["candidate_changes"]:
                affected_cells.add(change["location"])

            print(f"   Affected cells: {', '.join(sorted(affected_cells)[:8])}")
            if len(affected_cells) > 8:
                print(f"   ... and {len(affected_cells)-8} more cells")

    else:  # technique step
        print(f"\n{'='*60}")
        print(f"🧠 {step.get('technique', 'UNKNOWN').upper()}")
        if step.get("step_number"):
            print(f"Step #{step['step_number']}")
        print(f"{'='*60}")
        print(f"📋 {step['description']}")
        if step.get("explanation"):
            print(f"💡 {step['explanation']}")

        if step.get("cells_solved", 0) > 0:
            print(f"✅ Cells filled: {', '.join(step.get('solved_positions', []))}")

        if step.get("focus_cells"):
            from helpers.get_location import get_cell_location

            focus_locations = [get_cell_location(r, c) for r, c in step["focus_cells"]]
            print(f"🎯 Focus cells: {', '.join(focus_locations)}")

        if step.get("value"):
            print(f"🔢 Value placed: {step['value']}")

        if step.get("candidate_changes"):
            print(f"🔍 Candidate eliminations: {len(step['candidate_changes'])}")
            for change in step["candidate_changes"][:3]:  # Show first 3
                eliminated = change.get("eliminated", [])
                print(f"   {change['location']}: removed {eliminated}")
            if len(step["candidate_changes"]) > 3:
                print(
                    f"   ... and {len(step['candidate_changes'])-3} more eliminations"
                )

    # Show progress
    remaining = sum(1 for row in step["grid"] for cell in row if cell == 0)
    print(f"📊 Progress: {remaining} cells remaining")


def test_step_by_step_solver():
    """Test the step-by-step solver that applies one technique at a time."""
    print("STEP-BY-STEP SUDOKU SOLVER - ONE TECHNIQUE AT A TIME")
    print("=" * 70)

    # Use a puzzle that will show multiple step types
    puzzle = [
        [0, 0, 0, 0, 3, 0, 0, 0, 8],
        [0, 4, 2, 0, 0, 0, 6, 0, 0],
        [6, 0, 9, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 5, 7, 0, 0, 4],
        [3, 0, 0, 0, 0, 0, 0, 0, 7],
        [2, 0, 0, 9, 4, 0, 0, 6, 0],
        [0, 0, 5, 0, 0, 3, 2, 0, 1],
        [0, 0, 1, 0, 0, 0, 0, 7, 0],
        [0, 0, 0, 0, 2, 0, 0, 0, 0],
    ]

    print_grid(puzzle, "Initial Puzzle")

    # Solve with step-by-step solver (applies one technique at a time)
    result = step_by_step_solver.solve(puzzle)

    print(f"\n Solving Summary:")
    print(f"   Puzzle solved: {result['is_solved']}")
    print(f"   Total steps: {result['total_steps']}")
    print(f"   Iterations: {result['iterations']}")
    print(f"   Techniques used: {', '.join(result['techniques_applied'])}")

    print(f"\n Step-by-Step Process:")

    # Show each step with clear separation
    for i, step in enumerate(result["solving_steps"]):
        print_step_details(step, i)

        # Show grid for first few steps or when cells are solved
        if i < 3 or step.get("cells_solved", 0) > 0:
            print_grid(step["grid"], f"Grid after this step")

    print(f"\n🏆 Final Result:")
    print(f"   {result['message']}")

    if result["is_solved"]:
        print_grid(result["solved_grid"], "Final Solution")

    return result


def test_step_types():
    """Test to verify step type separation."""
    print("\n\n🔍 STEP TYPE ANALYSIS")
    print("=" * 50)

    puzzle = [
        [0, 0, 0, 6, 0, 0, 4, 0, 0],
        [7, 0, 0, 0, 0, 3, 6, 0, 0],
        [0, 0, 0, 0, 9, 1, 0, 8, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 5, 0, 1, 8, 0, 0, 0, 3],
        [0, 0, 0, 3, 0, 6, 0, 4, 5],
        [0, 4, 0, 2, 0, 0, 0, 6, 0],
        [9, 0, 3, 0, 0, 0, 0, 0, 0],
        [0, 2, 0, 0, 0, 0, 1, 0, 0],
    ]

    result = step_by_step_solver.solve(puzzle)

    # Analyze step types
    step_types = {}
    for step in result["solving_steps"]:
        step_type = step.get("step_type", "unknown")
        if step_type not in step_types:
            step_types[step_type] = 0
        step_types[step_type] += 1

    print(f"Step Type Breakdown:")
    for step_type, count in step_types.items():
        print(f"   {step_type}: {count} steps")

    print(f"\nStep Sequence:")
    for i, step in enumerate(result["solving_steps"]):
        step_type = step.get("step_type", "unknown")
        technique = step.get("technique", "Unknown")
        cells_solved = step.get("cells_solved", 0)
        candidates_eliminated = step.get("candidates_eliminated", 0)

        print(
            f"   {i+1:2d}. {step_type:20} | {technique:15} | Cells: {cells_solved} | Eliminations: {candidates_eliminated}"
        )


if __name__ == "__main__":
    # Test 1: Main functionality
    test_step_by_step_solver()

    # Test 2: Step type analysis
    test_step_types()
