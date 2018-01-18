from sys import path
path.append("../src")

from ponyge.utilities.algorithm.general import check_python_version

check_python_version()

from ponyge.algorithm.parameters import params
import ponyge.utilities.algorithm.command_line_parser as parser
from ponyge.representation.grammar import Grammar
from ponyge.utilities.fitness.math_functions import sci_notation

import sys
import os


def main(command_line_args):
    """
    Given a specified grammar file, parse the grammar using the Grammar class
    and print out the number of unique permutations and combinations of
    distinct phenotypes that this grammar is capable of generating at a
    number of given depths.

    :return: Nothing.
    """

    # Parse command line args (we only want the grammar file)
    cmd_args, unknown = parser.parse_cmd_args(command_line_args)

    # Join original params dictionary with command line specified arguments.
    # NOTE that command line arguments overwrite all previously set parameters.
    params.update(cmd_args)

    # Parse grammar file and set grammar class.
    grammar = Grammar(os.path.join("..", "grammars", params['GRAMMAR_FILE']))

    print("\nNumber of unique possible solutions for a range of depths for "
          "specified grammar:", params['GRAMMAR_FILE'], "\n")

    for depth in grammar.permutations:

        print(" Depth: %d \t Number of unique solutions: %s" %
              (depth, sci_notation(grammar.permutations[depth])))


if __name__ == "__main__":

    # Do not write or save any files.
    params['DEBUG'] = True

    # Run main program.
    main(sys.argv[1:])  # exclude the ponyge.py arg itself
