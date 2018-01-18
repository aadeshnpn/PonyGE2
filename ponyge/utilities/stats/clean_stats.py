from ponyge.stats.stats import stats
# from ponyge.algorithm.parameters import params


def clean_stats(parameter):
    """
    Removes certain unnecessary stats from the stats.stats.stats dictionary
    to clean up the current run.
    
    :return: Nothing.
    """
    
    if not parameter.params['CACHE']:
        stats.pop('unique_inds')
        stats.pop('unused_search')
    
    if not parameter.params['MUTATE_DUPLICATES']:
        stats.pop('regens')
