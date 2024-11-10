import random
import numpy as np

# Genetic Algorithm Parameters
POPULATION_SIZE = 100
MUTATION_RATE = 0.1
CUBE_SIZE = 5
MAX_GENERATIONS = 1000

# Objective function to calculate deviation
def calculate_deviation(cube):
    target_sum = CUBE_SIZE * (CUBE_SIZE**3 + 1) // 2
    deviation = 0

    # Check rows, columns, and pillars
    for i in range(CUBE_SIZE):
        deviation += abs(target_sum - np.sum(cube[i, :, :]))  # Row sum
        deviation += abs(target_sum - np.sum(cube[:, i, :]))  # Column sum
        deviation += abs(target_sum - np.sum(cube[:, :, i]))  # Pillar sum

    # Check main space diagonals
    deviation += abs(target_sum - np.sum([cube[i, i, i] for i in range(CUBE_SIZE)]))
    deviation += abs(target_sum - np.sum([cube[i, i, CUBE_SIZE - i - 1] for i in range(CUBE_SIZE)]))
    deviation += abs(target_sum - np.sum([cube[i, CUBE_SIZE - i - 1, i] for i in range(CUBE_SIZE)]))
    deviation += abs(target_sum - np.sum([cube[CUBE_SIZE - i - 1, i, i] for i in range(CUBE_SIZE)]))

    return deviation

# Initializing a random individual
def create_individual():
    return np.random.permutation(range(1, CUBE_SIZE**3 + 1)).reshape((CUBE_SIZE, CUBE_SIZE, CUBE_SIZE))

# Fitness function
def fitness(individual):
    return -calculate_deviation(individual)  # Negate deviation for maximization

# Ordered crossover function
def ordered_crossover(parent1, parent2):
    size = CUBE_SIZE**3
    start, end = sorted(random.sample(range(size), 2))
    child1, child2 = np.empty(size, dtype=int), np.empty(size, dtype=int)
    child1.fill(-1)
    child2.fill(-1)

    child1[start:end] = parent1[start:end]
    child2[start:end] = parent2[start:end]

    def fill_child(child, parent):
        current_pos = end % size
        for num in parent:
            if num not in child:
                child[current_pos] = num
                current_pos = (current_pos + 1) % size
        return child

    child1 = fill_child(child1, parent2)
    child2 = fill_child(child2, parent1)

    return child1.reshape((CUBE_SIZE, CUBE_SIZE, CUBE_SIZE)), child2.reshape((CUBE_SIZE, CUBE_SIZE, CUBE_SIZE))

# Mutation function with duplicate prevention
def mutate(individual):
    if random.random() < MUTATION_RATE:
        size = CUBE_SIZE**3
        idx1, idx2 = random.sample(range(size), 2)
        flat_individual = individual.flatten()
        flat_individual[idx1], flat_individual[idx2] = flat_individual[idx2], flat_individual[idx1]
        individual = flat_individual.reshape((CUBE_SIZE, CUBE_SIZE, CUBE_SIZE))
    return individual

# Generating initial population
population = [create_individual() for _ in range(POPULATION_SIZE)]

# Main loop of the genetic algorithm
for generation in range(MAX_GENERATIONS):
    population = sorted(population, key=lambda ind: fitness(ind), reverse=True)

    new_population = population[:10]  # Elitism: keep the top 10 individuals

    while len(new_population) < POPULATION_SIZE:
        parent1, parent2 = random.sample(population[:50], 2)  # Tournament selection
        offspring1, offspring2 = ordered_crossover(parent1.flatten(), parent2.flatten())
        offspring1 = mutate(offspring1)
        offspring2 = mutate(offspring2)
        new_population.extend([offspring1, offspring2])

    population = new_population[:POPULATION_SIZE]

    # Print best result in each generation
    best_fitness = fitness(population[0])
    print(f"Generation {generation}, Best fitness: {best_fitness}")

    if best_fitness == 0:  # Perfect solution found
        print("Optimal solution found!")
        break

# Display the best solution
best_solution = population[0]
print("Best solution:")
print(best_solution)