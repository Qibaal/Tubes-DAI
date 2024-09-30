import numpy as np
import random
import itertools

def random_restart_hill_climbing(cube, max_restarts=10, max_iterations_per_restart=1000):
    """
    Solves the magic cube using Random Restart Hill-climbing.
    It performs hill-climbing until a local minimum is reached, then restarts with a new random configuration.
    
    Args:
    - cube (MagicCube): Instance of the MagicCube class containing the cube configuration.
    - max_restarts (int): The maximum number of random restarts.
    - max_iterations_per_restart (int): The maximum number of iterations for each hill-climbing run.
    
    Returns:
    - solved (bool): Returns True if the cube is solved (i.e., cost is zero), False otherwise.
    """
    for restart in range(max_restarts):
        print(f"Restart {restart+1}/{max_restarts}")
        
        # Randomize the cube's initial state (except on the first restart)
        if restart > 0:
            numbers = list(range(1, cube.size**3 + 1))
            np.random.shuffle(numbers)
            cube.cube = np.array(numbers).reshape((cube.size, cube.size, cube.size))
        
        current_cost = cube.calculate_cost()  # Calculate the cost for the randomized cube
        
        # Perform hill-climbing for this restart
        iteration = 0
        while current_cost > 0 and iteration < max_iterations_per_restart:
            print(f"Iteration {iteration}: {current_cost} cost")
            
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
                
                # If the new configuration has a lower cost, update the best cube
                if new_cost < best_cost:
                    best_cost = new_cost
                    best_cube = new_cube.copy()
                    best_swap = (pos1, pos2)  # Track the swap
            
            # If no better configuration was found, stop the hill-climbing for this restart (local minimum)
            if best_cost == current_cost:
                print("No better neighbors found, stopping hill-climbing.")
                break
            
            # Update the cube with the best found neighbor configuration
            cube.cube = best_cube
            current_cost = best_cost
            
            # Print details of the best swap
            if best_swap:
                pos1, pos2 = best_swap
                print(f"Swapped positions {pos1} and {pos2}, resulting in new cost: {current_cost}")
                print(f"Elements swapped: {cube.cube[pos1]}, {cube.cube[pos2]}")
            
            iteration += 1
        
        # If the cube is solved, return success
        if current_cost == 0:
            print(f"Solved the magic cube in {iteration} iterations during restart {restart+1}!")
            return True
    
    # If after all restarts, the solution was not found
    print(f"Stopped after {max_restarts} restarts with {current_cost} cost remaining.")
    return False
