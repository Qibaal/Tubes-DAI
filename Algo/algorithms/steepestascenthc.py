import numpy as np
import itertools
import matplotlib.pyplot as plt  # Import for plotting

def steepest_ascent_hill_climbing(cube):
    max_iterations = 1000  # Define the maximum number of iterations allowed
    iteration = 0
    current_cost = cube.calculate_cost()  # Initial cost
    # cost_progress = [] 
    data = []
    final_cost = 9999
    
    # Iterate until there are no conflicts (cost == 0) or max iterations are reached
    while current_cost > 0 and iteration < max_iterations:
        print(f"Iteration {iteration}: {current_cost} cost")
        
        # Append the current cost to the progress list for plotting later
        # cost_progress.append(current_cost)

        
        best_cube = cube.cube.copy()  # Keep a copy of the current cube
        best_cost = current_cost  # Start with the current cost
        best_swap = None  # Track the best swap
        new_cost = 0
        
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


        # If no better configuration was found, stop the algorithm (local minimum)
        if best_cost == current_cost:
            print("No better neighbors found, stopping.")
            return best_cost, best_cube
        
        # Update the cube with the best found neighbor configuration
        cube.cube = best_cube
        current_cost = best_cost
        
        # Print details of the best swap
        if best_swap:
            pos1, pos2 = best_swap
            print(f"Swapped positions {pos1} and {pos2}, resulting in new cost: {current_cost}")
            print(f"Elements swapped: {cube.cube[pos1]}, {cube.cube[pos2]}")

        iteration += 1
    
    
    # # Plot the cost progression over iterations
    # plt.plot(range(len(cost_progress)), cost_progress)
    # plt.title("Cost Progression during Steepest Ascent Hill-Climbing")
    # plt.xlabel("Iteration")
    # plt.ylabel("Total Cost")
    # plt.grid(True)
    # plt.show()
    
