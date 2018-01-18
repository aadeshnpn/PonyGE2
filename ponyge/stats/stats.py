from copy import copy
from sys import stdout
from time import time
import numpy as np

# from ponyge.algorithm.parameters import params
from ponyge.utilities.algorithm.NSGA2 import compute_pareto_metrics
from ponyge.utilities.algorithm.state import create_state
# from ponyge.utilities.stats import trackers
from ponyge.utilities.stats.save_plots import save_plot_from_data, \
    save_pareto_fitness_plot
from ponyge.utilities.stats.file_io import save_stats_to_file, save_stats_headers, \
    save_best_ind_to_file, save_first_front_to_file


class Stats:
    """Algorithm statistics."""

    def __init__(self, parameter):
        self.stats = {
                "gen": 0,
                "total_inds": 0,
                "regens": 0,
                "invalids": 0,
                "runtime_error": 0,
                "unique_inds": len(parameter.trackers.cache),
                "unused_search": 0,
                "ave_genome_length": 0,
                "max_genome_length": 0,
                "min_genome_length": 0,
                "ave_used_codons": 0,
                "max_used_codons": 0,
                "min_used_codons": 0,
                "ave_tree_depth": 0,
                "max_tree_depth": 0,
                "min_tree_depth": 0,
                "ave_tree_nodes": 0,
                "max_tree_nodes": 0,
                "min_tree_nodes": 0,
                "ave_fitness": 0,
                "best_fitness": 0,
                "time_taken": 0,
                "total_time": 0,
                "time_adjust": 0
                }
        self.parameter = parameter

    def get_stats(self, individuals, end=False):
        """
        Generate the statistics for an evolutionary run. Save statistics to
        utilities.trackers.stats_list. Print statistics. Save fitness plot
        information.

        :param individuals: A population of individuals for which to generate
        statistics.
        :param end: Boolean flag for indicating the end of an evolutionary run.
        :return: Nothing.
        """

        if hasattr(self.parameter.params['FITNESS_FUNCTION'], 'multi_objective'):
            # Multiple objective optimisation is being used.

            # Remove fitness stats from the stats dictionary.
            self.stats.pop('best_fitness', None)
            self.stats.pop('ave_fitness', None)

            # Update stats.
            self.get_moo_stats(individuals, end)

        else:
            # Single objective optimisation is being used.
            self.get_soo_stats(individuals, end)

        if self.parameter.params['SAVE_STATE'] and not self.parameter.params['DEBUG'] and \
                                self.stats['gen'] % self.parameter.params['SAVE_STATE_STEP'] == 0:
            # Save the state of the current evolutionary run.
            create_state(self.parameter, individuals)

    def get_soo_stats(self, individuals, end):
        """
        Generate the statistics for an evolutionary run with a single objective.
        Save statistics to utilities.trackers.stats_list. Print statistics. Save
        fitness plot information.

        :param individuals: A population of individuals for which to generate
        statistics.
        :param end: Boolean flag for indicating the end of an evolutionary run.
        :return: Nothing.
        """
        # Get best individual.
        best = max(individuals)

        if not self.parameter.trackers.best_ever or best > self.parameter.trackers.best_ever:
            # Save best individual in trackers.best_ever.
            self.parameter.trackers.best_ever = best

        if end or self.parameter.params['VERBOSE'] or not self.parameter.params['DEBUG']:
            # Update all stats.
            self.update_stats(individuals, end)

        # Save fitness plot information
        if self.parameter.params['SAVE_PLOTS'] and not self.parameter.params['DEBUG']:
            if not end:
                self.parameter.trackers.best_fitness_list.append(self.parameter.trackers.best_ever.fitness)

            if self.parameter.params['VERBOSE'] or end:
                save_plot_from_data(self.parameter, self.parameter.trackers.best_fitness_list, "best_fitness")

        # Print statistics
        if self.parameter.params['VERBOSE'] and not end:
            self.print_generation_stats()

        elif not self.parameter.params['SILENT']:
            # Print simple display output.
            perc = self.stats['gen'] / (self.parameter.params['GENERATIONS']+1) * 100
            stdout.write("Evolution: %d%% complete\r" % perc)
            stdout.flush()

        # Generate test fitness on regression problems
        if hasattr(self.parameter.params['FITNESS_FUNCTION'], "training_test") and end:

            # Save training fitness.
            self.parameter.trackers.best_ever.training_fitness = copy(self.parameter.trackers.best_ever.fitness)

            # Evaluate test fitness.
            self.parameter.trackers.best_ever.test_fitness = self.parameter.params['FITNESS_FUNCTION'](
                self.parameter.trackers.best_ever, dist='test')

            # Set main fitness as training fitness.
            self.parameter.trackers.best_ever.fitness = self.parameter.trackers.best_ever.training_fitness

        # Save stats to list.
        if self.parameter.params['VERBOSE'] or (not self.parameter.params['DEBUG'] and not end):
            self.parameter.trackers.stats_list.append(copy(self.stats))

        # Save stats to file.
        if not self.parameter.params['DEBUG']:

            if self.stats['gen'] == 0:
                save_stats_headers(self.parameter, self.stats)

            save_stats_to_file(self.parameter, self.stats, end)

            if self.parameter.params['SAVE_ALL']:
                save_best_ind_to_file(self.stats, self.parameter.trackers.best_ever, end, self.stats['gen'])

            elif self.parameter.params['VERBOSE'] or end:
                save_best_ind_to_file(self.stats, self.parameter.trackers.best_ever, end)

        if end and not self.parameter.params['SILENT']:
            self.print_final_stats()


    def get_moo_stats(self, individuals, end):
        """
        Generate the statistics for an evolutionary run with multiple objectives.
        Save statistics to utilities.trackers.stats_list. Print statistics. Save
        fitness plot information.

        :param individuals: A population of individuals for which to generate
        statistics.
        :param end: Boolean flag for indicating the end of an evolutionary run.
        :return: Nothing.
        """

        # Compute the pareto front metrics for the population.
        pareto = compute_pareto_metrics(individuals)

        # Save first front in trackers. Sort arbitrarily along first objective.
        self.parameter.trackers.best_ever = sorted(pareto.fronts[0], key=lambda x: x.fitness[0])

        # Store stats about pareto fronts.
        self.stats['pareto_fronts'] = len(pareto.fronts)
        self.stats['first_front'] = len(pareto.fronts[0])

        if end or self.parameter.params['VERBOSE'] or not self.parameter.params['DEBUG']:
            # Update all stats.
            self.update_stats(individuals, end)

        # Save fitness plot information
        if self.parameter.params['SAVE_PLOTS'] and not self.parameter.params['DEBUG']:

            # Initialise empty array for fitnesses for all inds on first pareto
            # front.
            all_arr = [[] for _ in range(self.parameter.params['FITNESS_FUNCTION'].num_obj)]

            # Generate array of fitness values.
            fitness_array = [ind.fitness for ind in self.parameter.trackers.best_ever]

            # Add paired fitnesses to array for graphing.
            for fit in fitness_array:
                for o in range(self.parameter.params['FITNESS_FUNCTION'].num_obj):
                    all_arr[o].append(fit[o])

            if not end:
                self.parameter.trackers.first_pareto_list.append(all_arr)

                # Append empty array to best fitness list.
                self.parameter.trackers.best_fitness_list.append([])

                # Get best fitness for each objective.
                for o, ff in \
                        enumerate(self.parameter.params['FITNESS_FUNCTION'].fitness_functions):

                    # Get sorted list of all fitness values for objective "o"
                    fits = sorted(all_arr[o], reverse=ff.maximise)

                    # Append best fitness to trackers list.
                    self.parameter.trackers.best_fitness_list[-1].append(fits[0])

            if self.parameter.params['VERBOSE'] or end:

                # Plot best fitness for each objective.
                for o, ff in \
                        enumerate(self.parameter.params['FITNESS_FUNCTION'].fitness_functions):
                    to_plot = [i[o] for i in self.parameter.trackers.best_fitness_list]

                    # Plot fitness data for objective o.
                    save_plot_from_data(self.parameter, to_plot, ff.__class__.__name__)

                # TODO: PonyGE2 can currently only plot moo problems with 2 objectives.
                # Check that the number of fitness objectives is not greater than 2
                if self.parameter.params['FITNESS_FUNCTION'].num_obj > 2:
                    s = "stats.stats.get_moo_stats\n" \
                        "Warning: Plotting of more than 2 simultaneous " \
                        "objectives is not yet enabled in PonyGE2."
                    print(s)

                else:
                    save_pareto_fitness_plot(self.parameter)

        # Print statistics
        if self.parameter.params['VERBOSE'] and not end:
            self.print_generation_stats()
            self.print_first_front_stats()

        elif not self.parameter.params['SILENT']:
            # Print simple display output.
            perc = self.stats['gen'] / (self.parameter.params['GENERATIONS'] + 1) * 100
            stdout.write("Evolution: %d%% complete\r" % perc)
            stdout.flush()

        # Generate test fitness on regression problems
        if hasattr(self.parameter.params['FITNESS_FUNCTION'], "training_test") and end:

            for ind in self.parameter.trackers.best_ever:
                # Iterate over all individuals in the first front.

                # Save training fitness.
                ind.training_fitness = copy(ind.fitness)

                # Evaluate test fitness.
                ind.test_fitness = self.parameter.params['FITNESS_FUNCTION'](ind, dist='test')

                # Set main fitness as training fitness.
                ind.fitness = ind.training_fitness

        # Save stats to list.
        if self.parameter.params['VERBOSE'] or (not self.parameter.params['DEBUG'] and not end):
            self.parameter.trackers.stats_list.append(copy(self.stats))

        # Save stats to file.
        if not self.parameter.params['DEBUG']:

            if self.stats['gen'] == 0:
                save_stats_headers(self.parameter, self.stats)
            
            save_stats_to_file(self.parameter, self.stats, end)

            if self.parameter.params['SAVE_ALL']:
                save_first_front_to_file(self.stats, end, self.stats['gen'])

            elif self.parameter.params['VERBOSE'] or end:
                save_first_front_to_file(self.stats, end)

        if end and not self.parameter.params['SILENT']:
            self.print_final_moo_stats()

    def update_stats(self, individuals, end):
        """
        Update all stats in the stats dictionary.

        :param individuals: A population of individuals.
        :param end: Boolean flag for indicating the end of an evolutionary run.
        :return: Nothing.
        """

        if not end:
            # Time Stats
            self.parameter.trackers.time_list.append(time() - self.stats['time_adjust'])
            self.stats['time_taken'] = self.parameter.trackers.time_list[-1] - \
                                self.parameter.trackers.time_list[-2]
            self.stats['total_time'] = self.parameter.trackers.time_list[-1] - \
                                self.parameter.trackers.time_list[0]

        # Population Stats
        self.stats['total_inds'] = self.parameter.params['POPULATION_SIZE'] * (self.stats['gen'] + 1)
        self.stats['runtime_error'] = len(self.parameter.trackers.runtime_error_cache)
        if self.parameter.params['CACHE']:
            self.stats['unique_inds'] = len(self.parameter.trackers.cache)
            self.stats['unused_search'] = 100 - self.stats['unique_inds'] / \
                                        self.stats['total_inds'] * 100

        # Genome Stats
        genome_lengths = [len(i.genome) for i in individuals]
        self.stats['max_genome_length'] = np.nanmax(genome_lengths)
        self.stats['ave_genome_length'] = np.nanmean(genome_lengths)
        self.stats['min_genome_length'] = np.nanmin(genome_lengths)

        # Used Codon Stats
        codons = [i.used_codons for i in individuals]
        self.stats['max_used_codons'] = np.nanmax(codons)
        self.stats['ave_used_codons'] = np.nanmean(codons)
        self.stats['min_used_codons'] = np.nanmin(codons)

        # Tree Depth Stats
        depths = [i.depth for i in individuals]
        self.stats['max_tree_depth'] = np.nanmax(depths)
        self.stats['ave_tree_depth'] = np.nanmean(depths)
        self.stats['min_tree_depth'] = np.nanmin(depths)

        # Tree Node Stats
        nodes = [i.nodes for i in individuals]
        self.stats['max_tree_nodes'] = np.nanmax(nodes)
        self.stats['ave_tree_nodes'] = np.nanmean(nodes)
        self.stats['min_tree_nodes'] = np.nanmin(nodes)

        if not hasattr(self.parameter.params['FITNESS_FUNCTION'], 'multi_objective'):
            # Fitness Stats
            fitnesses = [i.fitness for i in individuals]
            self.stats['ave_fitness'] = np.nanmean(fitnesses, axis=0)
            self.stats['best_fitness'] = self.parameter.trackers.best_ever.fitness

    def print_generation_stats(self):
        """
        Print the statistics for the generation and individuals.

        :return: Nothing.
        """

        print("______\n")
        for stat in sorted(self.stats.keys()):
            print(" ", stat, ": \t", self.stats[stat])
        print("\n")

    def print_first_front_stats(self):
        """
        Stats printing for the first pareto front for multi-objective optimisation.

        :return: Nothing.
        """

        print("  first front fitnesses :")
        for ind in self.parameter.trackers.best_ever:
            print("\t  ", ind.fitness)

    def print_final_stats(self):
        """
        Prints a final review of the overall evolutionary process.

        :return: Nothing.
        """

        if hasattr(self.parameter.params['FITNESS_FUNCTION'], "training_test"):
            print("\n\nBest:\n  Training fitness:\t",
                self.parameter.trackers.best_ever.training_fitness)
            print("  Test fitness:\t\t", self.parameter.trackers.best_ever.test_fitness)
        else:
            print("\n\nBest:\n  Fitness:\t", self.parameter.trackers.best_ever.fitness)

        print("  Phenotype:", self.parameter.trackers.best_ever.phenotype)
        print("  Genome:", self.parameter.trackers.best_ever.genome)
        self.print_generation_stats()

    def print_final_moo_stats(self):
        """
        Prints a final review of the overall evolutionary process for
        multi-objective problems.

        :return: Nothing.
        """

        print("\n\nFirst Front:")
        for ind in self.parameter.trackers.best_ever:
            print(" ", ind)
        self.print_generation_stats()
