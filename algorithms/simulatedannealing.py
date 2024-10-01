import numpy as np
import random
import math
import matplotlib.pyplot as plt  # Import for plotting

def simulated_annealing(cube, initial_temperature=1000, cooling_rate=0.99, min_temperature=1):
    """
    Solves the magic cube using Simulated Annealing.

    Args:
    - cube (MagicCube): Instance of the MagicCube class containing the cube configuration.
    - initial_temperature (float): Starting temperature for the annealing process.
    - cooling_rate (float): Rate at which the temperature decreases.
    - min_temperature (float): The minimum temperature at which to stop the algorithm.

    Returns:
    - solved (bool): Returns True if the cube is solved (i.e., cost is zero), False otherwise.
    """
    current_temperature = initial_temperature
    current_cost = cube.calculate_cost()
    cost_progress = []  # List to track cost at each iteration
    
    iteration = 0
    
    while current_temperature > min_temperature and current_cost > 0:
        print(f"Iteration {iteration}: Current cost = {current_cost}, Temperature = {current_temperature}")
        
        # Track the current cost for plotting later
        cost_progress.append(current_cost)
        
        # Generate a neighbor by swapping two random positions in the cube
        new_cube = cube.cube.copy()
        pos1 = tuple(random.randint(0, cube.size - 1) for _ in range(3))
        pos2 = tuple(random.randint(0, cube.size - 1) for _ in range(3))
        
        # Ensure that the two positions are not the same
        while pos1 == pos2:
            pos2 = tuple(random.randint(0, cube.size - 1) for _ in range(3))
        
        # Swap the elements
        new_cube[pos1], new_cube[pos2] = new_cube[pos2], new_cube[pos1]
        
        # Calculate the cost of the new configuration
        cube.cube = new_cube
        new_cost = cube.calculate_cost()
        
        # Determine if we accept the new configuration
        cost_difference = new_cost - current_cost
        if cost_difference < 0:
            # Accept the new configuration if it's better
            current_cost = new_cost
        else:
            # Accept the new configuration with a certain probability if it's worse
            probability = math.exp(-cost_difference / current_temperature)
            if random.random() < probability:
                current_cost = new_cost
            else:
                # Revert the cube back to its previous state if not accepted
                cube.cube[pos1], cube.cube[pos2] = cube.cube[pos2], cube.cube[pos1]
        
        # Cool down the temperature
        current_temperature *= cooling_rate
        
        iteration += 1

    # Final result
    if current_cost == 0:
        print(f"Solved the magic cube in {iteration} iterations!")
        solved = True
    else:
        print(f"Stopped after {iteration} iterations with {current_cost} cost remaining.")
        solved = False

    # Plot the cost progress over iterations
    plt.plot(range(len(cost_progress)), cost_progress)
    plt.title("Cost Progression during Simulated Annealing")
    plt.xlabel("Iteration")
    plt.ylabel("Total Cost")
    plt.grid(True)
    plt.show()

    return solved
