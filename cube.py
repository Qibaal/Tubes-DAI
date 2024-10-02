import numpy as np
from algorithms.steepestascenthc import steepest_ascent_hill_climbing  # Import the steepest ascent hill-climbing function
from algorithms.sidewaysmovehc import hill_climbing_with_sideways_move
from algorithms.randomrestarthc import random_restart_hill_climbing
from algorithms.stochastichc import stochastic_hill_climbing  # Import the stochastic hill-climbing function
from algorithms.simulatedannealing import simulated_annealing  # Import the simulated annealing function
from algorithms.genetic import genetic_algorithm  # Import the genetic algorithm function

class MagicCube:
    def __init__(self, cube_data=None, size=5):
        """
        Initializes the MagicCube instance with either provided cube_data or generates a random cube.
        Arguments:
        - cube_data: A 3D array of size^3 elements. If None, a shuffled cube is generated.
        - size: The size of the cube, default is 5.
        """
        self.size = size
        if cube_data is not None:
            self.cube = np.array(cube_data).reshape((size, size, size))  # Convert cube_data to a 3D numpy array
        else:
            # Generate a list of numbers from 1 to size^3 and shuffle them to fill the cube
            numbers = list(range(1, size**3 + 1))
            np.random.shuffle(numbers)
            self.cube = np.array(numbers).reshape((size, size, size))
        
        # Calculate the magic number for a magic cube of this size
        self.magic_number = self.calculate_magic_number()

    def calculate_magic_number(self):
        """
        Calculate the magic number for a magic cube.
        Formula: size * (size^3 + 1) // 2
        """
        return (self.size * (self.size**3 + 1)) // 2

    def display(self):
        """
        Displays the current cube configuration.
        """
        print("Cube:")
        print(self.cube)
    
    def calculate_cost(self):
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
        
        # Cost for pillars (z-axis)
        for row in range(self.size):
            for col in range(self.size):
                pillar_sum = self.cube[:, row, col].sum()
                cost += pillar_sum != self.magic_number
        
        # Cost for main diagonals on each level
        for level in range(self.size):
            diag1_sum = np.trace(self.cube[level])  # Left-to-right diagonal
            diag2_sum = np.trace(np.fliplr(self.cube[level]))  # Right-to-left diagonal
            cost += diag1_sum != self.magic_number
            cost += diag2_sum != self.magic_number
        
        # Cost for space diagonals (through all levels)
        diag1 = sum(self.cube[i, i, i] for i in range(self.size))  # Top-left to bottom-right
        diag2 = sum(self.cube[i, i, self.size - i - 1] for i in range(self.size))  # Top-right to bottom-left
        diag3 = sum(self.cube[i, self.size - i - 1, i] for i in range(self.size))  # Bottom-left to top-right
        diag4 = sum(self.cube[i, self.size - i - 1, self.size - i - 1] for i in range(self.size))  # Bottom-right to top-left
        cost += diag1 != self.magic_number
        cost += diag2 != self.magic_number
        cost += diag3 != self.magic_number
        cost += diag4 != self.magic_number

        return cost

    def display_cost(self):
        """
        Displays the current total cost.
        """
        cost = self.calculate_cost()
        print(f"Total Cost: {cost}")

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

# Display the cost of the current cube configuration
magic_cube.display_cost()

com = input("Masukkan algo: ")

if com == "sa":
    steepest_ascent_hill_climbing(magic_cube)
elif com == "sm":
    hill_climbing_with_sideways_move(magic_cube, max_sideways_moves=1000, max_iterations=1000)
elif com == "rr":
    random_restart_hill_climbing(magic_cube)
elif com ==  "s":
    stochastic_hill_climbing(magic_cube) 
elif com == "sa":
    simulated_annealing(magic_cube)
elif com == "g":
    genetic_algorithm(cube_size=5, population_size=100, generations=1000, mutation_rate=0.1, elitism=True)