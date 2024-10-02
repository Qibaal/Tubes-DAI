import numpy as np
import itertools
import matplotlib.pyplot as plt  # Import for plotting

def hill_climbing_with_sideways_move(cube, max_sideways_moves=100, max_iterations=1000, max_repeated_swaps=3):
    """
    Solves the magic cube using Hill-climbing with Sideways Move by iteratively finding the best neighbors.
    Allows sideways moves (equal-cost moves) to escape plateaus. Stops if a swap happens repeatedly.

    Args:
    - cube (MagicCube): Instance of the MagicCube class containing the cube configuration.
    - max_sideways_moves (int): Maximum number of allowed sideways moves.
    - max_iterations (int): Maximum number of iterations.
    - max_repeated_swaps (int): Maximum number of repeated swaps before stopping.

    Returns:
    - solved (bool): Returns True if the cube is solved (i.e., cost is zero), False otherwise.
    """
    iteration = 0
    sideways_moves = 0  # Counter for the sideways moves
    current_cost = cube.calculate_cost()  # Initial cost
    cost_progress = []  # List to track cost at each iteration

    last_swaps = []  # List to keep track of the last swaps

    while current_cost > 0 and iteration < max_iterations:
        print(f"Iteration {iteration}: {current_cost} cost, Sideways moves: {sideways_moves}")
        
        best_cube = cube.cube.copy()  # Keep a copy of the current cube
        best_cost = current_cost  # Start with the current cost
        best_swap = None  # Track the best swap
        
        # Explore all possible pairs of positions (i.e., every possible neighbor)
        for pos1, pos2 in itertools.combinations(np.ndindex(cube.cube.shape), 2):
            new_cube = cube.cube.copy()
            
            # Swap the two elements
            new_cube[pos1], new_cube[pos2] = new_cube[pos2], new_cube[pos1]
            
            # Set the cube to the new state and calculate the cost
            cube.cube = new_cube
            new_cost = cube.calculate_cost()
            
            # If the new configuration has a lower or equal cost, update the best cube
            if new_cost < best_cost or (new_cost == best_cost and sideways_moves < max_sideways_moves):
                best_cost = new_cost
                best_cube = new_cube.copy()
                best_swap = (pos1, pos2)
                if new_cost == best_cost:
                    sideways_moves += 1  # Increment sideways moves counter when cost doesn't change
        
        # If no better configuration was found and sideways moves are exhausted, stop the algorithm
        if best_cost == current_cost and sideways_moves >= max_sideways_moves:
            print(f"Plateau reached with {sideways_moves} sideways moves, stopping.")
            break
        
        # Update the cube with the best found neighbor configuration
        cube.cube = best_cube
        current_cost = best_cost
        cost_progress.append(current_cost)  # Append the current cost to the progress list

        # Print details of the best swap
        if best_swap:
            pos1, pos2 = best_swap
            print(f"Swapped positions {pos1} and {pos2}, resulting in new cost: {current_cost}")
            print(f"Elements swapped: {cube.cube[pos1]}, {cube.cube[pos2]}")
            
            # Track repeated swaps
            if best_swap in last_swaps:
                last_swaps.append(best_swap)
            else:
                last_swaps = [best_swap]  # Reset tracking if new swap is found

            # If we have repeated the same swap too many times, stop
            if len(last_swaps) >= max_repeated_swaps and last_swaps[-max_repeated_swaps:] == [best_swap] * max_repeated_swaps:
                print(f"Repeated the same swap {best_swap} {max_repeated_swaps} times, stopping.")
                break

        iteration += 1

    # Final result after all iterations
    if current_cost == 0:
        print(f"Solved the magic cube in {iteration} iterations!")
        solved = True
    else:
        print(f"Stopped after {iteration} iterations with {current_cost} cost remaining.")
        solved = False

    # Plot the cost progress over iterations
    plt.plot(range(len(cost_progress)), cost_progress)
    plt.title("Cost Progression during Hill-Climbing with Sideways Moves")
    plt.xlabel("Iteration")
    plt.ylabel("Total Cost")
    plt.grid(True)
    plt.show()

    return solved
