import numpy as np
import random
import matplotlib.pyplot as plt  # Import for plotting

def stochastic_hill_climbing(cube, max_iterations=1000):
    iteration = 0
    current_cost = cube.calculate_actual_cost()
    steps = []  # Track steps with index swaps and cost

    while current_cost > 0 and iteration < max_iterations:
        print(f"Iteration {iteration}: {current_cost} cost")
        
        new_cube = cube.cube.copy()
        
        pos1 = tuple(random.randint(0, cube.size - 1) for _ in range(3))
        pos2 = tuple(random.randint(0, cube.size - 1) for _ in range(3))
        
        while pos1 == pos2:
            pos2 = tuple(random.randint(0, cube.size - 1) for _ in range(3))
        
        new_cube[pos1], new_cube[pos2] = new_cube[pos2], new_cube[pos1]
        
        cube.cube = new_cube
        new_cost = cube.calculate_actual_cost()

        if new_cost < current_cost:
            print(f"Accepted new configuration by swapping {pos1} and {pos2}, new cost: {new_cost}")
            steps.append({'index1': pos1[0] * cube.size**2 + pos1[1] * cube.size + pos1[2], 
                          'index2': pos2[0] * cube.size**2 + pos2[1] * cube.size + pos2[2], 
                          'cost': new_cost})
            current_cost = new_cost
        else:
            cube.cube[pos1], cube.cube[pos2] = cube.cube[pos2], cube.cube[pos1]
            steps.append({'index1': 0, 'index2': 0, 'cost': current_cost})

        iteration += 1

    return current_cost, cube.cube, iteration, steps