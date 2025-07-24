"""
Test the frontend-optimized solver with clear step separation.
"""

from services.frontend_solver import frontend_solver


def print_grid(grid, title="Grid"):
    """Print a Sudoku grid with title."""
    print(f"\n{title}:")
    print("┌───────┬───────┬───────┐")
    for i, row in enumerate(grid):
        print("│", end=" ")
        for j, cell in enumerate(row):
            print(cell if cell != 0 else ".", end=" ")
            if j % 3 == 2 and j < 8:
                print("│", end=" ")
        print("│")
        if i % 3 == 2 and i < 8:
            print("├───────┼───────┼───────┤")
    print("└───────┴───────┴───────┘")


def print_step_details(step, step_index):
    """Print detailed information about a solving step."""
    step_type = step.get("step_type", "unknown")

    # Different formatting based on step type
    if step_type == "initial_constraints":
        print(f"\n{'='*60}")
        print(f"🔧 INITIAL SETUP")
        print(f"{'='*60}")
        print(f"📋 {step['description']}")
        print(f"🔍 Candidates eliminated: {step['candidates_eliminated']}")
        print(f"💡 {step['explanation']}")

    elif step_type == "technique":
        print(f"\n{'='*60}")
        print(f"🧠 {step['technique'].upper()}")
        print(f"{'='*60}")
        print(f"📋 {step['description']}")
        print(f"💡 {step['explanation']}")

        if step["cells_solved"] > 0:
            print(f"✅ Cells filled: {', '.join(step['solved_positions'])}")

        if step.get("candidate_changes"):
            print(f"🔍 Technique eliminations: {len(step['candidate_changes'])}")
            for change in step["candidate_changes"][:3]:  # Show first 3
                eliminated = sorted(change["eliminated"])
                remaining = (
                    sorted(change["new_candidates"])
                    if change["new_candidates"]
                    else "solved"
                )
                print(f"   {change['location']}: removed {eliminated} → {remaining}")
            if len(step["candidate_changes"]) > 3:
                print(
                    f"   ... and {len(step['candidate_changes'])-3} more eliminations"
                )

    elif step_type == "constraint_elimination":
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

    # Show progress
    remaining = sum(1 for row in step["grid"] for cell in row if cell == 0)
    print(f"📊 Progress: {remaining} cells remaining")


def test_frontend_solver():
    """Test the frontend solver with step separation."""
    print("🧩 FRONTEND SUDOKU SOLVER - CLEAR STEP SEPARATION")
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

    # Solve with frontend solver
    result = frontend_solver.solve(puzzle)

    print(f"\n📊 Solving Summary:")
    print(f"   Puzzle solved: {result['is_solved']}")
    print(f"   Total logical steps: {result['total_logical_steps']}")
    print(f"   Total display steps: {len(result['solving_steps'])}")
    print(f"   Techniques used: {', '.join(result['techniques_applied'])}")

    print(f"\n🔍 Step-by-Step Process:")

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

    result = frontend_solver.solve(puzzle)

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
    test_frontend_solver()

    # Test 2: Step type analysis
    test_step_types()
