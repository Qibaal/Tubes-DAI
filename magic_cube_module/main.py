import json
import time
import numpy as np
import matplotlib.pyplot as plt

from algorithms.steepestascenthc import steepest_ascent_hill_climbing
from algorithms.sidewaysmovehc import hill_climbing_with_sideways_move
from algorithms.randomrestarthc import random_restart_hill_climbing
from algorithms.stochastichc import stochastic_hill_climbing  
from algorithms.simulatedannealing import simulated_annealing  
from algorithms.genetic import genetic_algorithm  

class SearchResults:
    def __init__(self):
        self.initial_cost = []
        self.initial_cube = []
        self.final_cost = []
        self.final_cube = []
        self.steps = []
        self.duration = []
        self.stuck_count = 0
        self.iterations_per_restart = []  
        
    def add_run(self, initial_cost, initial_cube, final_cost, final_cube, iterations, duration, steps, iterations_per_restart=None):  # Add parameter
        self.initial_cost.append(float(initial_cost))  # Convert numpy float to Python float
        self.initial_cube.append(list(initial_cube.flatten()))  # Convert numpy array to list
        self.final_cost.append(float(final_cost))  # Convert numpy float to Python float
        self.final_cube.append(list(final_cube.flatten()))  # Convert numpy array to list
        self.steps.append(steps)
        self.duration.append(float(duration))  # Convert numpy float to Python float
        if iterations_per_restart is not None:  # Add this
            self.iterations_per_restart.append(iterations_per_restart)

class MagicCubeSearch:
    def __init__(self, size=5):
        # Generate a single initial cube and store it
        self.initial_cube_state = MagicCube(size=size).cube

        # Initialize results for each algorithm
        self.sac = SearchResults()  # Steepest Ascent
        self.sm = SearchResults()   # Sideways Move
        self.rr = SearchResults()   # Random Restart
        self.s = SearchResults()    # Stochastic
        self.sa = SearchResults()   # Simulated Annealing
        self.g = SearchResults()    # Genetic
        
        self.run_all_searches()
        self.plot_genetic_results = self._plot_genetic_results  # Assign method

    def run_all_searches(self):
        num_runs = 1
        algorithms = [
            # ("SAC", self.run_steepest_ascent),
            # ("SM", self.run_sideways_move),
            # ("RR", self.run_random_restart),
            # ("S", self.run_stochastic),
            # ("SA", self.run_simulated_annealing),
            ("G", self.run_genetic)
        ]

        for alg_name, alg_func in algorithms:
            for run in range(num_runs):
                print(f"{alg_name} - Run {run+1}")
                alg_func()

    def run_steepest_ascent(self):
        self.cube = MagicCube(cube_data=self.initial_cube_state)
        start_time = time.time()
        initial_cost = self.cube.calculate_cost()
        initial_cube = np.copy(self.cube.cube)
        final_cost, final_cube, iterations, steps = steepest_ascent_hill_climbing(self.cube)
        duration = time.time() - start_time
        self.sac.add_run(initial_cost, initial_cube, final_cost, final_cube, iterations, duration, steps)

    def run_sideways_move(self):
        self.cube = MagicCube(cube_data=self.initial_cube_state)
        start_time = time.time()
        initial_cost = self.cube.calculate_cost()
        initial_cube = np.copy(self.cube.cube)
        final_cost, final_cube, iterations, steps = hill_climbing_with_sideways_move(self.cube, max_sideways_moves=10, max_iterations=100)
        duration = time.time() - start_time
        self.sm.add_run(initial_cost, initial_cube, final_cost, final_cube, iterations, duration, steps)

    def run_random_restart(self):
        self.cube = MagicCube(cube_data=self.initial_cube_state)
        start_time = time.time()
        initial_cost = self.cube.calculate_cost()
        initial_cube = np.copy(self.cube.cube)
        final_cost, final_cube, iterations, steps, iterations_per_restart = random_restart_hill_climbing(self.cube, max_restarts=3)
        duration = time.time() - start_time
        self.rr.add_run(initial_cost, initial_cube, final_cost, final_cube, iterations, duration, steps, iterations_per_restart)

    def run_stochastic(self):
        self.cube = MagicCube(cube_data=self.initial_cube_state)
        start_time = time.time()
        initial_cost = self.cube.calculate_cost()
        initial_cube = np.copy(self.cube.cube)
        final_cost, final_cube, iterations, steps = stochastic_hill_climbing(self.cube)
        duration = time.time() - start_time
        self.s.add_run(initial_cost, initial_cube, final_cost, final_cube, iterations, duration, steps)

    def run_simulated_annealing(self):
        self.cube = MagicCube(cube_data=self.initial_cube_state)
        start_time = time.time()
        initial_cost = self.cube.calculate_cost()
        initial_cube = np.copy(self.cube.cube)
        final_cost, final_cube, iterations, temperatures, steps, stuck_in_local_optima = simulated_annealing(self.cube)
        duration = time.time() - start_time
        self.sa.add_run(initial_cost, initial_cube, final_cost, final_cube, iterations, duration, steps)
        self.sa.stuck_count = stuck_in_local_optima  # Store the specific counter

    def run_genetic(self):
        # Control parameters for experiments
        population_sizes = [5, 7, 10]
        iteration_counts = [3000, 30000, 300000]
        all_results = []

        # Run experiments with population size as the control variable
        for iterations in iteration_counts:
            for population_size in population_sizes:
                for run in range(3):  # Run each configuration 3 times
                    print(f"Running Genetic Algorithm with Population {population_size}, Iterations {iterations} - Run {run+1}")
                    
                    # Initialize the genetic algorithm without passing 'cube' as an argument
                    result = genetic_algorithm(
                        population_size=population_size,
                        max_iterations=iterations,
                        mutation_rate=0.1,
                        elitism=True
                    )
                    
                    result["experiment_id"] = f"pop_{population_size}_iter_{iterations}_run_{run+1}"
                    all_results.append(result)
                    self._plot_genetic_results(result, f"pop_{population_size}_iter_{iterations}_run_{run+1}")

        # Run experiments with iterations as the control variable
        for population_size in population_sizes:
            for iterations in iteration_counts:
                for run in range(3):  # Run each configuration 3 times
                    print(f"Running Genetic Algorithm with Population {population_size}, Iterations {iterations} - Run {run+1}")
                    
                    result = genetic_algorithm(
                        population_size=population_size,
                        max_iterations=iterations,
                        mutation_rate=0.1,
                        elitism=True
                    )
                    
                    result["experiment_id"] = f"pop_{population_size}_iter_{iterations}_run_{run+1}"
                    all_results.append(result)
                    self._plot_genetic_results(result, result["experiment_id"])

    def _plot_genetic_results(self, results, experiment_id):
        """
        Plot results for the Genetic Algorithm, showing the max and average objective values per generation.
        """
        # Extract max and average objective values for each iteration
        max_obj_values, avg_obj_values = zip(*results["objective_per_iteration"])

        # Plotting max and average objective values
        plt.figure(figsize=(12, 6))
        plt.plot(max_obj_values, label='Max Objective Value')
        plt.plot(avg_obj_values, label='Average Objective Value')
        plt.title(f'Objective Value vs Generations - {experiment_id}')
        plt.xlabel('Generations')
        plt.ylabel('Objective Value')
        plt.legend()
        plt.grid(True)

        # Save or show the plot as needed
        plt.savefig(f'{experiment_id}_objective_vs_generations.png')
        plt.show()

class MagicCube:
    def __init__(self, cube_data=None, size=5):
        self.size = size
        if cube_data is not None:
            self.cube = np.array(cube_data).reshape((size, size, size))
        else:
            numbers = list(range(1, size**3 + 1))
            np.random.shuffle(numbers)
            self.cube = np.array(numbers).reshape((size, size, size))
        
        self.magic_number = self.calculate_magic_number()
        
        # Define weights for different types of sums
        self.weights = {
            'rows': 1.0,          # Basic weight for rows
            'columns': 1.0,       # Basic weight for columns
            'pillars': 1.2,       # Slightly higher weight for pillars (vertical lines)
            'level_diagonals': 1.5,  # Higher weight for diagonals within each level
            'space_diagonals': 2.0,  # Highest weight for space diagonals
            'deviation_penalty': 0.1  # Additional penalty for large deviations
        }

    def calculate_magic_number(self):
        """
        Calculate the magic number for a magic cube.
        Formula: size * (size^3 + 1) // 2
        """
        return (self.size * (self.size**3 + 1)) // 2

    def calculate_cost(self):
        """
        Enhanced objective function that calculates the weighted total cost based on the deviations 
        from the magic number. Different weights are applied to different types of sums, and additional
        penalties are added for large deviations.
        """
        cost = 0
        
        # Cost for rows
        row_costs = []
        for level in range(self.size):
            for row in range(self.size):
                row_sum = self.cube[level, row, :].sum()
                deviation = abs(row_sum - self.magic_number)
                row_costs.append(deviation)
                cost += self.weights['rows'] * deviation
                # Add extra penalty for large deviations
                if deviation > self.magic_number * 0.2:  # If deviation is more than 20% of magic number
                    cost += self.weights['deviation_penalty'] * deviation
        
        # Cost for columns
        column_costs = []
        for level in range(self.size):
            for col in range(self.size):
                col_sum = self.cube[level, :, col].sum()
                deviation = abs(col_sum - self.magic_number)
                column_costs.append(deviation)
                cost += self.weights['columns'] * deviation
                if deviation > self.magic_number * 0.2:
                    cost += self.weights['deviation_penalty'] * deviation
        
        # Cost for pillars (z-axis)
        pillar_costs = []
        for row in range(self.size):
            for col in range(self.size):
                pillar_sum = self.cube[:, row, col].sum()
                deviation = abs(pillar_sum - self.magic_number)
                pillar_costs.append(deviation)
                cost += self.weights['pillars'] * deviation
                if deviation > self.magic_number * 0.2:
                    cost += self.weights['deviation_penalty'] * deviation
        
        # Cost for main diagonals on each level
        level_diagonal_costs = []
        for level in range(self.size):
            # Left-to-right diagonal
            diag1_sum = np.trace(self.cube[level])
            deviation1 = abs(diag1_sum - self.magic_number)
            level_diagonal_costs.append(deviation1)
            cost += self.weights['level_diagonals'] * deviation1
            
            # Right-to-left diagonal
            diag2_sum = np.trace(np.fliplr(self.cube[level]))
            deviation2 = abs(diag2_sum - self.magic_number)
            level_diagonal_costs.append(deviation2)
            cost += self.weights['level_diagonals'] * deviation2
            
            # Extra penalty for diagonal deviations
            if deviation1 > self.magic_number * 0.15:  # Lower threshold for diagonals
                cost += self.weights['deviation_penalty'] * deviation1 * 1.5
            if deviation2 > self.magic_number * 0.15:
                cost += self.weights['deviation_penalty'] * deviation2 * 1.5
        
        # Cost for space diagonals (through all levels)
        space_diagonal_costs = []
        # Top-left to bottom-right
        diag1 = sum(self.cube[i, i, i] for i in range(self.size))
        deviation1 = abs(diag1 - self.magic_number)
        space_diagonal_costs.append(deviation1)
        cost += self.weights['space_diagonals'] * deviation1
        
        # Top-right to bottom-left
        diag2 = sum(self.cube[i, i, self.size - i - 1] for i in range(self.size))
        deviation2 = abs(diag2 - self.magic_number)
        space_diagonal_costs.append(deviation2)
        cost += self.weights['space_diagonals'] * deviation2
        
        # Bottom-left to top-right
        diag3 = sum(self.cube[i, self.size - i - 1, i] for i in range(self.size))
        deviation3 = abs(diag3 - self.magic_number)
        space_diagonal_costs.append(deviation3)
        cost += self.weights['space_diagonals'] * deviation3
        
        # Bottom-right to top-left
        diag4 = sum(self.cube[i, self.size - i - 1, self.size - i - 1] for i in range(self.size))
        deviation4 = abs(diag4 - self.magic_number)
        space_diagonal_costs.append(deviation4)
        cost += self.weights['space_diagonals'] * deviation4
        
        # Extra penalty for space diagonal deviations
        for deviation in space_diagonal_costs:
            if deviation > self.magic_number * 0.1:  # Even lower threshold for space diagonals
                cost += self.weights['deviation_penalty'] * deviation * 2
        
        # Add a balance penalty if the distribution of costs is very uneven
        cost_std = np.std(row_costs + column_costs + pillar_costs + 
                         level_diagonal_costs + space_diagonal_costs)
        cost += cost_std * 0.5  # Penalty for high variance in costs
        
        return cost

    def calculate_actual_cost(self):
        """
        Calculates the actual number of constraint violations (unweighted).
        This is useful for tracking actual progress.
        """
        cost = 0
        
        # Cost for rows
        for level in range(self.size):
            for row in range(self.size):
                row_sum = self.cube[level, row, :].sum()
                cost += row_sum != self.magic_number
        
        # Cost for columns
        for level in range(self.size):
            for col in range(self.size):
                col_sum = self.cube[level, :, col].sum()
                cost += col_sum != self.magic_number
        
        # Cost for pillars
        for row in range(self.size):
            for col in range(self.size):
                pillar_sum = self.cube[:, row, col].sum()
                cost += pillar_sum != self.magic_number
        
        # Cost for level diagonals
        for level in range(self.size):
            diag1_sum = np.trace(self.cube[level])
            diag2_sum = np.trace(np.fliplr(self.cube[level]))
            cost += diag1_sum != self.magic_number
            cost += diag2_sum != self.magic_number
        
        # Cost for space diagonals
        diag1 = sum(self.cube[i, i, i] for i in range(self.size))
        diag2 = sum(self.cube[i, i, self.size - i - 1] for i in range(self.size))
        diag3 = sum(self.cube[i, self.size - i - 1, i] for i in range(self.size))
        diag4 = sum(self.cube[i, self.size - i - 1, self.size - i - 1] for i in range(self.size))
        cost += diag1 != self.magic_number
        cost += diag2 != self.magic_number
        cost += diag3 != self.magic_number
        cost += diag4 != self.magic_number

        return cost

    def display(self):
        """
        Displays the current cube configuration.
        """
        print("Cube:")
        print(self.cube)

    def display_cost(self):
        """
        Displays both the weighted cost and actual constraint violations.
        """
        weighted_cost = self.calculate_cost()
        actual_violations = self.calculate_actual_cost()
        print(f"Weighted Cost: {weighted_cost}")
        print(f"Actual Constraint Violations: {actual_violations}")

magic_cube = MagicCube()
initial_cost = magic_cube.calculate_cost()

magic_cube.display_cost()
search = MagicCubeSearch()

def plot_obj_values(search_results, algorithm_name):
    plt.figure(figsize=(12, 6))
    for i, steps in enumerate(search_results.steps):
        # Ensure each run has 'cost' values for each step
        if steps:  # Check if the steps list is not empty
            costs = [step['cost'] for step in steps]
            plt.plot(range(len(costs)), costs, label=f'Run {i+1}')
    
    plt.title(f'Objective Value vs Iterations - {algorithm_name}')
    plt.xlabel('Iterations')
    plt.ylabel('Objective Value')
    plt.legend()
    plt.grid(True)
    plt.savefig(f'{algorithm_name}_objective_vs_iterations.png')
    plt.show()

# Plot "e^(4E/T) (y) banyak iterasi (x)" for Simulated Annealing
def plot_sa_exp_values(search_results):
    plt.figure(figsize=(12, 6))
    for i, steps in enumerate(search_results.steps):
        # Extract e^(dE/T) values from steps
        exp_values = [step['exp_value'] for step in steps]
        plt.plot(range(len(exp_values)), exp_values, label=f'Run {i+1}')
    
    plt.title('e^(dE/T) vs Iterations - Simulated Annealing')
    plt.xlabel('Iterations')
    plt.ylabel('e8')
    plt.yscale('log')  # Use log scale for better visualization
    plt.legend()
    plt.grid(True)
    plt.savefig('SA_exp_vs_iterations.png')
    plt.show()
    
# Call plotting functions
plot_obj_values(search.sac, 'Steepest Ascent')
plot_obj_values(search.sm, 'Sideways Move')
plot_obj_values(search.rr, 'Random Restart')
plot_obj_values(search.s, 'Stochastic')
plot_obj_values(search.sa, 'Simulated Annealing')
plot_sa_exp_values(search.sa)

# Steepest Ascent
steepest_ascent = {
    "name": "steepest_ascent",
    "final_cost": search.sac.final_cost,
    "time": search.sac.duration,
    "final_cube": search.sac.final_cube,
    "steps": search.sac.steps
}

# Sideways Move
sideways_move = {
    "name": "stochastic",
    "final_cost": search.sm.final_cost,
    "time": search.sm.duration,
    "final_cube": search.sm.final_cube,
    "steps": search.sm.steps
}

# Random Restart
random_restart = {
    "name": "random_restart",
    "final_cost": search.rr.final_cost,
    "time": search.rr.duration,
    "final_cube": search.rr.final_cube,
    "steps": search.rr.steps,
    "iterations_per_restart": search.rr.iterations_per_restart
}

# Stochastic
stochastic = {
    "name": "stochastic",
    "final_cost": search.s.final_cost,
    "time": search.s.duration,
    "final_cube": search.s.final_cube,
    "steps": search.s.steps
}

# Simulated Annealing
simulated_annealing = {
    "name": "simulated_annealing",
    "final_cost": search.sa.final_cost,
    "time": search.sa.duration,
    "final_cube": search.sa.final_cube,
    "steps": search.sa.steps,
    "stuck_frequency": search.sa.stuck_count
}

# Genetic
genetic = {
    "name": "genetic",
    "final_cost": search.g.final_cost,
    "time": search.g.duration,
    "final_cube": search.g.final_cube,
    "generations": search.g.iterations_per_restart
}

config = [
    steepest_ascent,
    sideways_move,
    random_restart,
    stochastic,
    simulated_annealing,
    genetic
]

def format_array(array):
    """
    Format array for desired output style with indentation, but without explicit \n characters.
    """
    # Grouping values in sets of 10 for readability
    formatted = "["
    formatted += ", ".join(str(value) for value in array[:10])  # First line without \n
    for i in range(10, len(array), 10):
        formatted += ", " + ", ".join(str(value) for value in array[i:i+10])
    formatted += "]"
    return formatted

initialConfig = {
    "initial_cost": float(search.sac.initial_cost[0]),
    "initial_cube": format_array(search.sac.initial_cube[0])
}

for entry in config:
    entry["final_cost"] = [float(cost) for cost in entry["final_cost"]]
    entry["time"] = [float(time) for time in entry["time"]]
    entry["final_cube"] = [format_array(cube) for cube in entry["final_cube"]]

    # Check that 'steps' exists and that each step entry has valid data
    if "steps" in entry:
        processed_steps = []
        for step_list in entry["steps"]:
            processed_step_list = []
            for step in step_list:
                # Ensure that step elements are properly formatted dictionaries with expected keys
                if isinstance(step, dict) and "index1" in step and "index2" in step and "cost" in step:
                    try:
                        processed_step = {
                            "index1": int(step["index1"]) if isinstance(step["index1"], (int, float, str)) else 0,
                            "index2": int(step["index2"]) if isinstance(step["index2"], (int, float, str)) else 0,
                            "cost": float(step["cost"]) if isinstance(step["cost"], (int, float, str)) else 0.0
                        }
                        processed_step_list.append(processed_step)
                    except ValueError:
                        print(f"Error converting step values in entry '{entry['name']}': {step}")
            processed_steps.append(processed_step_list)
        entry["steps"] = processed_steps

    if "iterations_per_restart" in entry:
        entry["iterations_per_restart"] = [
            [int(count) if isinstance(count, (int, float, str)) else 0 for count in iter_count]
            if isinstance(iter_count, list) else int(iter_count) if isinstance(iter_count, (int, float, str)) else 0
            for iter_count in entry["iterations_per_restart"]
        ]

# Write the processed data to a JavaScript file
with open("C:\\Users\\FAVIAN\\OneDrive - Institut Teknologi Bandung\\Favian\\S1\\5th Semester\\DAI\\Tugas\\Tubes-DAI\\magic-simulator\\app\\data\\configData.js", "w") as f:
    f.write("export const initialConfig = ")
    json.dump(initialConfig, f, indent=2)
    f.write(";\n\nexport const config = ")
    json.dump(config, f, indent=2)
    f.write(";")