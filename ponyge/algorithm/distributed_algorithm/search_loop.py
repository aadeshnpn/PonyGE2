from ponyge.agent.agent import Agent
from ponyge.algorithm.parameters import params
#from fitness.evaluation import evaluate_fitness
from ponyge.stats.stats import stats
#from utilities.stats import trackers
#from operators.initialisation import initialisation
#from utilities.algorithm.initialise_run import pool_init

def create_agents(n,p):
    """
    Create a list of agent specified by n parameter
    """
    return [ Agent(p) for a in range(n) ]


def individuals_from_agents(agents):
    return [agent.individual[0] for agent in agents]

def search_loop():
    """
    This loop is used when the multiagent parameter is passed
    """

    # Create a list of agents based on the paramater passed
    agents = create_agents(params['AGENT_SIZE'], params['INTERACTION_PROBABILITY'])

    # Collect individual state for the first time
    get_stats(individuals_from_agents(agents))

    ##Multi-Agent based GE
    for generation in range(1,(params['GENERATIONS']+1)):
        stats['gen'] = generation
        
        #New generation
        agents = params['STEP'](agents)

        #Gather stats again after step
        get_stats(individuals_from_agents(agents))

    return [agent.individual[0] for agent in agents]