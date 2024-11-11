import numpy as np
import time
import matplotlib.pyplot as plt

from algorithms.steepestascenthc import steepest_ascent_hill_climbing
from algorithms.sidewaysmovehc import hill_climbing_with_sideways_move
from algorithms.randomrestarthc import random_restart_hill_climbing
from algorithms.stochastichc import stochastic_hill_climbing  # Import the stochastic hill-climbing function
from algorithms.simulatedannealing import simulated_annealing  # Import the simulated annealing function
from algorithms.genetic import genetic_algorithm  # Import the genetic algorithm function

class SearchResults:
    def __init__(self):
        self.initial_cost = []
        self.initial_cube = []
        self.final_cost = []
        self.final_cube = []
        self.steps = []
        self.duration = []
        self.stuck_count = 0
        self.iterations_per_restart = []  # Add this new field
        
    def add_run(self, initial_cost, initial_cube, final_cost, final_cube, iterations, duration, steps, iterations_per_restart=None):  # Add parameter
        self.initial_cost.append(initial_cost)
        self.initial_cube.append(initial_cube.flatten().tolist())
        self.final_cost.append(final_cost)
        self.final_cube.append(final_cube.flatten().tolist())
        self.steps.append(steps)
        self.duration.append(duration)
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

    def run_all_searches(self):
        num_runs = 3
        algorithms = [
            ("SAC", self.run_steepest_ascent),
            ("SM", self.run_sideways_move),
            ("RR", self.run_random_restart),
            ("S", self.run_stochastic),
            ("SA", self.run_simulated_annealing),
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
        final_cost, final_cube, iterations, steps = hill_climbing_with_sideways_move(self.cube, max_sideways_moves=10, max_iterations=1000)
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
        self.cube = MagicCube(cube_data=self.initial_cube_state)
        start_time = time.time()
        initial_cost = self.cube.calculate_cost()
        final_cost, final_cube, generations = genetic_algorithm(
            self.cube, 100, 2000, 0.1, True
        )
        duration = time.time() - start_time
        self.g.add_run(initial_cost, final_cost, generations, duration)


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

# Plot "nilai obj (y) banyak iterasi (x)" for each algorithm (generalized for all except Genetic Algorithm)
def plot_obj_values(search_results, algorithm_name):
    plt.figure(figsize=(12, 6))
    for i, steps in enumerate(search_results.steps):
        # Ensure steps have a 'cost' field; adjust if necessary based on the data structure
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