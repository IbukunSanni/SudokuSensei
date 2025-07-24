"""
Test script to verify the API works with the enhanced solver.
"""

import requests
import json


def test_api_enhanced():
    """Test the API with enhanced solver."""
    # Simple puzzle for testing
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

    url = "http://localhost:8000/solve"
    headers = {"Content-Type": "application/json"}
    data = {"puzzle": puzzle}

    print("Testing enhanced API...")
    try:
        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            result = response.json()
            print("✅ API request successful!")
            print(f"Puzzle solved: {result['is_solved']}")
            print(f"Message: {result['message']}")
            print(f"Techniques applied: {', '.join(result['techniques_applied'])}")
            print(f"Total solving steps: {len(result['solving_steps'])}")

            # Show first few steps
            print("\nFirst 3 solving steps:")
            for i, step in enumerate(result["solving_steps"][:3]):
                print(f"  Step {i}: {step['technique']}")
                print(f"    Description: {step['description']}")
                print(f"    Cells solved: {step['cells_solved']}")
                print(
                    f"    Candidates eliminated: {step.get('candidates_eliminated', 0)}"
                )

                # Show some solved positions if available
                if step.get("solved_positions"):
                    positions = step["solved_positions"][:5]  # First 5
                    print(f"    Sample solved positions: {', '.join(positions)}")
                print()

            return True
        else:
            print(f"❌ API request failed with status {response.status_code}")
            print(f"Response: {response.text}")
            return False

    except requests.exceptions.ConnectionError:
        print(
            "❌ Could not connect to API. Make sure the server is running on http://localhost:8000"
        )
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


if __name__ == "__main__":
    test_api_enhanced()
