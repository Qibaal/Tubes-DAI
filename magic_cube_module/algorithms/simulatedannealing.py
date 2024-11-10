import numpy as np
import random
import math
from tqdm import tqdm

def simulated_annealing(cube,
                       initial_temperature=1000,
                       min_temperature=0.01,
                       max_iterations=5000,
                       stage_iterations=1000,
                       multi_swap_probability=0.3):
    
    current_temperature = initial_temperature
    current_cost = cube.calculate_actual_cost()
    best_cost = current_cost
    best_configuration = cube.cube.copy()

    steps = []
    temperatures = []
    consecutive_non_improvements = 0
    stuck_in_local_optima = 0  # Counter for tracking stuck points

    def get_problem_specific_neighbor():
        pos1 = tuple(random.randint(0, cube.size - 1) for _ in range(3))
        pos2 = tuple(random.randint(0, cube.size - 1) for _ in range(3))
        while pos1 == pos2:
            pos2 = tuple(random.randint(0, cube.size - 1) for _ in range(3))
        return pos1, pos2

    def perform_multi_swap():
        new_cube = cube.cube.copy()
        num_swaps = random.randint(2, 4)
        positions = [tuple(random.randint(0, cube.size - 1) for _ in range(3)) for _ in range(num_swaps)]
        for i in range(len(positions) - 1):
            new_cube[positions[i]], new_cube[positions[i + 1]] = new_cube[positions[i + 1]], new_cube[positions[i]]
        return new_cube

    def calculate_acceptance_probability(cost_difference, temperature):
        if cost_difference <= 0:
            return 1.0
        normalized_delta = cost_difference / max(abs(current_cost), 1)
        normalized_delta = min(normalized_delta, 5.0)
        return math.exp(-normalized_delta / (temperature / initial_temperature))

    def adaptive_temperature_schedule(iteration):
        if consecutive_non_improvements > 5000:
            return initial_temperature * 0.5
        stage = iteration // stage_iterations
        cooling_rate = 0.999 if stage < max_iterations // stage_iterations // 3 else 0.997 if stage < max_iterations // stage_iterations * 2 // 3 else 0.995
        return current_temperature * cooling_rate

    with tqdm(total=max_iterations) as pbar:
        for iteration in range(max_iterations):
            if current_temperature < min_temperature or current_cost == 0:
                break

            pos1, pos2 = get_problem_specific_neighbor()
            if random.random() < multi_swap_probability:
                new_cube = perform_multi_swap()
            else:
                cube.cube[pos1], cube.cube[pos2] = cube.cube[pos2], cube.cube[pos1]

            new_cost = cube.calculate_actual_cost()
            cost_difference = new_cost - current_cost
            
            acceptance_prob = calculate_acceptance_probability(cost_difference, current_temperature)

            if random.random() < acceptance_prob:
                current_cost = new_cost
                steps.append({
                    'index1': pos1, 
                    'index2': pos2, 
                    'cost': current_cost,
                    'exp_value': acceptance_prob
                })
                if cost_difference < 0:
                    consecutive_non_improvements = 0
                    if new_cost < best_cost:
                        best_cost = new_cost
                        best_configuration = cube.cube.copy()
                else:
                    consecutive_non_improvements += 1
            else:
                cube.cube[pos1], cube.cube[pos2] = cube.cube[pos2], cube.cube[pos1]
                steps.append({
                    'index1': pos1, 
                    'index2': pos2, 
                    'cost': current_cost,
                    'exp_value': acceptance_prob
                })
                consecutive_non_improvements += 1
            
            # Check for being stuck in local optima
            if consecutive_non_improvements > 1000:
                stuck_in_local_optima += 1
                consecutive_non_improvements = 0  # Reset counter after counting as stuck

            current_temperature = adaptive_temperature_schedule(iteration)
            temperatures.append(current_temperature)
            pbar.update(1)
            pbar.set_postfix({'Cost': current_cost, 'Temp': f'{current_temperature:.2f}', 'Best': best_cost})

    cube.cube = best_configuration
    return best_cost, best_configuration, iteration, temperatures, steps, stuck_in_local_optima