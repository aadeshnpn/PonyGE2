# PonyGE2
# Copyright (c) 2017 Michael Fenton, James McDermott,
#                    David Fagan, Stefan Forstenlechner,
#                    and Erik Hemberg
# Hereby licensed under the GNU GPL v3.
""" Python GE implementation """

from ponyge.utilities.algorithm.general import check_python_version

check_python_version()

# from ponyge.stats.stats import get_stats
from ponyge.algorithm.parameters import Parameters
import sys


def run(parameter):
    """ Run program """

    # Run evolution
    #print (type(parameter.params))
    individuals = parameter.params['SEARCH_LOOP'](parameter)

    # Print final review
    parameter.stats.get_stats(individuals, end=True)


if __name__ == "__main__":

    # Parameter is the list. Initialized it
    parameters = Parameters()

    # Read the parameter file for santa fe trail example
    parameter_list = ['--parameters', '..,santa_fe_trail.txt']

    # Load the parameter
    parameters.set_params(parameter_list)

    run(parameters)
