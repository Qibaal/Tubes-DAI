import numpy as np
import random
import matplotlib.pyplot as plt  # Import library for plotting

def create_initial_population(magic_cube, population_size):
    """
    Generate an initial population of random cubes with the same shape as the given magic_cube.
    """
    population = []
    size = magic_cube.size
    for _ in range(population_size):
        cube = np.random.permutation(range(1, size**3 + 1)).reshape((size, size, size))
        population.append(cube)
    return population

def calculate_fitness(cube, magic_cube):
    """
    Calculate the fitness of the cube using the objective function from the MagicCube class.
    """
    magic_cube.cube = cube  # Update the cube in the MagicCube instance
    return magic_cube.calculate_cost()

def selection(population, fitness_scores):
    """
    Select two parents from the population using tournament selection.
    """
    tournament_size = 3
    selected_indices = random.sample(range(len(population)), k=tournament_size)
    selected_fitness = [fitness_scores[i] for i in selected_indices]
    best_index = selected_indices[selected_fitness.index(min(selected_fitness))]
    return population[best_index]

def crossover(parent1, parent2):
    """
    Perform crossover between two parent cubes.
    """
    size = parent1.shape[0]
    child = parent1.copy()
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
    cube[pos1], cube[pos2] = cube[pos2], cube[pos1]
    return cube

def genetic_algorithm(magic_cube, population_size=100, generations=1000, mutation_rate=0.15, elitism=True):
    """
    Solve the magic cube using a genetic algorithm.
    """
    population = create_initial_population(magic_cube, population_size)
    best_cube = None
    best_fitness = float('inf')
    fitness_progress = []

    for generation in range(generations):
        fitness_scores = [calculate_fitness(cube, magic_cube) for cube in population]
        min_fitness = min(fitness_scores)
        if min_fitness < best_fitness:
            best_fitness = min_fitness
            best_cube = population[fitness_scores.index(min_fitness)]
            print(f"Generation {generation}: Best fitness = {best_fitness}")

        fitness_progress.append(best_fitness)

        if best_fitness == 0:
            print(f"Solution found in generation {generation}")
            print("Best solution found:")
            print(best_cube)
            break

        new_population = []
        if elitism:
            new_population.append(best_cube)

        while len(new_population) < population_size:
            parent1 = selection(population, fitness_scores)
            parent2 = selection(population, fitness_scores)
            child = crossover(parent1, parent2)
            if random.random() < mutation_rate:
                child = mutate(child)
            new_population.append(child)

        population = new_population

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
