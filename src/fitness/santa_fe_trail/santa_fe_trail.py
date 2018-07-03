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
    #Fitness function for matching a string. Takes a string and returns
    #fitness. Penalises output that is not the same length as the target.
    #Penalty given to individual string components which do not match ASCII
    #value of target.

    def __init__(self):
        # Initialise base fitness function class.
        super().__init__()
        
        # Set target string.
        self.target = params['TARGET']

    def evaluate(self, ind, **kwargs):
        ant = AntSimulator(600)
        code = ind.phenotype
        routine = ant.build_routine(code)
        ant.run(routine)
        #print (code,'Food eaten',ant.eaten)
        return 90.0/(ant.eaten+1)

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
