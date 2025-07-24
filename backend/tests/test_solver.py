"""
Test script to visualize the step-by-step solving process of a Sudoku puzzle.
"""

import requests
import json
import time
import os


def clear_screen():
    """Clear the console screen."""
    os.system("cls" if os.name == "nt" else "clear")


def print_grid(grid):
    """Print a Sudoku grid in a readable format."""
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


def test_solver():
    """Test the solver API and visualize the step-by-step solving process."""
    # Example puzzle (0 represents empty cells)
    puzzle = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9],
    ]

    # Send request to the solver API
    url = "http://localhost:8000/solve"
    headers = {"Content-Type": "application/json"}
    data = {"puzzle": puzzle}

    print("Sending puzzle to solver...")
    response = requests.post(url, headers=headers, json=data)

    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        print(response.text)
        return

    result = response.json()

    # Display solving steps
    print(f"\nPuzzle solved: {result['is_solved']}")
    print(f"Message: {result['message']}")
    print(f"Techniques applied: {', '.join(result['techniques_applied'])}")
    print("\nPress Enter to see each solving step...")
    input()

    # Display each step
    for i, step in enumerate(result["solving_steps"]):
        clear_screen()
        print(f"Step {i}: {step['technique']}")
        print(f"Description: {step['description']}")
        print(f"Cells solved in this step: {step['cells_solved']}")
        print_grid(step["grid"])
        if i < len(result["solving_steps"]) - 1:
            input("Press Enter for next step...")

    print("\nSolving process completed!")


if __name__ == "__main__":
    test_solver()
