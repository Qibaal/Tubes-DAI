import numpy as np
import random
import matplotlib.pyplot as plt  # Import library for plotting

def create_initial_population(size, population_size):
    """
    Generate an initial population of random 5x5x5 cubes.
    Each cube is a 3D array of shape (5, 5, 5) with numbers from 1 to size^3.
    """
    population = []
    for _ in range(population_size):
        cube = np.random.permutation(range(1, size**3 + 1)).reshape((size, size, size))
        population.append(cube)
    return population

def calculate_fitness(cube, magic_number):
    """
    Calculate the fitness (cost) of a cube.
    The fitness is the sum of absolute differences between the magic number and the sums of all rows, columns, pillars, and diagonals.
    """
    size = cube.shape[0]
    cost = 0
    
    # Cost for rows
    for level in range(size):
        for row in range(size):
            row_sum = cube[level, row, :].sum()
            cost += abs(row_sum - magic_number)
    
    # Cost for columns
    for level in range(size):
        for col in range(size):
            col_sum = cube[level, :, col].sum()
            cost += abs(col_sum - magic_number)
    
    # Cost for pillars (z-axis)
    for row in range(size):
        for col in range(size):
            pillar_sum = cube[:, row, col].sum()
            cost += abs(pillar_sum - magic_number)
    
    # Cost for main diagonals on each level
    for level in range(size):
        diag1_sum = np.trace(cube[level])  # Left-to-right diagonal
        diag2_sum = np.trace(np.fliplr(cube[level]))  # Right-to-left diagonal
        cost += abs(diag1_sum - magic_number)
        cost += abs(diag2_sum - magic_number)
    
    # Cost for space diagonals (through all levels)
    diag1 = sum(cube[i, i, i] for i in range(size))  # Top-left to bottom-right
    diag2 = sum(cube[i, i, size - i - 1] for i in range(size))  # Top-right to bottom-left
    diag3 = sum(cube[i, size - i - 1, i] for i in range(size))  # Bottom-left to top-right
    diag4 = sum(cube[i, size - i - 1, size - i - 1] for i in range(size))  # Bottom-right to top-left
    cost += abs(diag1 - magic_number)
    cost += abs(diag2 - magic_number)
    cost += abs(diag3 - magic_number)
    cost += abs(diag4 - magic_number)

    return cost

def selection(population, fitness_scores):
    """
    Select two parents from the population using tournament selection.
    Use population indices to ensure that no invalid index errors occur.
    """
    tournament_size = 3
    selected_indices = random.sample(range(len(population)), k=tournament_size)
    
    # Get the fitness values for the selected individuals
    selected_fitness = [fitness_scores[i] for i in selected_indices]
    
    # Select the index of the individual with the best (lowest) fitness
    best_index = selected_indices[selected_fitness.index(min(selected_fitness))]
    
    return population[best_index]

def crossover(parent1, parent2):
    """
    Perform crossover between two parent cubes. Swap a random slice of the cube (e.g., rows or layers).
    """
    size = parent1.shape[0]
    child = parent1.copy()

    # Randomly swap layers between the two parents
    crossover_point = random.randint(0, size - 1)
    if random.random() > 0.5:
        child[:crossover_point] = parent2[:crossover_point]
    else:
        child[:, :crossover_point] = parent2[:, :crossover_point]

    return child

def mutate(cube):
    """
    Perform mutation by swapping two random elements in the cube.
    """
    size = cube.shape[0]
    pos1 = tuple(random.randint(0, size - 1) for _ in range(3))
    pos2 = tuple(random.randint(0, size - 1) for _ in range(3))
    
    # Swap two elements
    cube[pos1], cube[pos2] = cube[pos2], cube[pos1]
    
    return cube

def genetic_algorithm(cube_size=5, population_size=100, generations=1000, mutation_rate=0.1, elitism=True):
    """
    Solve the magic cube using a genetic algorithm.
    """
    magic_number = (cube_size * (cube_size**3 + 1)) // 2
    population = create_initial_population(cube_size, population_size)
    best_cube = None
    best_fitness = float('inf')

    # Store best fitness value for each generation
    fitness_progress = []

    for generation in range(generations):
        fitness_scores = [calculate_fitness(cube, magic_number) for cube in population]
        
        # Find the best solution in the current population
        min_fitness = min(fitness_scores)
        if min_fitness < best_fitness:
            best_fitness = min_fitness
            best_cube = population[fitness_scores.index(min_fitness)]
            print(f"Generation {generation}: Best fitness = {best_fitness}")
        
        # Store the best fitness value in the current generation
        fitness_progress.append(best_fitness)
        
        # If we find a perfect solution, terminate early
        if best_fitness == 0:
            print(f"Solution found in generation {generation}")
            print("Best solution found:")
            print(best_cube)
            break
        
        new_population = []
        
        # Elitism: carry the best cube to the next generation
        if elitism:
            new_population.append(best_cube)
        
        # Create the next generation
        while len(new_population) < population_size:
            parent1 = selection(population, fitness_scores)
            parent2 = selection(population, fitness_scores)
            child = crossover(parent1, parent2)
            
            # Mutate the child with a certain probability
            if random.random() < mutation_rate:
                child = mutate(child)
            
            new_population.append(child)
        
        population = new_population
    
    # Plot the fitness progression
    plt.plot(fitness_progress)
    plt.title("Fitness Progression Over Generations")
    plt.xlabel("Generations")
    plt.ylabel("Best Fitness (Cost)")
    plt.grid(True)
    plt.show()

    print("Solution not found within the given generations.")
    print("Best solution found:")
    print(best_cube)
    print(f"Total Cost: {best_fitness}")
    return best_cube
