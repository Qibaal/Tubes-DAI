import numpy as np
import time
from algorithms.steepestascenthc import steepest_ascent_hill_climbing
from algorithms.sidewaysmovehc import hill_climbing_with_sideways_move
from algorithms.randomrestarthc import random_restart_hill_climbing
from algorithms.stochastichc import stochastic_hill_climbing  # Import the stochastic hill-climbing function
from algorithms.simulatedannealing import simulated_annealing  # Import the simulated annealing function
from algorithms.genetic import genetic_algorithm  # Import the genetic algorithm function

class SearchResults:
    def __init__(self):
        self.initial_cost = []
        self.final_cost = []
        self.iterations = []
        self.duration = []
        self.obj_values = []
        self.stuck_count = 0
        
    def add_run(self, initial_cost, final_cost, iterations, duration, obj_values):
        self.initial_cost.append(initial_cost)
        self.final_cost.append(final_cost)
        self.iterations.append(iterations)
        self.duration.append(duration)
        self.obj_values.append(obj_values)

class MagicCubeSearch:
    def __init__(self, size=5):
        self.cube = MagicCube(size=size)
        # Initialize results for each algorithm
        self.sac = SearchResults()  # Steepest Ascent
        self.sm = SearchResults()   # Sideways Move
        self.rr = SearchResults()   # Random Restart
        self.s = SearchResults()    # Stochastic
        self.sa = SearchResults()   # Simulated Annealing
        self.g = SearchResults()    # Genetic
        
        self.run_all_searches()

    def run_all_searches(self):
        for i in range(3):
            # Steepest Ascent
            print(f"SAC - Run {i+1}")
            self.run_steepest_ascent(i)
            
            # Sideways Move
            print(f"SM - Run {i+1}")
            self.run_sideways_move(i)
            
            # Random Restart
            print(f"RR - Run {i+1}")
            self.run_random_restart(i)
            
            # Stochastic
            print(f"S - Run {i+1}")
            self.run_stochastic(i)
            
            # Simulated Annealing
            print(f"SA - Run {i+1}")
            self.run_simulated_annealing(i)
            
            # Genetic
            print(f"G - Run {i+1}")
            self.run_genetic(i)

    def run_steepest_ascent(self, run_index):
        start_time = time.time()
        initial_cost = self.cube.calculate_cost()
        final_cost, final_cube, iterations, obj_values = steepest_ascent_hill_climbing(self.cube)
        duration = time.time() - start_time
        
        self.sac.add_run(initial_cost, final_cost, iterations, duration, obj_values)

    def run_sideways_move(self, run_index):
        start_time = time.time()
        initial_cost = self.cube.calculate_cost()
        final_cost, final_cube, iterations, obj_values = hill_climbing_with_sideways_move(
            self.cube, max_sideways_moves=10, max_iterations=1000
        )
        duration = time.time() - start_time
        
        self.sm.add_run(initial_cost, final_cost, iterations, duration, obj_values)

    def run_random_restart(self, run_index):
        start_time = time.time()
        initial_cost = self.cube.calculate_cost()
        final_cost, final_cube, iterations, restarts, obj_values = random_restart_hill_climbing(
            self.cube, max_restarts=3
        )
        duration = time.time() - start_time
        
        self.rr.add_run(initial_cost, final_cost, iterations, duration, obj_values)
        
    def run_stochastic(self, run_index):
        start_time = time.time()
        initial_cost = self.cube.calculate_cost()
        final_cost, final_cube, iterations, obj_values = stochastic_hill_climbing(self.cube)
        duration = time.time() - start_time
        
        self.s.add_run(initial_cost, final_cost, iterations, duration, obj_values)

    def run_simulated_annealing(self, run_index):
        start_time = time.time()
        initial_cost = self.cube.calculate_cost()
        final_cost, final_cube, iterations, temperatures, obj_values = simulated_annealing(self.cube)
        duration = time.time() - start_time
        
        self.sa.add_run(initial_cost, final_cost, iterations, duration, obj_values)

    def run_genetic(self, run_index):
        start_time = time.time()
        initial_cost = self.cube.calculate_cost()
        final_cost, final_cube, generations, obj_values = genetic_algorithm(
            self.cube, population_size=100, generations=2000, mutation_rate=0.1, elitism=True
        )
        duration = time.time() - start_time
        
        self.g.add_run(initial_cost, final_cost, generations, duration, obj_values)


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

# Test the implementation with sample cube data
cube_data = [
    # First layer
    [ [78, 109, 15, 41, 72], [45, 71, 77, 108, 14], [107, 13, 44, 75, 76], [74, 80, 106, 12, 43], [11, 42, 73, 79, 110] ],
    # Second layer
    [ [40, 66, 97, 103, 9], [102, 8, 39, 70, 96], [69, 100, 101, 7, 38], [6, 37, 68, 99, 105], [98, 104, 10, 36, 67] ],
    # Third layer
    [ [122, 3, 34, 65, 91], [64, 95, 121, 2, 33], [1, 32, 63, 94, 125], [93, 124, 5, 31, 62], [35, 61, 92, 123, 4] ],
    # Fourth layer
    [ [59, 90, 116, 22, 28], [21, 27, 58, 89, 120], [88, 119, 25, 26, 57], [30, 56, 87, 118, 24], [117, 23, 29, 60, 86] ],
    # Fifth layer
    [ [16, 47, 53, 84, 115], [83, 114, 20, 46, 52], [50, 51, 82, 113, 19], [112, 18, 49, 55, 81], [54, 85, 111, 17, 48] ]
]

# Initialize the magic cube with the provided cube data
magic_cube = MagicCube()
initial_cost = magic_cube.calculate_cost()

# Display the cost of the current cube configuration
magic_cube.display_cost()

# com = input("Masukkan algo: ")

# if com == "sac":
#     # Record the start time
#     start_time = time.time()

#     # Call the steepest_ascent_hill_climbing function
#     final_cost, final_cube = steepest_ascent_hill_climbing(magic_cube)

#     # Record the end time
#     end_time = time.time()

#     # Calculate the elapsed time
#     elapsed_time = end_time - start_time

#     # Print the elapsed time
#     print(f"Execution time: {elapsed_time} seconds")
#     data = {
#         "initial_cost": initial_cost,
#         "final_cost": final_cost,
#         "initial_cube": magic_cube.cube,
#         "final_cube": final_cube,
#         "time": elapsed_time
#     }
#     print(data)
# elif com == "sm":
#     max_sideways_moves=1000
#     hill_climbing_with_sideways_move(magic_cube, max_sideways_moves, max_iterations=1000)
# elif com == "rr":
#     max_restarts=10
#     random_restart_hill_climbing(magic_cube, max_restarts)
# elif com ==  "s":
#     stochastic_hill_climbing(magic_cube) 
# elif com == "sa":
#     simulated_annealing(magic_cube)
# elif com == "g":
#     # Kontrol jumlah populasi
#     for pop_size in [50, 100, 150]:  # Variasi jumlah populasi
#         print(f"Kontrol Jumlah Populasi: Populasi = {pop_size}\n")
#         for i in range(3):  
#             print(f"Iterasi ke-{i+1} dengan Populasi {pop_size}")
#             genetic_algorithm(magic_cube, population_size=pop_size, generations=2000, mutation_rate=0.1, elitism=True)

#     # Kontrol banyak iterasi
#     for gen_count in [1000, 2000, 3000]:  # Variasi banyak iterasi
#         print(f"Kontrol Banyak Iterasi: Iterasi = {gen_count}\n")
#         for i in range(3): 
#             print(f"Iterasi ke-{i+1} dengan Generasi {gen_count}")
#             genetic_algorithm(magic_cube, population_size=100, generations=gen_count, mutation_rate=0.1, elitism=True)

# Replace all the input/if-else code with:
search = MagicCubeSearch()