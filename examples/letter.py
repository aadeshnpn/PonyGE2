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


def mane(parameter):
    """ Run program """

    # Run evolution
    individuals = parameter.params['SEARCH_LOOP'](parameter)

    # Print final review
    parameter.stats.get_stats(individuals, end=True)


if __name__ == "__main__":
    #Parameter is the list
    parameters = Parameters()
    parameter_list = ['--parameters', '..,string_match.txt']

    parameters.set_params(parameter_list)

    mane(parameters)
