import numpy as np
import random
import itertools
import matplotlib.pyplot as plt  # Import library for plotting

def random_restart_hill_climbing(cube, max_restarts=10, max_iterations_per_restart=1000):
    """
    Solves the magic cube using Random Restart Hill-climbing.
    Args:
    - cube (MagicCube): Instance of the MagicCube class containing the cube configuration.
    - max_restarts (int): The maximum number of random restarts.
    - max_iterations_per_restart (int): The maximum number of iterations for each hill-climbing run.
    
    Returns:
    - best_cost (int): The best cost found across all restarts.
    - best_cube (np.ndarray): The best cube configuration found.
    - total_iterations (int): Total iterations taken in the best restart.
    - restarts (int): The number of restarts performed.
    - obj_values (list): Objective values at each iteration of the best run.
    """
    best_overall_cost = float('inf')
    best_overall_cube = cube.cube.copy()
    best_obj_values = []
    best_iterations = 0

    all_fitness_progress = []  # List to store all fitness values across restarts

    for restart in range(max_restarts):
        print(f"Restart {restart+1}/{max_restarts}")
        
        # Randomize the cube's initial state (except on the first restart)
        if restart > 0:
            numbers = list(range(1, cube.size**3 + 1))
            np.random.shuffle(numbers)
            cube.cube = np.array(numbers).reshape((cube.size, cube.size, cube.size))
        
        current_cost = cube.calculate_actual_cost()  # Calculate the cost for the randomized cube
        fitness_progress = []  # Track fitness progress for this restart
        iteration = 0

        while current_cost > 0 and iteration < max_iterations_per_restart:
            print(f"Iteration {iteration}: {current_cost} cost")
            fitness_progress.append(current_cost)
            
            best_cube = cube.cube.copy()
            best_cost = current_cost
            best_swap = None
            
            for pos1, pos2 in itertools.combinations(np.ndindex(cube.cube.shape), 2):
                new_cube = cube.cube.copy()
                new_cube[pos1], new_cube[pos2] = new_cube[pos2], new_cube[pos1]
                cube.cube = new_cube
                new_cost = cube.calculate_actual_cost()
                
                if new_cost < best_cost:
                    best_cost = new_cost
                    best_cube = new_cube.copy()
                    best_swap = (pos1, pos2)
            
            if best_cost == current_cost:
                print("No better neighbors found, stopping hill-climbing.")
                break
            
            cube.cube = best_cube
            current_cost = best_cost

            if best_swap:
                pos1, pos2 = best_swap
                print(f"Swapped positions {pos1} and {pos2}, resulting in new cost: {current_cost}")
            
            iteration += 1
        
        all_fitness_progress.append(fitness_progress)

        if current_cost < best_overall_cost:
            best_overall_cost = current_cost
            best_overall_cube = cube.cube.copy()
            best_obj_values = fitness_progress
            best_iterations = iteration
        
        if current_cost == 0:
            print(f"Solved the magic cube in {iteration} iterations during restart {restart+1}!")
            plt.plot(fitness_progress)
            plt.title(f"Fitness Progression in Restart {restart+1}")
            plt.xlabel("Iterations")
            plt.ylabel("Cost (Fitness)")
            plt.grid(True)
            plt.show()
            break  # Exit if solved

    for idx, fitness_progress in enumerate(all_fitness_progress):
        plt.plot(fitness_progress, label=f"Restart {idx+1}")
    
    plt.title("Cost Progression Across All Restarts")
    plt.xlabel("Iterations")
    plt.ylabel("Cost")
    plt.legend()
    plt.grid(True)
    plt.show()
    
    return best_overall_cost, best_overall_cube, best_iterations, max_restarts, best_obj_values

