import numpy as np
import random
import math
import matplotlib.pyplot as plt
from tqdm import tqdm

def simulated_annealing(cube,
                               initial_temperature=1000,  # Much higher initial temperature
                               min_temperature=0.01,      # Much lower minimum temperature
                               max_iterations=5000,     # Increased iterations
                               stage_iterations=1000,
                               multi_swap_probability=0.3):
    """
    Highly optimized simulated annealing with multi-stage cooling and advanced neighborhood generation.
    
    Args:
        cube (MagicCube): Instance of the MagicCube class
        initial_temperature (float): Starting temperature (higher for more exploration)
        min_temperature (float): Minimum temperature (lower for better convergence)
        max_iterations (int): Maximum number of iterations
        stage_iterations (int): Iterations per temperature stage
        multi_swap_probability (float): Probability of performing multiple swaps
    """
    current_temperature = initial_temperature
    current_cost = cube.calculate_actual_cost()
    best_cost = current_cost
    best_configuration = cube.cube.copy()
    
    # Enhanced statistics tracking
    cost_history = []
    stage_improvements = []
    consecutive_non_improvements = 0
    
    def get_problem_specific_neighbor():
        """Intelligent neighbor generation using problem-specific knowledge"""
        # Calculate row, column, and diagonal sums
        row_sums = np.array([[cube.cube[i, j, :].sum() for j in range(cube.size)] 
                            for i in range(cube.size)])
        col_sums = np.array([[cube.cube[i, :, k].sum() for k in range(cube.size)] 
                            for i in range(cube.size)])
        
        # Find positions contributing to high-cost lines
        high_cost_positions = []
        for i in range(cube.size):
            for j in range(cube.size):
                for k in range(cube.size):
                    row_deviation = abs(row_sums[i, j] - cube.magic_number)
                    col_deviation = abs(col_sums[i, k] - cube.magic_number)
                    if row_deviation > cube.magic_number * 0.05 or col_deviation > cube.magic_number * 0.05:
                        high_cost_positions.append((i, j, k))
        
        if high_cost_positions and random.random() < 0.8:  # 80% chance of intelligent move
            pos1 = random.choice(high_cost_positions)
            # Find a complementary position that might balance the sum
            target_sum = cube.magic_number
            current_sum = row_sums[pos1[0], pos1[1]]
            desired_value = target_sum - (current_sum - cube.cube[pos1])
            
            # Find positions with values close to desired_value
            potential_positions = []
            for i in range(cube.size):
                for j in range(cube.size):
                    for k in range(cube.size):
                        if (i,j,k) != pos1 and abs(cube.cube[i,j,k] - desired_value) < cube.magic_number * 0.1:
                            potential_positions.append((i,j,k))
            
            pos2 = random.choice(potential_positions) if potential_positions else \
                   tuple(random.randint(0, cube.size - 1) for _ in range(3))
        else:
            # Random move as fallback
            pos1 = tuple(random.randint(0, cube.size - 1) for _ in range(3))
            pos2 = tuple(random.randint(0, cube.size - 1) for _ in range(3))
            while pos1 == pos2:
                pos2 = tuple(random.randint(0, cube.size - 1) for _ in range(3))
        
        return pos1, pos2
    
    def perform_multi_swap():
        """Perform multiple coordinated swaps to improve solution quality"""
        new_cube = cube.cube.copy()
        num_swaps = random.randint(2, 4)  # Perform 2-4 coordinated swaps
        
        # Find related positions (same row/column/diagonal)
        positions = []
        for _ in range(num_swaps):
            if positions:
                # Choose related position to previous swap
                last_pos = positions[-1]
                related_positions = []
                for i in range(cube.size):
                    for j in range(cube.size):
                        for k in range(cube.size):
                            if (i == last_pos[0] or j == last_pos[1] or k == last_pos[2]) and \
                               (i,j,k) not in positions:
                                related_positions.append((i,j,k))
                pos = random.choice(related_positions) if related_positions else \
                      tuple(random.randint(0, cube.size - 1) for _ in range(3))
            else:
                pos = tuple(random.randint(0, cube.size - 1) for _ in range(3))
            positions.append(pos)
        
        # Perform cyclic swaps
        for i in range(len(positions)-1):
            new_cube[positions[i]], new_cube[positions[i+1]] = \
                new_cube[positions[i+1]], new_cube[positions[i]]
        
        return new_cube
    
    def adaptive_temperature_schedule(iteration, current_cost):
        """Multi-stage adaptive temperature scheduling"""
        if consecutive_non_improvements > 5000:  # If stuck
            return initial_temperature * 0.5  # Reheat
        
        # Calculate stage and progress within stage
        stage = iteration // stage_iterations
        stage_progress = (iteration % stage_iterations) / stage_iterations
        
        # Different cooling rates for different stages
        if stage < max_iterations // stage_iterations // 3:  # Early stages
            cooling_rate = 0.999
        elif stage < max_iterations // stage_iterations * 2 // 3:  # Middle stages
            cooling_rate = 0.997
        else:  # Late stages
            cooling_rate = 0.995
        
        # Adjust based on cost improvement
        if stage_improvements and stage_improvements[-1] > 0:
            cooling_rate = max(cooling_rate * 1.001, 0.9999)  # Slow down cooling
        
        return current_temperature * cooling_rate
    
    # Main optimization loop
    with tqdm(total=max_iterations) as pbar:
        for iteration in range(max_iterations):
            if current_temperature < min_temperature or current_cost == 0:
                break
            
            initial_stage_cost = current_cost
            
            # Decide between single swap and multi-swap
            if random.random() < multi_swap_probability:
                new_cube = perform_multi_swap()
                cube.cube = new_cube
            else:
                pos1, pos2 = get_problem_specific_neighbor()
                cube.cube[pos1], cube.cube[pos2] = cube.cube[pos2], cube.cube[pos1]
            
            new_cost = cube.calculate_actual_cost()
            cost_difference = new_cost - current_cost
            
            # Enhanced acceptance criteria
            if cost_difference < 0:  # Better solution
                current_cost = new_cost
                consecutive_non_improvements = 0
                if new_cost < best_cost:
                    best_cost = new_cost
                    best_configuration = cube.cube.copy()
            else:
                # Adaptive acceptance probability
                acceptance_probability = math.exp(-cost_difference / current_temperature)
                if random.random() < acceptance_probability:
                    current_cost = new_cost
                    consecutive_non_improvements += 1
                else:
                    if not multi_swap_probability:
                        cube.cube[pos1], cube.cube[pos2] = cube.cube[pos2], cube.cube[pos1]
                    else:
                        cube.cube = best_configuration.copy()
                    consecutive_non_improvements += 1
            
            # Update temperature using adaptive schedule
            if iteration % 100 == 0:  # Update temperature periodically
                current_temperature = adaptive_temperature_schedule(iteration, current_cost)
                stage_improvements.append(initial_stage_cost - current_cost)
            
            cost_history.append(current_cost)
            pbar.update(1)
            pbar.set_postfix({'Cost': current_cost, 
                            'Temp': f'{current_temperature:.2f}',
                            'Best': best_cost})
    
    # Restore best configuration
    cube.cube = best_configuration
    
    # Plot results
    plt.figure(figsize=(12, 6))
    plt.plot(cost_history)
    plt.title('Cost History during Enhanced Simulated Annealing')
    plt.xlabel('Iteration')
    plt.ylabel('Cost')
    plt.yscale('log')
    plt.grid(True)
    plt.show()
    
    return best_cost == 0, best_configuration, iteration, current_temperature, cost_history
