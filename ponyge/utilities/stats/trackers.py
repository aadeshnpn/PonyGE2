

class Trackers:
    """Utilities for tracking progress.
    
    of runs, including time taken per
    generation, fitness plots, fitness caches, etc.
    """

    def __init__(self):
        
        self.cache = {}
        # This dict stores the cache for an evolutionary run. The key for each entry
        # is the phenotype of the individual, the value is its fitness.

        self.runtime_error_cache = []
        # This list stores a list of phenotypes which produce runtime errors over an
        # evolutionary run.

        self.best_fitness_list = []
        # fitness_plot is simply a list of the best fitnesses at each generation.
        # Useful for plotting evolutionary progress.

        self.first_pareto_list = []
        # first_pareto_list stores the list of all individuals stored on the first
        # pareto front during multi objective optimisation.

        self.time_list = []
        # time_list stores the system time after each generation has been completed.
        # Useful for keeping track of how long each generation takes.

        self.stats_list = []
        # List for storing stats at each generation
        # Used when verbose mode is off to speed up program

        self.best_ever = None
        # Store the best ever individual here.
