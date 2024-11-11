import random
import numpy as np
import time

# Genetic Algorithm Parameters
POPULATION_SIZE = 100
MUTATION_RATE = 0.1
CUBE_SIZE = 5
MAX_GENERATIONS = 1000

# Assuming MagicCube class is available and has a calculate_cost method
class MagicCube:
    def __init__(self, cube_data=None, size=5):
        self.size = size
        if cube_data is not None:
            self.cube = np.array(cube_data).reshape((size, size, size))
        else:
            numbers = list(range(1, size**3 + 1))
            np.random.shuffle(numbers)
            self.cube = np.array(numbers).reshape((size, size, size))
    
    def calculate_cost(self):
        # Placeholder for actual cost calculation method
        return np.sum(self.cube)  # Replace with actual calculation logic

# Initializing a random individual as a MagicCube instance
def create_individual():
    return MagicCube(cube_data=np.random.permutation(range(1, CUBE_SIZE**3 + 1)))

# Fitness function
def fitness(individual):
    return -individual.calculate_cost()

# Ordered crossover function
def ordered_crossover(parent1, parent2):
    size = CUBE_SIZE**3  # Total number of elements in the cube
    start, end = sorted(random.sample(range(size), 2))  # Random crossover points

    # Flatten cubes for crossover, keeping track of unique elements
    parent1_flat, parent2_flat = parent1.cube.flatten(), parent2.cube.flatten()
    child1, child2 = np.empty(size, dtype=int), np.empty(size, dtype=int)
    child1.fill(-1)
    child2.fill(-1)

    child1[start:end], child2[start:end] = parent1_flat[start:end], parent2_flat[start:end]

    # Helper function to fill remaining spots without duplicates
    def fill_child(child, parent):
        current_pos = end % size
        for num in parent:
            if num not in child:
                child[current_pos] = num
                current_pos = (current_pos + 1) % size
        return child

    child1 = fill_child(child1, parent2_flat)
    child2 = fill_child(child2, parent1_flat)

    # Return children as new MagicCube instances
    return MagicCube(cube_data=child1), MagicCube(cube_data=child2)

# Mutation function with duplicate prevention and correction
def mutate(individual):
    if random.random() < MUTATION_RATE:
        size = CUBE_SIZE**3
        flat_individual = individual.cube.flatten()

        idx1, idx2 = random.sample(range(size), 2)
        flat_individual[idx1], flat_individual[idx2] = flat_individual[idx2], flat_individual[idx1]

        unique_values = set(flat_individual)
        full_range = set(range(1, CUBE_SIZE**3 + 1))
        missing_values = full_range - unique_values

        while len(unique_values) < size:
            for i in range(size):
                if list(flat_individual).count(flat_individual[i]) > 1:
                    flat_individual[i] = missing_values.pop()
                    unique_values = set(flat_individual)

        individual.cube = flat_individual.reshape((CUBE_SIZE, CUBE_SIZE, CUBE_SIZE))
    return individual

def genetic_algorithm(population_size, max_iterations, mutation_rate, elitism):
    results = {
        "initial_cube": create_individual().cube.flatten().tolist(),
        "final_cube": None,
        "final_cost": None,
        "objective_per_iteration": [],
        "population_size": population_size,
        "iterations": max_iterations,
        "duration": None
    }

    start_time = time.time()
    population = [create_individual() for _ in range(population_size)]

    for generation in range(max_iterations):
        population = sorted(population, key=fitness, reverse=True)

        max_obj = fitness(population[0])
        avg_obj = sum(fitness(ind) for ind in population) / population_size
        results["objective_per_iteration"].append((max_obj, avg_obj))

        new_population = population[:10] if elitism else []

        while len(new_population) < population_size:
            parent1, parent2 = random.sample(population[:50], 2)
            offspring1, offspring2 = ordered_crossover(parent1, parent2)
            offspring1 = mutate(offspring1)
            offspring2 = mutate(offspring2)
            new_population.extend([offspring1, offspring2])

        population = new_population[:population_size]

        if fitness(population[0]) == 0:
            break

    end_time = time.time()
    results["final_cube"] = population[0].cube.flatten().tolist()
    results["final_cost"] = -fitness(population[0])
    results["duration"] = end_time - start_time

    return results
