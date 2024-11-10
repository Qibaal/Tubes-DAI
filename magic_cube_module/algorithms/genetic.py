import random
import numpy as np
import time

# Genetic Algorithm Parameters
POPULATION_SIZE = 100
MUTATION_RATE = 0.1
CUBE_SIZE = 5
MAX_GENERATIONS = 1000

# Objective function to calculate deviation
def calculate_deviation(cube):
    target_sum = CUBE_SIZE * (CUBE_SIZE**3 + 1) // 2  # The target sum for rows, columns, and diagonals
    deviation = 0

    # Check rows, columns, and pillars
    for i in range(CUBE_SIZE):
        deviation += abs(target_sum - np.sum(cube[i, :, :]))  # Row sum deviation
        deviation += abs(target_sum - np.sum(cube[:, i, :]))  # Column sum deviation
        deviation += abs(target_sum - np.sum(cube[:, :, i]))  # Pillar sum deviation

    # Check main space diagonals
    deviation += abs(target_sum - np.sum([cube[i, i, i] for i in range(CUBE_SIZE)]))  # Main diagonal 1
    deviation += abs(target_sum - np.sum([cube[i, i, CUBE_SIZE - i - 1] for i in range(CUBE_SIZE)]))  # Main diagonal 2
    deviation += abs(target_sum - np.sum([cube[i, CUBE_SIZE - i - 1, i] for i in range(CUBE_SIZE)]))  # Main diagonal 3
    deviation += abs(target_sum - np.sum([cube[CUBE_SIZE - i - 1, i, i] for i in range(CUBE_SIZE)]))  # Main diagonal 4

    return deviation  # Return the total deviation

# Initializing a random individual
def create_individual():
    # Create a 3D array with unique numbers shuffled randomly
    return np.random.permutation(range(1, CUBE_SIZE**3 + 1)).reshape((CUBE_SIZE, CUBE_SIZE, CUBE_SIZE))

# Fitness function
def fitness(individual):
    # Return negative deviation for maximization (lower deviation is better)
    return -calculate_deviation(individual)

# Ordered crossover function
def ordered_crossover(parent1, parent2):
    size = CUBE_SIZE**3  # Total number of elements in the cube
    start, end = sorted(random.sample(range(size), 2))  # Random crossover points

    # Initialize children with placeholders
    child1, child2 = np.empty(size, dtype=int), np.empty(size, dtype=int)
    child1.fill(-1)
    child2.fill(-1)

    # Copy crossover segment from parents to children
    child1[start:end] = parent1[start:end]
    child2[start:end] = parent2[start:end]

    # Fill the rest of the child with non-duplicate elements from the other parent
    def fill_child(child, parent):
        current_pos = end % size
        for num in parent:
            if num not in child:
                child[current_pos] = num
                current_pos = (current_pos + 1) % size
        return child

    child1 = fill_child(child1, parent2)
    child2 = fill_child(child2, parent1)

    # Reshape children into 3D arrays and return
    return child1.reshape((CUBE_SIZE, CUBE_SIZE, CUBE_SIZE)), child2.reshape((CUBE_SIZE, CUBE_SIZE, CUBE_SIZE))

# Mutation function with duplicate prevention and correction
def mutate(individual):
    if random.random() < MUTATION_RATE:  # Check if mutation should occur
        size = CUBE_SIZE**3
        flat_individual = individual.flatten()  # Flatten the 3D array for easier manipulation

        # Swap two random elements
        idx1, idx2 = random.sample(range(size), 2)
        flat_individual[idx1], flat_individual[idx2] = flat_individual[idx2], flat_individual[idx1]

        # Check and correct duplicates
        unique_values = set(flat_individual)
        full_range = set(range(1, CUBE_SIZE**3 + 1))
        missing_values = full_range - unique_values  # Find values that should be in the cube but aren't

        while len(unique_values) < size:  # Check if duplicates exist
            for i in range(size):
                if list(flat_individual).count(flat_individual[i]) > 1:  # Detect duplicates
                    flat_individual[i] = missing_values.pop()  # Replace duplicate with a unique value
                    unique_values = set(flat_individual)  # Update unique values set

        # Reshape the flat array back into a 3D array
        individual = flat_individual.reshape((CUBE_SIZE, CUBE_SIZE, CUBE_SIZE))
    return individual

# Genetic algorithm function
def genetic_algorithm(cube, population_size=POPULATION_SIZE, generations=MAX_GENERATIONS, mutation_rate=MUTATION_RATE, elitism=True):
    # Create an initial population of individuals
    population = [create_individual() for _ in range(population_size)]

    for generation in range(generations):
        # Sort the population by fitness (descending order)
        population = sorted(population, key=lambda ind: fitness(ind), reverse=True)

        # Create a new population with elitism (retain top individuals)
        new_population = population[:10] if elitism else []

        # Generate new individuals through crossover and mutation
        while len(new_population) < population_size:
            parent1, parent2 = random.sample(population[:50], 2)  # Select parents from the top 50
            offspring1, offspring2 = ordered_crossover(parent1.flatten(), parent2.flatten())
            offspring1 = mutate(offspring1)  # Apply mutation
            offspring2 = mutate(offspring2)
            new_population.extend([offspring1, offspring2])

        # Update the population for the next generation
        population = new_population[:population_size]

        # Check for the best fitness in the current generation
        best_fitness = fitness(population[0])
        if best_fitness == 0:  # Stop if a perfect solution is found
            break

    # Return the final results
    return -best_fitness, population[0], generation, [fitness(ind) for ind in population]