"""
Trail class, ant simulator and fitness function for santa fe trail
"""

from algorithm.parameters import params
from fitness.base_ff_classes.base_ff import base_ff
import copy
from os import path
from fitness.swarm.env import Environment
#import pypeg2

"""
Ant simulator to simulate ants in Santa Fe trail environment
"""
    
class swarm(base_ff):
    #Fitness function for matching a string. Takes a string and returns
    #fitness. Penalises output that is not the same length as the target.
    #Penalty given to individual string components which do not match ASCII
    #value of target.

    def __init__(self):
        # Initialise base fitness function class.
        super().__init__()
        
        # Set target string.
        #self.target = params['TARGET']

    def evaluate(self, ind, **kwargs):
        code = ind.phenotype
        print (code)        
        env = Environment(rules_stream=code)
        env.build_json_environment()
        #env.parse_grammar(os.path.join(ROOT_DIR, args.rules))     
        env.add_agents(500)
        #first_agent = np.random.choice(env.agents)
        #first_agent.information = True
        food_collected = env.simulator(epoch) 
        #Maximum food that can be collected from single source is 1000        
        #routine = ant.build_routine(code)
        #print (code,'Food eaten',ant.eaten)
        return 1000/(food_collected)

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
