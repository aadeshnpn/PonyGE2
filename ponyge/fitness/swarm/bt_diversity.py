from ponyge.fitness.base_ff_classes.base_ff import base_ff
import xml.etree.ElementTree as ET
import math

class bt_diversity(base_ff):
    """
    Calculation the fintness of the individual.
    As the objective fitness is not yet avaliable, we calcualte fitness
    based on the diversity of the BT evaluated for itself
    """

    maximise = True  # True as it ever was.

    def __init__(self, parameter):
        # Initialise base fitness function class.
        super().__init__()
        """
        self.execution_behaviors = ['IsCarryable', 'IsSingleCarry',
        'SingleCarry', 'NeighbourObjects', 'IsMultipleCarry',
        'IsInPartialAttached', 'InitiateMultipleCarry',
        'IsEnoughStrengthToCarry', 'Move', 'GoTo',
        'IsMotionTrue', 'RandomWalk', 'IsMoveable', 'MultipleCarry']
        """
        self.execution_behaviors = ['MoveTowards', 'Explore',
        'CompositeSingleCarry','CompositeDrop', 'MoveAway', 'IsDropable',
        'NeighbourObjects']
        self.execution_behaviors.sort()

    def calcualte_diversity(self):
        self.sorted_keys = list(self.execution.keys())
        self.sorted_keys.sort()
        self.sorted_values = list(self.execution.values())
        self.sorted_values.sort()
        new_execution = dict()
        sorted_values_sum = sum(self.sorted_values)
        behavior_len = len(self.execution_behaviors)
        divisor = math.ceil(sorted_values_sum / behavior_len) * behavior_len
        if self.sorted_keys == self.execution_behaviors and \
                sorted_values_sum % behavior_len == 0 and \
                self.sorted_values[0] == int(
                    sorted_values_sum / behavior_len):
                    diversity = 1
        elif self.sorted_keys == self.execution_behaviors and \
                self.sorted_values[0] <= int(
                    sorted_values_sum / behavior_len):
                    for a in self.execution.keys():
                        self.execution[a] -= self.sorted_values[0]
                        if self.execution[a] > 0:
                            new_execution[a] = self.execution[a]

                    other_match_count = self.other_match_value(new_execution)
                    diversity = (self.sorted_values[0] * behavior_len + other_match_count * 1.0) / divisor
        else:
            other_match_count = self.other_match_value(self.execution)
            diversity = (other_match_count * 1.0) / divisor

        return diversity * 100

    def other_match_value(self, exection):
        match_set = set(exection.keys()) & set(self.execution_behaviors)
        return len(match_set)

    def evaluate(self, ind, **kwargs):
        # ind.phenotype will be a xml file. We can parse through the xml file
        # and determine the diversity based on the nodes
        ind.phenotype = ind.phenotype.replace('[','<')
        ind.phenotype = ind.phenotype.replace(']','>')
        ind.phenotype = ind.phenotype.replace('%','"')
        # print (ind.phenotype)
        self.root = ET.fromstring(ind.phenotype)

        self.contro_behaviors = {'Selector', 'Sequence'}
        nodes = []
        self.control = dict()
        self.control['Sequence'] = 0
        self.control['Selector'] = 0
        self.execution = dict()
        for node in self.root.iter():
            if node.tag in ['Sequence', 'Selector']:
                self.control[node.tag] += 1
                nodes.append(node.tag)
            else:
                if node.text.find('_') != -1:
                    node_text = node.text.split('_')
                    node_text = node_text[0]
                else:
                    node_text = node.text
                try:
                    self.execution[node_text] += 1
                except KeyError:
                    self.execution[node_text] = 1
                nodes.append(node_text)

        fitness = self.calcualte_diversity()
        return fitness
