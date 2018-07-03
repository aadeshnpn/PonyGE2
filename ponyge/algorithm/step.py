from ponyge.fitness.evaluation import evaluate_fitness
from ponyge.operators.crossover import crossover
from ponyge.operators.mutation import mutation
from ponyge.operators.replacement import replacement, steady_state
from ponyge.operators.selection import selection
# from ponyge.stats.stats import get_stats


def step(parameter, individuals):
    """
    Runs a single generation of the evolutionary algorithm process:
        Selection
        Variation
        Evaluation
        Replacement
    
    :param individuals: The current generation, upon which a single
    evolutionary generation will be imposed.
    :return: The next generation of the population.
    """

    # Select parents from the original population.
    parents = selection(parameter, individuals)

    # Crossover parents and add to the new population.
    cross_pop = crossover(parameter, parents)

    # Mutate the new population.
    new_pop = mutation(parameter, cross_pop)

    # Evaluate the fitness of the new population.
    new_pop = evaluate_fitness(new_pop, parameter)

    # Replace the old population with the new population.
    individuals = replacement(parameter, new_pop, individuals)

    # Generate statistics for run so far
    parameter.stats.get_stats(individuals)
    
    return individuals


def steady_state_step(parameter, individuals):
    """
    Runs a single generation of the evolutionary algorithm process,
    using steady state replacement.

    :param individuals: The current generation, upon which a single
    evolutionary generation will be imposed.
    :return: The next generation of the population.
    """
    
    individuals = steady_state(parameter, individuals)
    
    return individuals 