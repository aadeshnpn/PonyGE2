from multiprocessing import Pool
# from ponyge.algorithm.parameters import params
from ponyge.fitness.evaluation import evaluate_fitness
# from ponyge.stats.stats import stats, get_stats
# from ponyge.utilities.stats import trackers
from ponyge.operators.initialisation import initialisation
from ponyge.utilities.algorithm.initialise_run import pool_init


def search_loop(parameter):
    """
    This is a standard search process for an evolutionary algorithm. Loop over
    a given number of generations.
    
    :return: The final population after the evolutionary process has run for
    the specified number of generations.
    """

    # print ('stats generation one value',stats['gen'])
    # exit()
    if parameter.params['MULTICORE']:
        # initialize pool once, if mutlicore is enabled
        parameter.params['POOL'] = Pool(processes=parameter.params['CORES'], initializer=pool_init,
                              initargs=(parameter.params,))  # , maxtasksperchild=1)

    # Initialise population
    individuals = initialisation(parameter, parameter.params['POPULATION_SIZE'])

    # Evaluate initial population
    individuals = evaluate_fitness(individuals, parameter)

    # Generate statistics for run so far
    parameter.stats.get_stats(individuals)

    # print (stats)
    # exit()
    # print ('stats generation one value',stats['gen'])
    # exit()
    # Traditional GE
    for generation in range(1, (parameter.params['GENERATIONS']+1)):
        parameter.stats.stats['gen'] = generation

        # New generation
        individuals = parameter.params['STEP'](parameter, individuals)

    if parameter.params['MULTICORE']:
        # Close the workers pool (otherwise they'll live on forever).
        parameter.params['POOL'].close()

    return individuals


def search_loop_from_state(parameter):
    """
    Run the evolutionary search process from a loaded state. Pick up where
    it left off previously.

    :return: The final population after the evolutionary process has run for
    the specified number of generations.
    """
    
    individuals = parameter.trackers.state_individuals
    
    if parameter.params['MULTICORE']:
        # initialize pool once, if mutlicore is enabled
        parameter.params['POOL'] = Pool(processes=parameter.params['CORES'], initializer=pool_init,
                              initargs=(parameter.params,))  # , maxtasksperchild=1)
    
    # Traditional GE
    for generation in range(parameter.stats['gen'] + 1, (parameter.params['GENERATIONS'] + 1)):
        parameter.stats.stats['gen'] = generation
        
        # New generation
        individuals = parameter.params['STEP'](individuals)
    
    if parameter.params['MULTICORE']:
        # Close the workers pool (otherwise they'll live on forever).
        parameter.params['POOL'].close()
    
    return individuals
