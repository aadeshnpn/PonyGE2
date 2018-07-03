# from ponyge.utilities.stats.trackers import cache, runtime_error_cache
import numpy as np
# from ponyge.algorithm.parameters import params
# from ponyge.stats.stats import stats


def evaluate_fitness(individuals, parameter):
    """
    Evaluate an entire population of individuals. Invalid individuals are given
    a default bad fitness. If params['CACHE'] is specified then individuals
    have their fitness stored in a dictionary called utilities.trackers.cache.
    Dictionary keys are the string of the phenotype.
    There are currently three options for use with the cache:
        1. If params['LOOKUP_FITNESS'] is specified (default case if
           params['CACHE'] is specified), individuals which have already been
           evaluated have their previous fitness read directly from the cache,
           thus saving fitness evaluations.
        2. If params['LOOKUP_BAD_FITNESS'] is specified, individuals which
           have already been evaluated are given a default bad fitness.
        3. If params['MUTATE_DUPLICATES'] is specified, individuals which
           have already been evaluated are mutated to produce new unique
           individuals which have not been encountered yet by the search
           process.

    :param individuals: A population of individuals to be evaluated.
    :return: A population of fully evaluated individuals.
    """

    results, pool = [], None
    
    if parameter.params['MULTICORE']:
        pool = parameter.params['POOL']

    for name, ind in enumerate(individuals):
        ind.name = name

        # Iterate over all individuals in the population.
        if ind.invalid:
            # Invalid individuals cannot be evaluated and are given a bad
            # default fitness.
            ind.fitness = parameter.params['FITNESS_FUNCTION'].default_fitness
            parameter.stats.stats['invalids'] += 1

        else:
            eval_ind = True

            # Valid individuals can be evaluated.
            if parameter.params['CACHE'] and ind.phenotype in parameter.trackers.cache:
                # The individual has been encountered before in
                # the utilities.trackers.cache.

                if parameter.params['LOOKUP_FITNESS']:
                    # Set the fitness as the previous fitness from the
                    # cache.
                    ind.fitness = parameter.trackers.cache[ind.phenotype]
                    eval_ind = False

                elif parameter.params['LOOKUP_BAD_FITNESS']:
                    # Give the individual a bad default fitness.
                    ind.fitness = parameter.params['FITNESS_FUNCTION'].default_fitness
                    eval_ind = False

                elif parameter.params['MUTATE_DUPLICATES']:
                    # Mutate the individual to produce a new phenotype
                    # which has not been encountered yet.
                    while (not ind.phenotype) or ind.phenotype in parameter.trackers.cache:
                        ind = parameter.params['MUTATION'](ind)
                        parameter.stats.stats['regens'] += 1
                    
                    # Need to overwrite the current individual in the pop.
                    individuals[name] = ind
                    ind.name = name

            if eval_ind:
                results = eval_or_append(parameter, ind, results, pool)

    if parameter.params['MULTICORE']:
        for result in results:
            # Execute all jobs in the pool.
            ind = result.get()

            # Set the fitness of the evaluated individual by placing the
            # evaluated individual back into the population.
            individuals[ind.name] = ind

            # Add the evaluated individual to the cache.
            parameter.trackers.cache[ind.phenotype] = ind.fitness
        
            # Check if individual had a runtime error.
            if ind.runtime_error:
                parameter.trackers.runtime_error_cache.append(ind.phenotype)
                    
    return individuals


def eval_or_append(parameter, ind, results, pool):
    """
    Evaluates an individual if sequential evaluation is being used. If
    multi-core parallel evaluation is being used, adds the individual to the
    pool to be evaluated.

    :param ind: An individual to be evaluated.
    :param results: A list of individuals to be evaluated by the multicore
    pool of workers.
    :param pool: A pool of workers for multicore evaluation.
    :return: The evaluated individual or the list of individuals to be
    evaluated.
    """

    if parameter.params['MULTICORE']:
        # Add the individual to the pool of jobs.
        results.append(pool.apply_async(ind.evaluate, ()))
        return results
    
    else:
        # Evaluate the individual.
        ind.evaluate()

        # Check if individual had a runtime error.
        if ind.runtime_error:
            parameter.trackers.runtime_error_cache.append(ind.phenotype)

        if parameter.params['CACHE']:
            # The phenotype string of the individual does not appear
            # in the cache, it must be evaluated and added to the
            # cache.
            
            if (isinstance(ind.fitness, list) and not
                    any([np.isnan(i) for i in ind.fitness])) or \
                    (not isinstance(ind.fitness, list) and not
                     np.isnan(ind.fitness)):
                
                # All fitnesses are valid.
                parameter.trackers.cache[ind.phenotype] = ind.fitness
