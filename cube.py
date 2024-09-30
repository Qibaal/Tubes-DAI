import numpy as np
import random

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
    
    def check_rows(self):
        """
        Check all rows in each level of the cube.
        Returns the number of rows whose sum doesn't equal the magic number.
        """
        conflicts = 0
        for level in range(self.size):
            for row in range(self.size):
                if self.cube[level, row, :].sum() != self.magic_number:
                    conflicts += 1
        return conflicts

    def check_columns(self):
        """
        Check all columns in each level of the cube.
        Returns the number of columns whose sum doesn't equal the magic number.
        """
        conflicts = 0
        for level in range(self.size):
            for col in range(self.size):
                if self.cube[level, :, col].sum() != self.magic_number:
                    conflicts += 1
        return conflicts

    def check_main_diagonals(self):
        """
        Check the main diagonals of each level in the cube (both left-to-right and right-to-left).
        Returns the number of diagonals whose sum doesn't equal the magic number.
        """
        conflicts = 0
        for level in range(self.size):
            if np.trace(self.cube[level]) != self.magic_number:  # Check left-to-right diagonal
                conflicts += 1
            if np.trace(np.fliplr(self.cube[level])) != self.magic_number:  # Check right-to-left diagonal
                conflicts += 1
        return conflicts

    def check_pillars(self):
        """
        Check all pillars (vertical lines along the z-axis) in the cube.
        Returns the number of pillars whose sum doesn't equal the magic number.
        """
        conflicts = 0
        for row in range(self.size):
            for col in range(self.size):
                if self.cube[:, row, col].sum() != self.magic_number:
                    conflicts += 1
        return conflicts

    def check_space_diagonals(self):
        """
        Check the four space diagonals that span through all levels of the cube.
        Returns the number of space diagonals whose sum doesn't equal the magic number.
        """
        conflicts = 0
        diag1 = sum(self.cube[i, i, i] for i in range(self.size))  # Top-left to bottom-right diagonal
        diag2 = sum(self.cube[i, i, self.size - i - 1] for i in range(self.size))  # Top-right to bottom-left diagonal
        diag3 = sum(self.cube[i, self.size - i - 1, i] for i in range(self.size))  # Bottom-left to top-right diagonal
        diag4 = sum(self.cube[i, self.size - i - 1, self.size - i - 1] for i in range(self.size))  # Bottom-right to top-left diagonal

        # Check if each diagonal matches the magic number
        if diag1 != self.magic_number:
            conflicts += 1
        if diag2 != self.magic_number:
            conflicts += 1
        if diag3 != self.magic_number:
            conflicts += 1
        if diag4 != self.magic_number:
            conflicts += 1

        return conflicts

    def check_left_to_right_diagonals(self):
        """
        Check the diagonals that run from left to right across the cube (on each level along the z-axis).
        Returns the number of such diagonals whose sum doesn't equal the magic number.
        """
        conflicts = 0
        for i in range(self.size):
            if sum(self.cube[j, j, i] for j in range(self.size)) != self.magic_number:
                print("Left to right: ", sum(self.cube[j, j, i] for j in range(self.size)))
                conflicts += 1
        return conflicts

    def check_right_to_left_diagonals(self):
        """
        Check the diagonals that run from right to left across the cube (on each level along the z-axis).
        Returns the number of such diagonals whose sum doesn't equal the magic number.
        """
        conflicts = 0
        for i in range(self.size):
            if sum(self.cube[j, self.size - j - 1, i] for j in range(self.size)) != self.magic_number:
                print("Right to left: ", sum(self.cube[j, self.size - j - 1, i] for j in range(self.size)))
                conflicts += 1
        return conflicts

    def count_conflicts(self):
        """
        Counts the total number of conflicts across rows, columns, diagonals, pillars, and space diagonals.
        Returns the total number of conflicts in the cube.
        """
        conflicts = 0
        conflicts += self.check_rows()
        conflicts += self.check_columns()
        conflicts += self.check_main_diagonals()
        conflicts += self.check_pillars()
        conflicts += self.check_space_diagonals()
        conflicts += self.check_left_to_right_diagonals()
        print(self.check_left_to_right_diagonals())  # Optional debug statement
        conflicts += self.check_right_to_left_diagonals()
        print(self.check_right_to_left_diagonals())  # Optional debug statement
        return conflicts

    def best_neighbour(self):
        """
        Finds the best neighboring cube by swapping two elements randomly and checking conflicts.
        Returns the conflict count of the best neighboring configuration found.
        """
        best_cube = self.cube.copy()  # Keep a copy of the current cube
        best_conflict_count = self.count_conflicts()  # Get current number of conflicts
        
        # Try swapping two elements randomly in the cube and check for better configurations
        for _ in range(100):  # Limit the number of neighbors to explore
            new_cube = self.cube.copy()
            
            # Select two random positions in the 5x5x5 cube
            pos1 = tuple(random.randint(0, self.size - 1) for _ in range(3))
            pos2 = tuple(random.randint(0, self.size - 1) for _ in range(3))
            
            # Ensure the positions are different before swapping
            if pos1 != pos2:
                new_cube[pos1], new_cube[pos2] = new_cube[pos2], new_cube[pos1]  # Swap the elements
                
                # Calculate the number of conflicts in the new cube
                new_conflict_count = self.count_conflicts()
                
                # If the new configuration has fewer conflicts, update the best cube
                if new_conflict_count < best_conflict_count:
                    best_conflict_count = new_conflict_count
                    best_cube = new_cube
        
        self.cube = best_cube  # Update the current cube to the best neighbor found
        return best_conflict_count  # Return the conflict count of the best neighbor
    
    def solve(self, max_iterations=1000):
        """
        Solves the magic cube by iteratively finding the best neighbors until the solution is found
        or the maximum number of iterations is reached.
        """
        iteration = 0
        current_conflicts = self.count_conflicts()  # Initial conflict count

        # Iterate until there are no conflicts or the maximum number of iterations is reached
        while current_conflicts > 0 and iteration < max_iterations:
            print(f"Iteration {iteration}: {current_conflicts} conflicts")
            
            # Find the best neighboring configuration
            current_conflicts = self.best_neighbour()
            
            iteration += 1
        
        # Final result after all iterations
        if current_conflicts == 0:
            print(f"Solved the magic cube in {iteration} iterations!")
        else:
            print(f"Stopped after {iteration} iterations with {current_conflicts} conflicts remaining.")

        return current_conflicts == 0  # Return True if solved, False if not


# Define the cube data for testing
cube_data = [
    # First layer
    [
        [67, 18, 119, 106, 5],
        [116, 17, 14, 73, 95],
        [40, 50, 81, 65, 79],
        [56, 120, 55, 49, 35],
        [36, 110, 46, 22, 101]
    ],
    # Second layer
    [
        [66, 72, 27, 102, 48],
        [26, 39, 92, 44, 114],
        [32, 93, 88, 83, 19],
        [113, 57, 9, 62, 74],
        [78, 54, 99, 24, 60]
    ],
    # Third layer
    [
        [42, 111, 85, 2, 75],
        [30, 118, 21, 123, 23],
        [89, 68, 63, 58, 37],
        [103, 3, 105, 8, 96],
        [51, 15, 41, 124, 84]
    ],
    # Fourth layer
    [
        [115, 98, 4, 1, 97],
        [52, 64, 117, 69, 13],
        [107, 43, 38, 33, 94],
        [12, 82, 34, 87, 100],
        [29, 28, 122, 125, 11]
    ],
    # Fifth layer
    [
        [25, 16, 80, 104, 90],
        [91, 77, 71, 6, 70],
        [47, 61, 45, 76, 86],
        [31, 53, 112, 109, 10],
        [121, 108, 7, 20, 59]
    ]
]

# Initialize the magic cube with the provided cube data
magic_cube = MagicCube(cube_data=cube_data)
print(magic_cube.count_conflicts())  # Count initial conflicts
