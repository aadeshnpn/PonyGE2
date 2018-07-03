import datetime

"""
from operators.crossover import (
    crossover, crossover_inds, variable_onepoint, 
    variable_twopoint, fixed_onepoint, fixed_twopoint, subtree, 
    get_max_genome_index
    )
"""
from ponyge.algorithm.step import step
from ponyge.algorithm.parameters import params, set_params

__all__ = ["step","params","set_params"]

__title__ = 'ponyge'
__version__ = '0.0.1'
__license__ = 'Apache 2.0'
__copyright__ = 'Copyright %s Project ponyge Team' % datetime.date.today().year
