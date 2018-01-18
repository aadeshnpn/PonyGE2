from os import path, getcwd, makedirs
from shutil import rmtree
from copy import copy

# from ponyge.algorithm.parameters import params
# from ponyge.utilities.stats import trackers


def save_stats_to_file(parameter, stats, end=False):
    """
    Write the results to a results file for later analysis

    :param stats: The stats.stats.stats dictionary.
    :param end: A boolean flag indicating whether or not the evolutionary
    process has finished.
    :return: Nothing.
    """

    if parameter.params['VERBOSE']:
        filename = path.join(parameter.params['FILE_PATH'], "stats.tsv")
        savefile = open(filename, 'a')
        for stat in sorted(stats.keys()):
            savefile.write(str(stats[stat]) + "\t")
        savefile.write("\n")
        savefile.close()

    elif end:
        filename = path.join(parameter.params['FILE_PATH'], "stats.tsv")
        savefile = open(filename, 'a')
        for item in parameters.trackers.stats_list:
            for stat in sorted(item.keys()):
                savefile.write(str(item[stat]) + "\t")
            savefile.write("\n")
        savefile.close()


def save_stats_headers(parameter, stats):
    """
    Saves the headers for all stats in the stats dictionary.

    :param stats: The stats.stats.stats dictionary.
    :return: Nothing.
    """

    filename = path.join(parameter.params['FILE_PATH'], "stats.tsv")
    savefile = open(filename, 'w')
    for stat in sorted(stats.keys()):
        savefile.write(str(stat) + "\t")
    savefile.write("\n")
    savefile.close()


def save_best_ind_to_file(parameter, stats, ind, end=False, name="best"):
    """
    Saves the best individual to a file.

    :param stats: The stats.stats.stats dictionary.
    :param ind: The individual to be saved to file.
    :param end: A boolean flag indicating whether or not the evolutionary
    process has finished.
    :param name: The name of the individual. Default set to "best".
    :return: Nothing.
    """

    filename = path.join(parameter.params['FILE_PATH'], (str(name) + ".txt"))
    savefile = open(filename, 'w')
    savefile.write("Generation:\n" + str(stats['gen']) + "\n\n")
    savefile.write("Phenotype:\n" + str(ind.phenotype) + "\n\n")
    savefile.write("Genotype:\n" + str(ind.genome) + "\n")
    savefile.write("Tree:\n" + str(ind.tree) + "\n")
    if hasattr(parameter.params['FITNESS_FUNCTION'], "training_test"):
        if end:
            savefile.write("\nTraining fitness:\n" + str(ind.training_fitness))
            savefile.write("\nTest fitness:\n" + str(ind.test_fitness))
        else:
            savefile.write("\nFitness:\n" + str(ind.fitness))
    else:
        savefile.write("\nFitness:\n" + str(ind.fitness))
    savefile.close()


def save_first_front_to_file(parameter, stats, end=False, name="first"):
    """
    Saves all individuals in the first front to individual files in a folder.

    :param stats: The stats.stats.stats dictionary.
    :param end: A boolean flag indicating whether or not the evolutionary
                process has finished.
    :param name: The name of the front folder. Default set to "first_front".
    :return: Nothing.
    """

    # Save the file path (we will be over-writing it).
    orig_file_path = copy(parameter.params['FILE_PATH'])

    # Define the new file path.
    parameter.params['FILE_PATH'] = path.join(orig_file_path, str(name)+"_front")

    # Check if the front folder exists already
    if path.exists(parameter.params['FILE_PATH']):

        # Remove previous files.
        rmtree(parameter.params['FILE_PATH'])

    # Create front folder.
    makedirs(parameter.params['FILE_PATH'])

    for i, ind in enumerate(parameters.trackers.best_ever):
        # Save each individual in the first front to file.
        save_best_ind_to_file(stats, ind, end, name=str(i))

    # Re-set the file path.
    parameter.params['FILE_PATH'] = copy(orig_file_path)


def generate_folders_and_files(parameter):
    """
    Generates necessary folders and files for saving statistics and parameters.

    :return: Nothing.
    """

    if parameter.params['EXPERIMENT_NAME']:
        # Experiment manager is being used.
        path_1 = path.join(getcwd(), "..", "results")

        if not path.isdir(path_1):
            # Create results folder.
            makedirs(path_1)

        # Set file path to include experiment name.
        parameter.params['FILE_PATH'] = path.join(path_1, parameter.params['EXPERIMENT_NAME'])

    else:
        # Set file path to results folder.
        parameter.params['FILE_PATH'] = path.join(getcwd(), "..", "results")

    # Generate save folders
    if not path.isdir(parameter.params['FILE_PATH']):
        makedirs(parameter.params['FILE_PATH'])

    if not path.isdir(path.join(parameter.params['FILE_PATH'],
                                str(parameter.params['TIME_STAMP']))):
        makedirs(path.join(parameter.params['FILE_PATH'],
                        str(parameter.params['TIME_STAMP'])))

    parameter.params['FILE_PATH'] = path.join(parameter.params['FILE_PATH'],
                                    str(parameter.params['TIME_STAMP']))

    save_params_to_file(parameter)


def save_params_to_file(parameter):
    """
    Save evolutionary parameters in a parameters.txt file.

    :return: Nothing.
    """

    # Generate file path and name.
    filename = path.join(parameter.params['FILE_PATH'], "parameters.txt")
    savefile = open(filename, 'w')

    # Justify whitespaces for pretty printing/saving.
    col_width = max(len(param) for param in parameter.params.keys())

    for param in sorted(parameter.params.keys()):

        # Create whitespace buffer for pretty printing/saving.
        spaces = [" " for _ in range(col_width - len(param))]
        savefile.write(str(param) + ": " + "".join(spaces) +
                       str(parameter.params[param]) + "\n")

    savefile.close()
