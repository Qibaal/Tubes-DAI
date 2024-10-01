import numpy as np
import random
import matplotlib.pyplot as plt  # Import for plotting

def stochastic_hill_climbing(cube, max_iterations=1000):
    """
    Solves the magic cube using Stochastic Hill-climbing by randomly selecting a neighbor (two swapped elements).
    If the new neighbor has a lower cost, it becomes the current state.

    Args:
    - cube (MagicCube): Instance of the MagicCube class containing the cube configuration.
    - max_iterations (int): Maximum number of iterations allowed (default is 1000).

    Returns:
    - solved (bool): Returns True if the cube is solved (i.e., cost is zero), False otherwise.
    """
    iteration = 0
    current_cost = cube.calculate_cost()  # Initial cost
    cost_progress = []  # List to track cost at each iteration

    # Iterate until the cube is solved or max iterations are reached
    while current_cost > 0 and iteration < max_iterations:
        print(f"Iteration {iteration}: {current_cost} cost")
        
        # Record the current cost for plotting
        cost_progress.append(current_cost)
        
        # Copy the current cube configuration
        new_cube = cube.cube.copy()
        
        # Randomly select two positions in the cube to swap
        pos1 = tuple(random.randint(0, cube.size - 1) for _ in range(3))
        pos2 = tuple(random.randint(0, cube.size - 1) for _ in range(3))
        
        # Ensure the two positions are different before swapping
        while pos1 == pos2:
            pos2 = tuple(random.randint(0, cube.size - 1) for _ in range(3))
        
        # Swap the two elements
        new_cube[pos1], new_cube[pos2] = new_cube[pos2], new_cube[pos1]
        
        # Set the cube to the new state and calculate the cost
        cube.cube = new_cube
        new_cost = cube.calculate_cost()

        # If the new configuration has a lower cost, accept the change
        if new_cost < current_cost:
            print(f"Accepted new configuration by swapping {pos1} and {pos2}, new cost: {new_cost}")
            current_cost = new_cost
        else:
            # Reject the new configuration and revert to the old state
            cube.cube[pos1], cube.cube[pos2] = cube.cube[pos2], cube.cube[pos1]
        
        iteration += 1

    # Plot the cost progression over iterations
    plt.plot(range(len(cost_progress)), cost_progress)
    plt.title("Cost Progression during Stochastic Hill-Climbing")
    plt.xlabel("Iteration")
    plt.ylabel("Total Cost")
    plt.grid(True)
    plt.show()

    # Final result after all iterations
    if current_cost == 0:
        print(f"Solved the magic cube in {iteration} iterations!")
        return True
    else:
        print(f"Stopped after {iteration} iterations with {current_cost} cost remaining.")
        return False
