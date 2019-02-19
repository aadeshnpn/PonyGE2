"""Behavior repetative classes for swarms."""

import random
from ponyge.fitness.base_ff_classes.base_ff import base_ff
import xml.etree.ElementTree as ET


class bt_random(base_ff):
    """
    Calculation the fintness of the individual.
    As the objective fitness is not yet avaliable, we calcualte fitness
    based on the repetative structure of the BT evaluated for itself.
    """

    maximise = True  # True as it ever was.

    def __init__(self, parameter):
        # Initialise base fitness function class.
        super().__init__()

    def evaluate(self, ind, **kwargs):
        # ind.phenotype will be a xml file. We can parse through the xml file
        return random.randint(1, 100)
