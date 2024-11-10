import numpy as np
import itertools

def steepest_ascent_hill_climbing(cube):
    max_iterations = 1000  # Define the maximum number of iterations allowed
    iteration = 0
    current_cost = cube.calculate_cost()  # Initial cost
    obj_values = []  # Collect the objective values for each iteration
    steps = []  # Collect step data

    best_cube = cube.cube.copy()  # Keep a copy of the initial cube

    # Iterate until there are no conflicts (cost == 0) or max iterations are reached
    while current_cost > 0 and iteration < max_iterations:
        obj_values.append(current_cost)  # Record the current cost
        print(f"Iteration {iteration}: {current_cost} cost")

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

        # If no better configuration was found, stop the algorithm (local minimum)
        if best_cost == current_cost:
            print("No better neighbors found, stopping.")
            return best_cost, best_cube, iteration, steps

        # Update the cube with the best found neighbor configuration
        cube.cube = best_cube
        current_cost = best_cost

        # Print details of the best swap and record the step
        if best_swap:
            pos1, pos2 = best_swap
            step_info = {
                "index1": pos1[0] * cube.size**2 + pos1[1] * cube.size + pos1[2],
                "index2": pos2[0] * cube.size**2 + pos2[1] * cube.size + pos2[2],
                "cost": current_cost
            }
            steps.append(step_info)
            print(f"Step {iteration + 1}: {step_info}")
            print(f"Swapped positions {pos1} and {pos2}, resulting in new cost: {current_cost}")
            print(f"Elements swapped: {cube.cube[pos1]}, {cube.cube[pos2]}")
        else:
            steps.append({"index1": 0, "index2": 0, "cost": current_cost})

        iteration += 1

    return current_cost, best_cube, iteration, steps