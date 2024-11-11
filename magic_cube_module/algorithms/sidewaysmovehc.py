import numpy as np
import itertools
import matplotlib.pyplot as plt
from collections import defaultdict
import random

def hill_climbing_with_sideways_move(cube, max_sideways_moves, max_iterations, tabu_list_size=50):
    """
    Enhanced version of hill climbing with sideways moves that uses:
    - Tabu list to prevent cycling
    - Adaptive neighborhood selection
    - Line sum analysis for informed swaps
    - Temperature-like parameter for dynamic acceptance

    Returns:
    - final_cost: The final cost after the algorithm terminates.
    - final_cube: The state of the cube when the algorithm ends.
    - iteration: The number of iterations performed.
    - cost_progress: List of objective values over iterations.
    - sideways_moves: Total number of sideways moves made.
    """
    iteration = 0
    sideways_moves = 0
    current_cost = cube.calculate_cost()
    cost_progress = []
    steps = []  # Collect step data

    # Initialize tabu list to prevent revisiting recent states
    tabu_list = []

    # Track the effectiveness of different types of swaps
    swap_effectiveness = defaultdict(lambda: {'attempts': 0, 'improvements': 0})

    # Temperature-like parameter for accepting worse moves occasionally
    initial_temperature = 10.0

    while current_cost > 0 and iteration < max_iterations:
        print(f"Iteration {iteration}: {current_cost} cost, Sideways moves: {sideways_moves}")
        
        # Calculate current line sums
        line_sums = calculate_line_sums(cube)
        
        # Find problematic lines (those far from magic number)
        problem_areas = identify_problem_areas(line_sums)
        
        # Generate candidate swaps with preference for problematic areas
        candidate_swaps = generate_intelligent_swaps(problem_areas, cube.size, tabu_list)
        
        # Track if we found any improvement
        found_improvement = False
        temperature = initial_temperature * (1 - iteration / max_iterations)

        for swap_type, pos1, pos2 in candidate_swaps:
            if (pos1, pos2) in tabu_list:
                continue
                
            new_cube = cube.cube.copy()
            new_cube[pos1], new_cube[pos2] = new_cube[pos2], new_cube[pos1]
            
            cube.cube = new_cube
            new_cost = cube.calculate_cost()
            
            # Update swap effectiveness statistics
            swap_effectiveness[swap_type]['attempts'] += 1
            
            # Accept if better or with probability based on temperature
            if new_cost < current_cost:
                best_cube = new_cube.copy()
                current_cost = new_cost
                found_improvement = True
                swap_effectiveness[swap_type]['improvements'] += 1
                update_tabu_list(tabu_list, (pos1, pos2), tabu_list_size)

                # Add step tracking here
                step_info = {
                    "index1": pos1[0] * cube.size**2 + pos1[1] * cube.size + pos1[2],
                    "index2": pos2[0] * cube.size**2 + pos2[1] * cube.size + pos2[2],
                    "cost": current_cost
                }
                steps.append(step_info)
                print(f"Step {iteration + 1}: {step_info}")
                break

            elif new_cost == current_cost and sideways_moves < max_sideways_moves:
                acceptance_prob = np.exp(-0.1 / temperature)
                if random.random() < acceptance_prob:
                    best_cube = new_cube.copy()
                    current_cost = new_cost
                    sideways_moves += 1
                    update_tabu_list(tabu_list, (pos1, pos2), tabu_list_size)

                    # Add step tracking here
                    step_info = {
                        "index1": pos1[0] * cube.size**2 + pos1[1] * cube.size + pos1[2],
                        "index2": pos2[0] * cube.size**2 + pos2[1] * cube.size + pos2[2],
                        "cost": current_cost
                    }
                    steps.append(step_info)
                    print(f"Step {iteration + 1}: {step_info}")
                    break
            
            # Restore original cube for next attempt
            cube.cube = new_cube.copy()
        
        if not found_improvement and sideways_moves >= max_sideways_moves:
            print("No improvement found and sideways moves exhausted.")
            break
            
        cost_progress.append(current_cost)
        iteration += 1
        
        # Periodically adjust strategy based on effectiveness
        if iteration % 50 == 0:
            adjust_strategy(swap_effectiveness)
    
    # Return structured data matching the expected output
    return current_cost, cube.cube, iteration, steps

def calculate_line_sums(cube):
    """Calculate all line sums in the cube and their deviations from magic number."""
    line_sums = {
        'rows': [],
        'columns': [],
        'pillars': [],
        'diagonals': []
    }
    
    # Calculate row sums
    for i in range(cube.size):
        for j in range(cube.size):
            line_sums['rows'].append({
                'sum': cube.cube[i, j, :].sum(),
                'position': (i, j, ':'),
                'deviation': abs(cube.cube[i, j, :].sum() - cube.magic_number)
            })
            
            # Calculate column sums
            line_sums['columns'].append({
                'sum': cube.cube[i, :, j].sum(),
                'position': (i, ':', j),
                'deviation': abs(cube.cube[i, :, j].sum() - cube.magic_number)
            })
            
            # Calculate pillar sums
            line_sums['pillars'].append({
                'sum': cube.cube[:, i, j].sum(),
                'position': (':', i, j),
                'deviation': abs(cube.cube[:, i, j].sum() - cube.magic_number)
            })
    
    # Calculate diagonal sums
    # Main diagonal in each layer
    for i in range(cube.size):
        diag_sum = sum(cube.cube[i, j, j] for j in range(cube.size))
        line_sums['diagonals'].append({
            'sum': diag_sum,
            'position': (i, 'diag', 'main'),
            'deviation': abs(diag_sum - cube.magic_number)
        })
        
        # Anti-diagonal in each layer
        anti_diag_sum = sum(cube.cube[i, j, cube.size-1-j] for j in range(cube.size))
        line_sums['diagonals'].append({
            'sum': anti_diag_sum,
            'position': (i, 'diag', 'anti'),
            'deviation': abs(anti_diag_sum - cube.magic_number)
        })
    
    return line_sums

def identify_problem_areas(line_sums, top_n=5):
    """Identify areas of the cube that need the most improvement."""
    problems = []
    
    # Sort lines by deviation from magic number
    for line_type in line_sums:
        sorted_lines = sorted(line_sums[line_type], 
                            key=lambda x: x['deviation'], 
                            reverse=True)
        problems.extend([x['position'] for x in sorted_lines[:top_n]])
    
    return problems

def generate_intelligent_swaps(problem_areas, cube_size, tabu_list):
    """Generate candidate swaps with focus on problem areas."""
    candidates = []
    
    # Generate different types of swaps
    # 1. Within-line swaps for problematic lines
    for area in problem_areas:
        line_positions = get_line_positions(area, cube_size)
        for pos1, pos2 in itertools.combinations(line_positions, 2):
            if (pos1, pos2) not in tabu_list:
                candidates.append(('within_line', pos1, pos2))
    
    # 2. Cross-line swaps between problematic areas
    for area1, area2 in itertools.combinations(problem_areas, 2):
        pos1 = get_representative_position(area1, cube_size)
        pos2 = get_representative_position(area2, cube_size)
        if (pos1, pos2) not in tabu_list:
            candidates.append(('cross_line', pos1, pos2))
    
    # 3. Random swaps (for diversity)
    for _ in range(max(1, len(candidates) // 4)):
        pos1 = tuple(random.randrange(cube_size) for _ in range(3))
        pos2 = tuple(random.randrange(cube_size) for _ in range(3))
        if (pos1, pos2) not in tabu_list:
            candidates.append(('random', pos1, pos2))
    
    # Shuffle candidates to avoid getting stuck in patterns
    random.shuffle(candidates)
    return candidates

def get_line_positions(area, cube_size):
    """Get all positions in a given line."""
    positions = []
    if isinstance(area[0], str) and area[0] == ':':  # Pillar
        i, j = area[1], area[2]
        positions.extend((x, i, j) for x in range(cube_size))
    elif isinstance(area[1], str) and area[1] == ':':  # Column
        i, j = area[0], area[2]
        positions.extend((i, x, j) for x in range(cube_size))
    elif isinstance(area[2], str) and area[2] == ':':  # Row
        i, j = area[0], area[1]
        positions.extend((i, j, x) for x in range(cube_size))
    elif area[1] == 'diag':  # Diagonal
        i = area[0]
        if area[2] == 'main':
            positions.extend((i, x, x) for x in range(cube_size))
        else:  # anti-diagonal
            positions.extend((i, x, cube_size-1-x) for x in range(cube_size))
    return positions

def get_representative_position(area, cube_size):
    """Get a representative position from an area specification."""
    if isinstance(area[0], str) and area[0] == ':':  # Pillar
        return (random.randrange(cube_size), area[1], area[2])
    elif isinstance(area[1], str) and area[1] == ':':  # Column
        return (area[0], random.randrange(cube_size), area[2])
    elif isinstance(area[2], str) and area[2] == ':':  # Row
        return (area[0], area[1], random.randrange(cube_size))
    elif area[1] == 'diag':  # Diagonal
        x = random.randrange(cube_size)
        if area[2] == 'main':
            return (area[0], x, x)
        else:  # anti-diagonal
            return (area[0], x, cube_size-1-x)
    return area  # Default case

def update_tabu_list(tabu_list, swap, max_size):
    """Update the tabu list with the new swap."""
    tabu_list.append(swap)
    if len(tabu_list) > max_size:
        tabu_list.pop(0)

def adjust_strategy(swap_effectiveness):
    """Adjust strategy based on the effectiveness of different swap types."""
    for swap_type, stats in swap_effectiveness.items():
        if stats['attempts'] > 0:
            effectiveness = stats['improvements'] / stats['attempts']
            print(f"Swap type {swap_type} effectiveness: {effectiveness:.2%}")

def plot_results(cost_progress):
    """Plot the cost progression with additional statistics."""
    plt.figure(figsize=(12, 6))
    plt.plot(cost_progress, label='Cost')
    plt.title("Cost Progression during Improved Hill-Climbing")
    plt.xlabel("Iteration")
    plt.ylabel("Total Cost")
    plt.grid(True)
    
    # Add moving average
    window = min(50, len(cost_progress))
    if window > 0:
        moving_avg = np.convolve(cost_progress, 
                                np.ones(window)/window, 
                                mode='valid')
        plt.plot(range(window-1, len(cost_progress)), 
                moving_avg, 
                'r--', 
                label='Moving Average')
    
    plt.legend()
    plt.show()