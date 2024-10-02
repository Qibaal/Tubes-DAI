import random
import matplotlib.pyplot as plt  # Import library for plotting

def selection(population, fitness_scores):
    """
    Select two parents from the population using tournament selection.
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
    Perform crossover between two parent cubes (numpy arrays). Swap a random slice of the cube (e.g., rows or layers).
    """
    size = parent1.shape[0]
    child = parent1.copy()

    # Randomly swap layers between the two parents
    crossover_point = random.randint(0, size - 1)
    if random.random() > 0.5:
        child[:crossover_point] = parent2[:crossover_point]
    else:
        child[:, :crossover_point] = parent2[:, :crossover_point]

    return child  # Returning the cube data (a numpy array)

def mutate(cube):
    """
    Perform mutation by swapping two random elements in the cube (numpy array).
    """
    size = cube.shape[0]
    pos1 = tuple(random.randint(0, size - 1) for _ in range(3))
    pos2 = tuple(random.randint(0, size - 1) for _ in range(3))
    
    # Swap two elements
    cube[pos1], cube[pos2] = cube[pos2], cube[pos1]
    
    return cube

def genetic_algorithm(magic_cube, population_size=100, generations=1000, mutation_rate=0.1, elitism=True):
    """
    Solve the magic cube using a genetic algorithm.
    
    Parameters:
    - magic_cube: An instance of the MagicCube class passed as an argument.
    - population_size: Number of cubes in each generation.
    - generations: Maximum number of generations to run the algorithm.
    - mutation_rate: Probability of mutation.
    - elitism: If True, carry over the best solution to the next generation.
    
    Return Codes:
    - 0: Solution found successfully.
    - 1: Solution not found within the given generations.
    """
    # Initialize the population using the cube passed in (as numpy arrays)
    population = [magic_cube.cube.copy() for _ in range(population_size)]
    best_cube = None
    best_fitness = float('inf')

    # Store best fitness value for each generation
    fitness_progress = []

    for generation in range(generations):
        # Calculate the fitness for each cube in the population
        fitness_scores = [magic_cube.calculate_cost() for magic_cube.cube in population]
        
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
            return 0  # Solution found
        
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
    print(f"Best solution found with fitness {best_fitness}:")
    print(best_cube)
    return 1  # Solution not found within the given generations
