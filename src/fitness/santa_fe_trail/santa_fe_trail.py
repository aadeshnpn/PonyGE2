"""
Trail class, ant simulator and fitness function for santa fe trail
"""

from algorithm.parameters import params
from fitness.base_ff_classes.base_ff import base_ff
import copy
from os import path
from fitness.santa_fe_trail.gp import AntSimulator
#import pypeg2

"""
Ant simulator to simulate ants in Santa Fe trail environment
"""
    
class santa_fe_trail(base_ff):
    #Fitness function for Santa Fe Trail using Novelty Search

    def __init__(self):
        # Initialise base fitness function class.
        super().__init__()
        
        # Set target string.
        self.target = params['TARGET']
        self.maximise = True

    def evaluate(self, ind, **kwargs):
        ant = AntSimulator(650)
        code = ind.phenotype
        routine = ant.build_routine(code)
        ant.run(routine)
        #print (code,'Food eaten',ant.eaten)
        #return 90.0/(ant.eaten+1)
        #print (ant.eaten, ant.ss_foodeaten)
        return ant.eaten, ant.ss_foodeaten, ant.foodeaten_sequence, ant.step_sequence

##Parsing type

#class Parameter:
#    grammar = name()

#class Parameters(Namespace):
#    grammar = csl(Parameter)

def main():
    ant = AntSimulator(500)
    ant.load_trail()
    sample = 'move(); "if(food_ahead()==1) {"right(); move();"} else {" right(); "}" move(); move();'
    sample = '''
    if food_ahead()==1:
        left()
        move()
    else:
        right()
        move()
    '''
    print (sample)
    ant.run(sample)

if __name__ == '__main__':
    main()
