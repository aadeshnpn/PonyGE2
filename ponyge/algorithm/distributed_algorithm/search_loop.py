from ponyge.agent.agent import Agent
# from ponyge.algorithm.parameters import params
# from fitness.evaluation import evaluate_fitness
# from ponyge.stats.stats import stats, get_stats
# from utilities.stats import trackers
# from operators.initialisation import initialisation
# from utilities.algorithm.initialise_run import pool_init


def create_agents(n, p):
    """
    Create a list of agent specified by n parameter
    """
    return [Agent(p) for a in range(n)]


def individuals_from_agents(agents):
    return [agent.individual[0] for agent in agents]


def search_loop(parameter):
    """
    This loop is used when the multiagent parameter is passed
    """

    # Create a list of agents based on the paramater passed
    agents = create_agents(parameter.params['AGENT_SIZE'], parameter.params['INTERACTION_PROBABILITY'])

    # Collect individual state for the first time
    parameter.stats.get_stats(individuals_from_agents(agents))

    # Multi-Agent based GE
    for generation in range(1, (parameter.params['GENERATIONS']+1)):
        parameter.stats.stats['gen'] = generation
        
        # New generation
        agents = parameter.params['STEP'](agents)

        # Gather stats again after step
        parameter.stats.get_stats(individuals_from_agents(agents))

    return [agent.individual[0] for agent in agents]