import numpy as np
import random

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

    def calculate_magic_number(self):
        return (self.size * (self.size**3 + 1)) // 2

    def display(self):
        print("Cube:")
        print(self.cube)
    
    def check_rows(self):
        conflicts = 0
        for level in range(self.size):
            for row in range(self.size):
                if self.cube[level, row, :].sum() != self.magic_number:
                    conflicts += 1
        return conflicts

    def check_columns(self):
        conflicts = 0
        for level in range(self.size):
            for col in range(self.size):
                if self.cube[level, :, col].sum() != self.magic_number:
                    conflicts += 1
        return conflicts

    def check_main_diagonals(self):
        conflicts = 0
        for level in range(self.size):
            if np.trace(self.cube[level]) != self.magic_number:
                conflicts += 1
            if np.trace(np.fliplr(self.cube[level])) != self.magic_number:
                conflicts += 1
        return conflicts

    def check_pillars(self):
        conflicts = 0
        for row in range(self.size):
            for col in range(self.size):
                if self.cube[:, row, col].sum() != self.magic_number:
                    conflicts += 1
        return conflicts

    def check_space_diagonals(self):
        conflicts = 0
        diag1 = sum(self.cube[i, i, i] for i in range(self.size))
        diag2 = sum(self.cube[i, i, self.size - i - 1] for i in range(self.size))
        diag3 = sum(self.cube[i, self.size - i - 1, i] for i in range(self.size))
        diag4 = sum(self.cube[i, self.size - i - 1, self.size - i - 1] for i in range(self.size))

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
        conflicts = 0
        for i in range(self.size):
            if sum(self.cube[j, j, i] for j in range(self.size)) != self.magic_number:
                conflicts += 1
        return conflicts

    def check_right_to_left_diagonals(self):
        conflicts = 0
        for i in range(self.size):
            if sum(self.cube[j, self.size - j - 1, i] for j in range(self.size)) != self.magic_number:
                conflicts += 1
        return conflicts

    def count_conflicts(self):
        conflicts = 0
        conflicts += self.check_rows()
        print(self.check_rows())
        conflicts += self.check_columns()
        print(self.check_columns())
        conflicts += self.check_main_diagonals()
        print(self.check_main_diagonals())
        conflicts += self.check_pillars()
        print(self.check_pillars())
        conflicts += self.check_space_diagonals()
        print(self.check_space_diagonals())
        conflicts += self.check_left_to_right_diagonals()
        print(self.check_left_to_right_diagonals())
        conflicts += self.check_right_to_left_diagonals()
        print(self.check_right_to_left_diagonals())
        return conflicts


    def best_neighbour(self):
        """Generates the best neighboring cube by swapping two elements and checking conflicts."""
        best_cube = self.cube.copy()  # Keep a copy of the current cube
        best_conflict_count = self.count_conflicts()  # Current number of conflicts
        
        # Find two different random positions in the cube to swap
        for _ in range(100):  # Limit number of neighbors to explore
            new_cube = self.cube.copy()
            
            # Randomly select two different positions in the 5x5x5 cube
            pos1 = tuple(random.randint(0, self.size - 1) for _ in range(3))
            pos2 = tuple(random.randint(0, self.size - 1) for _ in range(3))
            
            # Ensure positions are different
            if pos1 != pos2:
                # Swap the elements
                new_cube[pos1], new_cube[pos2] = new_cube[pos2], new_cube[pos1]
                
                # Evaluate the new cube (after swap)
                new_conflict_count = self.count_conflicts()
                
                # If the new configuration has fewer conflicts, update the best cube
                if new_conflict_count < best_conflict_count:
                    best_conflict_count = new_conflict_count
                    best_cube = new_cube
        
        self.cube = best_cube  # Update the current cube to the best neighbor
        return best_conflict_count  # Return the number of conflicts of the best neighbor
    
    def solve(self, max_iterations=1000):
        """Solves the magic cube by finding the best neighbors iteratively until the solution is found or a maximum number of iterations is reached."""
        iteration = 0
        current_conflicts = self.count_conflicts()

        while current_conflicts > 0 and iteration < max_iterations:
            print(f"Iteration {iteration}: {current_conflicts} conflicts")
            
            # Get the best neighbor configuration
            current_conflicts = self.best_neighbour()
            
            iteration += 1
        
        # Final check after the loop
        if current_conflicts == 0:
            print(f"Solved the magic cube in {iteration} iterations!")
        else:
            print(f"Stopped after {iteration} iterations with {current_conflicts} conflicts remaining.")

        return current_conflicts == 0  # Return True if solved, False if not solved


cube_data = [
    # First layer
    [
        [78, 109, 15, 41, 72],
        [45, 71, 77, 108, 14],
        [107, 13, 44, 75, 76],
        [74, 80, 106, 12, 43],
        [11, 42, 73, 79, 110]
    ],
    # Second layer
    [
        [40, 66, 97, 103, 9],
        [102, 8, 39, 70, 96],
        [69, 100, 101, 7, 38],
        [6, 37, 68, 99, 105],
        [98, 104, 10, 36, 67]
    ],
    # Third layer
    [
        [122, 3, 34, 65, 91],
        [64, 95, 121, 2, 33],
        [1, 32, 63, 94, 125],
        [93, 124, 5, 31, 62],
        [35, 61, 92, 123, 4]
    ],
    # Fourth layer
    [
        [59, 90, 116, 22, 28],
        [21, 27, 58, 89, 120],
        [88, 119, 25, 26, 57],
        [30, 56, 87, 118, 24],
        [117, 23, 29, 60, 86]
    ],
    # Fifth layer
    [
        [16, 47, 53, 84, 115],
        [83, 114, 20, 46, 52],
        [50, 51, 82, 113, 19],
        [112, 18, 49, 55, 81],
        [54, 85, 111, 17, 48]
    ]
]


magic_cube = MagicCube(cube_data=cube_data)
print(magic_cube.count_conflicts())

# print(f"\nConflicts: {magic_cube.count_conflicts()}")

# print(f'\nneigbour conflict count: {magic_cube.best_neighbour()}')
