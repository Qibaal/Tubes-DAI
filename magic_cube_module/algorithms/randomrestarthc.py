import numpy as np
import random
import itertools
import matplotlib.pyplot as plt  # Import library for plotting

def random_restart_hill_climbing(cube, max_restarts, max_iterations_per_restart=50):
    best_overall_cost = float('inf')
    best_overall_cube = cube.cube.copy()
    iterations_per_restart = []  # New array to track iterations for each restart
    best_steps = []  # Modified to store steps with index1, index2, cost format
    
    for restart in range(max_restarts):
        print(f"Restart {restart+1}/{max_restarts}")

        if restart > 0:
            numbers = list(range(1, cube.size**3 + 1))
            np.random.shuffle(numbers)
            cube.cube = np.array(numbers).reshape((cube.size, cube.size, cube.size))

        current_cost = cube.calculate_cost()
        steps = []  # Track steps for current restart
        iteration = 0

        while current_cost > 0 and iteration < max_iterations_per_restart:
            print(f"Iteration {iteration}: {current_cost} cost")

            best_cube = cube.cube.copy()
            best_cost = current_cost
            best_swap = None

            for pos1, pos2 in itertools.combinations(np.ndindex(cube.cube.shape), 2):
                new_cube = cube.cube.copy()
                new_cube[pos1], new_cube[pos2] = new_cube[pos2], new_cube[pos1]
                cube.cube = new_cube
                new_cost = cube.calculate_cost()

                if new_cost < best_cost:
                    best_cost = new_cost
                    best_cube = new_cube.copy()
                    best_swap = (pos1, pos2)

            if best_cost == current_cost:
                print("No better neighbors found, stopping hill-climbing.")
                steps.append({
                    'index1': 0,
                    'index2': 0,
                    'cost': current_cost
                })
                break

            if best_swap:
                pos1, pos2 = best_swap
                steps.append({
                    'index1': np.ravel_multi_index(pos1, cube.cube.shape),
                    'index2': np.ravel_multi_index(pos2, cube.cube.shape),
                    'cost': best_cost
                })

            cube.cube = best_cube
            current_cost = best_cost
            iteration += 1

        iterations_per_restart.append(iteration)  # Store iterations for this restart

        if current_cost < best_overall_cost:
            best_overall_cost = current_cost
            best_overall_cube = cube.cube.copy()
            best_steps = steps  # Store steps from best restart

        if current_cost == 0:
            break

    return best_overall_cost, best_overall_cube, len(best_steps), best_steps, iterations_per_restart