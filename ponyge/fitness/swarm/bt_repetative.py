"""Behavior repetative classes for swarms."""

import math
from ponyge.fitness.base_ff_classes.base_ff import base_ff
import xml.etree.ElementTree as ET


class bt_repetative(base_ff):
    """
    Calculation the fintness of the individual.
    As the objective fitness is not yet avaliable, we calcualte fitness
    based on the repetative structure of the BT evaluated for itself.
    """

    maximise = True  # True as it ever was.

    def __init__(self, parameter):
        # Initialise base fitness function class.
        super().__init__()
        self.execution_behaviors = [
            'MoveTowards', 'Explore', 'CompositeSingleCarry',
            'CompositeDrop', 'MoveAway', 'NeighbourObjects', 'IsDropable',
            'IsCarrying', 'IsVisitedBefore']

        if parameter.params['MULTICARRY'] is True:
            self.execution_behaviors = [
                'MoveTowards', 'Explore', 'CompositeDropPartial',
                'CompositeMultipleCarry', 'IsVisitedBefore', 'MoveAway',
                'IsInPartialAttached', 'NeighbourObjects']

        if parameter.params['COMMUNICATION'] is True:
            self.execution_behaviors += [
                'CompositeDropCue', 'CompositePickCue', 'CompositeSendSignal',
                'CompositeReceiveSignal']

        self.execution_behaviors.sort()

    def calcualte_diversity(self):
        self.sorted_keys = list(self.execution.keys())
        self.sorted_keys.sort()
        counter = 0.0
        three_main_nodes = ['Explore', 'CompositeSingleCarry', 'CompositeDrop']
        for node in three_main_nodes:
            if node in self.sorted_keys:
                counter += 1

        return (counter / 3.0) * 100

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
        depth = 0
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
