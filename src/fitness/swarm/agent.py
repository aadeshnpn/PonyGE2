import numpy as np
import copy
from enum import Enum
from fitness.swarm.utils.geomUtils import *
import sys
from fitness.swarm.utils.world_objects import *
#from pydge.genetic import *
import ast
from operator import itemgetter

#behavior = Enum('behavior', 'RANDOM_WALK GO_TO_SOURCE GO_TO_NEST')
#action = Enum('action','DO_NOTHING CHANGE_BEHAVIOR SET_INTERNAL_VARIABLE')        

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

class Agent:
    def __init__(self,name,location=[0,0],grid=1,rules=None,grammar=None):
        self.name = name
        #eprint (self.chromosome.gene.phenotype)
        self.location = location
        self.grid = grid #{'Default':[1]}
        self.direction = np.random.random() * (2*np.pi)
        self.following = {}
        self.grid_change = True
        self.temp_grid = None
        self.information = False
        #self.food_unit = 0
        self.food = None 
        self.current_behaviors = {'RANDOM_WALK','PICK_CUES','RECEIVE_SIGNALS'} #,'GO_TO_SOURCE','SEND_SIGNALS','DROP_CUES','PICK_CUES','RECEIVE_SIGNALS'}
        self.rules = rules
        self.hub = 0
        self.site = None
        self.active_rule = []
        self.active_internal_state = []
        self.obstacle = None
        self.velocity = 10
        self.timestep_threshold = 500
        self.signal = None 
        self.environment_signals = None
        self.environment_cue = None
        self.environment_food = None
        self.environment_agents = None
        self.move_behaviour = True

        ##Pre-conditions
        self.HAS_FOOD = False
        self.ON_NEST = True
        self.ON_GRASS = False
        self.ON_SOURCE = False
        self.ON_FOOD = False
        self.ON_AGENTS = False
        self.GOT_STUCK = False
        self.STAY_UP = 0.5
        self.SAW_RED = False
        self.ON_SLOPE = False
        self.STAY_DOWN = 0.5
        self.DROP_FOOD = True
        self.NO_PRECONDITION = True
        self.GIONNI_TP = False
        self.WANT_FOOD = True

        self.SEND_SIGNALS = False
        self.RECEIVE_SIGNALS = False
        self.PUT_CUES = False
        self.GET_CUES = False

        self.ON_SIGNAL = False
        self.ON_CUE = False
        ##Other preconditions
        self.ON_AREA = False
        self.SEES_OBSTACLE = False
        self.IS_CLOSE_TO = False

        self.precondition_dict = {
            'HAS_FOOD':self.get_has_food,
            'ON_NEST':self.get_on_nest,
            'ON_GRASS':self.get_on_grass,           
            'ON_SOURCE':self.get_on_source,            
            'GOT_STUCK':self.get_got_stuck,
            'STAY_UP':self.get_stay_up,
            'SAW_RED':self.get_saw_red,
            'ON_SLOPE':self.get_on_slope,
            'STAY_DOWN':self.get_stay_down,
            'DROP_FOOD':self.get_drop_food,
            'NO_PRECONDITION':self.get_default,
            'GIONNI_TP':self.get_default,
            'WANT_FOOD':self.get_want_food,
            'ON_SIGNALS':self.get_signals,
            'ON_CUE':self.get_cues
            #'SEND_SIGNALS':self.get_send_signals,
            #'RECEIVE_SIGNALS':self.get_receive_signals,
            #'PUT_CUES':self.get_put_cues,
            #'GET_CUES':self.get_cues
        }
        
        self.internal_state_dict ={
            'DROP_FOOD':self.set_drop_food,
            #'STAY_DOWN_MOTIVATION':self.set_stay_down_motivated,
            #'STAY_UP_MOTIVATION':self.set_stay_up_motivated,
            'WANT_FOOD':self.set_want_food,
            #'STAY_DOWN':self.set_stay_down,
            #'STAY_UP':self.set_stay_up
        }
        self.internal_state_app = {
            'DROP_FOOD':self.do_drop_food,
            'WANT_FOOD':self.do_want_food
        }
        self.actions = {
            'RANDOM_WALK':self.random_walk,
            'GO_TO_NEST':self.go_to_nest,
            'GO_TO_SOURCE':self.go_to_source,
            'DROP_CUES':self.drop_cues,
            'PICK_CUES':self.pick_cues,
            'SEND_SIGNALS':self.send_signals,
            'RECEIVE_SIGNALS':self.receive_signals
        }
        ##Internal state
        self.is_drop_food = False
        self.is_stay_down_motivated = True
        self.is_stay_up_motivated = True
        self.is_want_food = True
        self.is_stay_down = False
        self.is_stay_up = False
        self.SEE_CUE = False
        self.SEE_SIGNAL = False
        #self.behaviour = {0:}
        #self.health = 

    def increment_timestep(self):
        if self.genetic_mode:
            self.timestep += 1

    def get_default(self):
        return False

    def set_drop_food(self,value):
        self.is_drop_food = value
    
    def set_stay_down_motivated(self,operation,value):
        self.is_stay_down_motivated = np.abs(self.is_stay_down_motivated * operation + value)
    
    def set_stay_up_motivated(self,operation,value):
        self.is_stay_up_motivated = np.abs(self.is_stay_up_motivated * operation + value)

    def set_want_food(self,value):
        #self.is_want_food = np.abs(self.is_want_food * operation + value)
        self.is_want_food = value

    def set_stay_down(self,operation,value):
        self.is_stay_down = np.abs(self.is_stay_down * operation + value)
    
    def set_stay_up(self,operation,value):
        self.is_stay_up = np.abs(self.is_stay_up * operation + value)        

    def get_has_food(self):
        return self.HAS_FOOD
    
    def get_on_nest(self):
        return self.ON_NEST
    
    def get_on_grass(self):
        return self.ON_GRASS
    
    def get_on_source(self):
        return self.ON_SOURCE    
    
    def get_got_stuck(self):
        return self.GOT_STUCK
    
    def get_stay_up(self):
        return self.STAY_UP
    
    def get_saw_red(self):
        return self.SAW_RED

    def get_on_slope(self):
        return self.ON_SLOPE
    
    def get_stay_down(self):
        return self.STAY_DOWN

    def get_drop_food(self):
        return self.DROP_FOOD

    def get_want_food(self):
        return self.WANT_FOOD

    def get_signals(self):
        return self.SEE_SIGNAL

    def get_cues(self):
        return self.SEE_CUE
    #def get_send_signals(self):
    #    return self.SEND_SIGNALS

    #def get_receive_signals(self):
    #    return self.RECEIVE_SIGNALS

    #def get_put_cues(self):
    #    return self.PUT_CUES

    #def get_cues(self):
    #    return self.GET_CUES

    ##Time for rules check
    def apply_rules(self):
        #print (self.rules)
        #print (self.current_behaviors)
        i = 0
        self.active_rule = {}
        for rule in self.rules:
            ##First check for the behaviours match with the rule before procedding
            ##This constraint is define in paper
            #print (rule.behaviours,rule.preconditions,rule.actions)
            precondition_met = True
            if not self.current_behaviors.isdisjoint(rule.behaviours):
                ##Since this rule behavirous matches with the current behavior. 
                ##Check if the preconditions are satisfied
                #print (i,rule.preconditions)
                for precondition in rule.preconditions:
                    #print (precondition, precondition_met)
                    if precondition_met:
                        #print (self.precondition_dict[precondition[0]](), precondition[2])                        
                        if precondition[1] == '>':
                            if not self.precondition_dict[precondition[0]]() > float(precondition[2]):
                                precondition_met = False
                                #print (self.precondition_dict[precondition[0]](), precondition[2])
                        elif precondition[1] == '<=':                        
                            if not self.precondition_dict[precondition[0]]() <= float(precondition[2]):
                                precondition_met = False
                                #print (self.precondition_dict[precondition[0]](), precondition[2])
                        else:
                            #print (self.precondition_dict[precondition[0]](), eval(precondition[2]))
                            if not self.precondition_dict[precondition[0]]() is eval(precondition[2]):
                                precondition_met = False
                        #print (precondition_met)
                                #print (self.precondition_dict[precondition[0]](), bool(precondition[2]))                        
                            #self.HAS_FOOD = 9
                        #if precondition[0] is bool(precondition[2]):
                        #    print (precondition)
                if precondition_met:
                    for action in rule.actions:
                        if action[0] == 'AB':
                            if action[1] > np.random.random():
                                #self.action[2]()
                                #print (i,action[2],'Done')
                                #self.active_rule.append(action[2])
                                if action[2] not in self.active_rule:
                                    self.active_rule[action[2]] = 0
                                self.active_rule[action[2]] += 1
                            #else:
                            #    print (i,action[2],'failed')
                        else:
                            if action[1] > np.random.random():
                                if action[2] == 0:
                                    #print (bool(action[4]))
                                    #print (action)
                                    self.internal_state_dict[action[3]](ast.literal_eval(action[4]))
                                    self.active_internal_state.append(action[3])
                                    #print (self.is_drop_food)
                                else:
                                    self.internal_state_dict[action[3]](action[2],action[4])                                    
                                    #print (action)
                    
            i += 1
            #print (rule.actions)            
        #exit(1)
    ### Actions
    def apply_internal_rules(self,environment):
        for state in self.active_internal_state:
            #if 0.5 > np.random.random():
            #    self.internal_state_app['DROP_FOOD'](environment)
            #self.internal_state_app['WANT_FOOD'](environment)
            self.internal_state_app[state](environment)

    def apply_actions(self,environment):
        #eprint ('Apply action',self.active_rule)
        #eprint (self.name,self.active_rule,self.HAS_FOOD,self.STAY_UP,self.ON_SOURCE,self.ON_NEST)
        ##First run preconditions
        #eprint (self.active_rule)
        #self.actions['RANDOM_WALK'](environment)
        #self.actions['PICK_CUES'](environment)
        #self.actions['RECEIVE_SIGNALS'](environment)
        #action = sorted(self.active_rule.items(),key=itemgetter(1),reverse=True)[0][0]
        action = set(self.active_rule.items())#sorted(self.active_rule.items(),key=itemgetter(1),reverse=True)[0][0]
        #eprint ('Apply actions',self.name,action)
        if len(action) == 1:
            action = list(action)[0][0]
        elif len(action) > 1:
            action = sorted(self.active_rule.items(),key=itemgetter(1),reverse=True)[1][0]  
        else:
            return
        self.current_behaviors = set()
        #eprint (self.name,action,self.location)
        self.actions[action](environment)
        self.current_behaviors.add(action)
        #for action in self.active_rule:
            #print (action)
            #self.actions['RANDOM_WALK'](environment)
        #    self.actions[action](environment)
        #    self.current_behaviors.add(action)
            #self.actions['SEND_SIGNALS'](environment)
            #self.actions['RECEIVE_SIGNALS'](environment)
            #self.actions['DROP_CUES'](environment)

            
    def do_drop_food(self,environment):
        ##Drop food on to environment
        #eprint (self.ON_SOURCE)
        if self.food and self.HAS_FOOD and not self.ON_SOURCE:
            self.HAS_FOOD = False
            #environment.remove_food(self.location,self.food)
            environment.add_food(copy.copy(self.location),self.food)
            #eprint ("Drop food",self.name)

    def do_want_food(self,environment):
        ##Drop food on to environment
        if not self.HAS_FOOD and self.ON_FOOD:
            #eprint ('want food',self.name)
            self.HAS_FOOD = True
            environment.remove_food(self.location,self.environment_food)
            self.food = self.environment_food
            #environment.add_food(copy.copy(self.location),self.food)

    def no_action(self):
        pass
    
    def change_behaviour(self,new_behaviour):
        self.current_behaviours = new_behaviour
    
    def set_internal_variable(self,internal_variable,value,prob):
        if prob > np.random.random():
            self.internal_variable = value

    ##Definiation of all preconditions
    
    def grid_location(self,width,height):
        return [self.location[0]+width/2,self.location[1]+height/2]        

    def see_obstacles(self,environment):
        pass

    def sense(self,environment):
        grid_key,grid_values = environment.findGrid(self.location)
        new_grid = {grid_key:grid_values}
        #eprint ("new grid",new_grid,self.grid)
        #grid_cord=list(self.grid.keys())[0]
        #print (grid_cord[0])
        if self.grid == new_grid:
            self.grid_change = False
        else:
            #print (self.name,self.grid,self.temp_grid)
            self.grid_change = True
            self.temp_grid = new_grid
            ##Remove all the sense objects from previous grid
            for i in self.grid:
                #self.grid[i].remove(self.signal)
                try:
                    environment.grid_objects[self.grid[i]].remove(self.signal)
                except:
                    pass
        #self.on_nest(grid_values,environment)            
        #print (self.ON_NEST,grid_values,environment.hub[0].grid)
        #exit(0)
        ##Sense the environment
        self.on_source(grid_values,environment)
        self.on_nest(grid_values,environment)
        self.on_obstacles(grid_values,environment)
        self.on_signal(grid_values,environment)
        self.on_cue(grid_values,environment)
        #self.on_food(grid_values,environment)
        #eprint (self.name,self.current_behaviors)
        #if self.genetic_mode:
        #    self.on_agents(grid_values,environment)
    

    def act(self,environment):
        if self.genetic_mode and self.ON_AGENTS:
            #self.chromosome_stack += [{'chromosome':self.chromosome,'fitness':self.chromosome.gene.fitness}] + [ {'chromosome':agent.chromosome,'fitness':agent.chromosome.gene.fitness} for agent in self.environment_agents ]
            self.chromosome_stack += [self.chromosome] + [ agent.chromosome for agent in self.environment_agents ]
            #print (self.chromosome_stack)
            if self.timestep % self.timestep_threshold == 0:            
                if self.best_ever is None:
                    self.best_ever = self.chromosome
                best_ever = max(self.chromosome_stack)
                #individuals.sort(reverse = True)
                #self.chromosome_stack = sorted(self.chromosome_stack,key=itemgetter('fitness'),reverse=True)
                self.chromosome_stack.sort(reverse = True)
                #new_pop = []
                #while len(new_pop) < 2:
                new_pop = self.chromosome.gene.onepoint_crossover(best_ever,self.chromosome_stack[1])
                new_pop = self.chromosome.gene.int_flip_mutation(new_pop)
                new_pop = Chromosome(Genetics(self.chromosome.gene.grammar,fitness_function=ForagingFitness()),new_pop)
                    #agent_list= Agent(Genetics(self.gene.grammar),pop)
                #print (agent_list)
                #for agent in agent_list:
                    ##Fitness function call for swarm
                #    agent.gene.eval_fitness(agent)  
                    ##Fitness function call for stringmatch
                    #agent.gene.eval_fitness(agent)
                #new_pop = self.chromosome.gene.generational_replacement(agent_list,individuals)
                #parents = self.chromosome.gene.tournament_selection(new_pop)
                #print (parents)
                self.best_ever = max(self.best_ever,best_ever)
                self.chromosome_stack.pop()
                self.timestep = 0
                self.food_collected = 0                
                if random.random() > 0.8:
                    #self.best_ever
                    self.best_ever = new_pop


    def on_agents(self,grid_value,environment):
        agent_objects = list(filter(lambda x : type(x).__name__ == 'Agent',environment.grid_objects[grid_value]))
        if agent_objects:
            self.environment_agents = agent_objects
            self.ON_AGENTS = True
        else:
            self.ON_AGENTS = False

    def ON_GRASS(self):
        return False

    def on_source(self,grid_value,environment):
        site_objects = list(filter(lambda x : type(x).__name__ == 'Sites',environment.grid_objects[grid_value]))
        #eprint (self.location,grid_value,environment.sites[1].grid)
        if site_objects:
            self.ON_SOURCE = True
            self.site = site_objects[0].id
            #self.signal.sites = self.site
            #self.food_unit = 1
            #self.HAS_FOOD = True
            self.carry_food(environment)
            #environment.sites[i].food_unit -= 1
            #eprint (self.signal.sites)
            #exit(1)
            #break
        else:
            self.ON_SOURCE = False
            #self.site = None

    def on_nest(self,grid_value,environment):
        #for i in environment.hub:
        if list(filter(lambda x : type(x).__name__ == 'Hub',environment.grid_objects[grid_value])):
        #if grid_value in environment.hub[self.hub].grid:
            self.ON_NEST = True            
            #if self.HAS_FOOD:
            self.deposite_food(environment)
            #self.DROP_FOOD = True
            #self.HAS_FOOD = False
        else:
            self.ON_NEST = False
    
    def on_obstacles(self,grid_value,environment):
        obstacles_objects = list(filter(lambda x : type(x).__name__ == 'Obstacles',environment.grid_objects[grid_value]))      
        if obstacles_objects:
            self.SEES_OBSTACLE = True
            self.obstacle = obstacles_objects[0]
        else:
            self.SEES_OBSTACLE = False
            self.velocity = 25

    def on_signal(self,grid_value,environment):
        signal_objects = list(filter(lambda x : type(x).__name__ == 'Signal',environment.grid_objects[grid_value]))
        if signal_objects:
            self.SEE_SIGNAL = True
            self.environment_signals = signal_objects[0]
        else:
            self.SEE_SIGNAL = False

    def on_cue(self,grid_value,environment):
        cue_objects = list(filter(lambda x : type(x).__name__ == 'Cue',environment.grid_objects[grid_value]))
        if cue_objects:
            #eprint (self.name,grid_value)            
            #eprint ('see cue')
            self.SEE_CUE = True
            self.environment_cue = cue_objects
        else:
            self.SEE_CUE = False
            #self.environment_cue = None

    def on_food(self,grid_value,environment):
        food_objects = list(filter(lambda x : type(x).__name__ == 'Food',environment.grid_objects[grid_value]))
        if food_objects:
            #eprint ('see cue')
            self.ON_FOOD = True
            self.environment_food = food_objects[0]
        else:
            self.ON_FOOD = False                     

    def carry_food(self,environment):
        if not self.HAS_FOOD:
            environment.sites[self.site].food_unit -= 1
            environment.sites[self.site].radius -= 0.1
            self.HAS_FOOD = True
            self.food = environment.add_food(self.location)
            #self.food_unit = 1

    def deposite_food(self,environment):
        if self.HAS_FOOD and 'GO_TO_NEST' in self.current_behaviors:
            environment.fitness += 1
            self.DROP_FOOD = True
            self.HAS_FOOD = False
            if self.genetic_mode:
                self.food_collected += 1
            #eprint (self.name,self.location,self.food)
            ##Destroy food object
            del self.food
            self.food = None
            #eprint (self.name,"food deposited")            
            #environment.remove_food(self.location,self.food)
            #self.

    def drop_food(self,environment):
        self.food_unit = 0
    
    #Default behaviours
    def random_walk(self,environment):
        ##Random walk only towards 1st and 4th quadrant
        #self.move_behaviour = True
        #if 0.5 > np.random.random():
        #   self.direction = np.random.uniform(3*np.pi/2,2*np.pi) #* (2*np.pi)
        #else:
        #    self.direction = np.random.uniform(0,np.pi/2) #* (2*np.pi)
        #self.direction = np.random.random() * (2*np.pi)
        #eprint ("From random walk",self.direction)
        ##Random walk can only change direction in limited way
        #self.direction = np.random.uniform(0,np.pi*2) #* (2*np.pi)        
        #self.direction = np.random.uniform(self.direction,-np.pi/4) + np.random.uniform(self.direction,np.pi/4)
        delta_d = np.random.normal(0, .1)
        self.direction = (self.direction + delta_d) % (2 * np.pi)
        
    def go_to_nest(self,environment):
        #print (environment.hub[self.hub].location)
        #self.move_behaviour = True
        ##            def follow(self,environment):
        if self.following is None:
            list_agents = self.grid[list(self.grid.keys())[0]]
            #list_agents = list_agents[1:]
            #print (self.name,list_agents)
            #print (len(list_agents)-1)
            if len(list_agents) > 2:
                #list_agents.remove(list_agents[0])
                #choice_list = [a for a in list_agents if a != self]
                #list_agents.pop(self)
                #print (list_agents)
                random_agent = np.random.choice(list_agents)
                #print (self.name,random_agent)
                if type(random_agent) is int or random_agent == self:
                    self.following = None
                else:
                    self.following = random_agent
                    #Information is flowed very fast
                    if self.information:
                        if 0.5 > np.random.random():
                            random_agent.information = self.information
                    if random_agent.information:
                        if 0.5 > np.random.random():
                            self.information = random_agent.information
                    #if random_agent.information is not None:# and self.information is None:
                    #    self.information = random_agent.information
            
        else:
            #if self.name == 1:
                #print (self.name,self.following.name)
            self.direction = self.following.direction
        
        #pass
        #if agent
        #pass

        self.direction = get_direction(environment.hub[self.hub].location,self.location)
        if self.site:
            self.send_signals(environment)                        

    def go_to_source(self,environment):
        #print (environment.sites[self.site])
        #self.move_behaviour = True        
        if self.site:
            self.drop_cues(environment)        
            self.direction = get_direction(environment.sites[self.site].location,self.location)

    #There are communication behaviours. They will be executed by apply actions
    def drop_cues(self,environment):
        #eprint ("Drop Cues",self.name,self.location)
        #self.move_behaviour = True   
        if not self.ON_SOURCE and not self.ON_NEST:
            environment.add_cue(copy.copy(self.location),copy.copy(self.direction))
    
    def pick_cues(self,environment):
        if self.SEE_CUE and self.environment_cue:
            #eprint (self.name)
            #self.direction = sum(cue.direction for cue in self.environment_cue) / len(self.environment_cue)
            #self.velocity = sum(cue.velocity for cue in self.environment_cue) / len(self.environment_cue)
            self.direction = self.environment_cue[0].direction #/ len(self.environment_cue)
            self.velocity = self.environment_cue[0].velocity
            #eprint ('after cue calculation',self.environment_cue[0].direction,self.direction,self.velocity)
            #self.location = [0,0]
        #pass
    
    ##These signals move with the agents.
    ##These signals are distributed across some radi    def follow(self,environment):
        if self.following is None:
            list_agents = self.grid[list(self.grid.keys())[0]]
            #list_agents = list_agents[1:]
            #print (self.name,list_agents)
            #print (len(list_agents)-1)
            if len(list_agents) > 2:
                #list_agents.remove(list_agents[0])
                #choice_list = [a for a in list_agents if a != self]
                #list_agents.pop(self)
                #print (list_agents)
                random_agent = np.random.choice(list_agents)
                #print (self.name,random_agent)
                if type(random_agent) is int or random_agent == self:
                    self.following = None
                else:
                    self.following = random_agent
                    #Information is flowed very fast
                    if self.information:
                        if 0.5 > np.random.random():
                            random_agent.information = self.information
                    if random_agent.information:
                        if 0.5 > np.random.random():
                            self.information = random_agent.information
                    #if random_agent.information is not None:# and self.information is None:
                    #    self.information = random_agent.information
            
        else:
            #if self.name == 1:
                #print (self.name,self.following.name)
            self.direction = self.following.direction
        

    ##For now lets only broadcast, the site information, the direction it is headed
    def send_signals(self,environment):
        self.signal.grid = environment.get_adjcent_grid(self.location,environment.signal_radius)
        #print (self.location,self.signal.grid)
        for grid in self.signal.grid:
            if self.signal not in environment.grid_objects[grid]:
                environment.grid_objects[grid].append(self.signal)
        self.signal.direction = self.direction
        #pass

    def receive_signals(self,environment):
        if self.SEE_SIGNAL and self.environment_signals:
            self.site = self.environment_signals.site
            self.direction = self.environment_signals.direction
        pass
    
    def avoid_obstacles(self,environment):
        if self.SEES_OBSTACLE:
            #print (self.location,self.obstacle.potential_field.location)
            delta = self.obstacle.potential_field.effect(self.location)
            self.direction = np.arctan2(delta[1], delta[0])
            self.velocity= np.sqrt(delta[0] ** 2 + delta[1] ** 2)
            
    def move(self,environment):
        #if self.following is None:
        #self.random_walk()
        if self.move_behaviour:
            #eprint (self.direction)
            self.location[0] = self.location[0] + np.cos(self.direction) * self.velocity
            #if self.location[0] > environment.x_limit:
            #        self.location[0] = self.location[0] - (self.location[0] - environment.x_limit) - 2
            #elif
            self.location[1] = self.location[1] + np.sin(self.direction) * self.velocity
            #self.move_behaviour = False
        #if environment.cues:
        #    eprint("From move",self.name,environment.cues[1].location,self.location)
    
    def limit_check(self,environment):
        ##In this environemnt we don't want them to appear from another end but repulse the environment
        #self.location = environment.check_limits(self.location) 
        self.location,self.direction = environment.check_limits(self.location,self.direction)
        #environment.find_grid(self.location) 
    
    def update(self,environment):
        if self.grid_change and None not in self.temp_grid.keys():
            #if self.grid != {'Default':[1]}:
            #environment.removeAgentGrid(list(self.grid.keys())[0],self)
            #print (list(self.grid.keys())[0])
            #print (self.grid,self.temp_grid)            
            #print (environment.grid_objects[list(self.grid.values())[0]])
            environment.grid_objects[list(self.grid.values())[0]].remove(self)
            #eprint ("grid change",self.temp_grid)
            self.grid = self.temp_grid
            environment.grid_objects[list(self.grid.values())[0]].append(self)
            #environment.addAgentGrid(list(self.grid.keys())[0],self)
        self.environment_cue = None
        self.environment_signal = None            
