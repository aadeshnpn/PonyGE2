import numpy as np
import math
import time
import os
import sys
import copy

from joblib import Parallel, delayed
import multiprocessing
import json
from fitness.swarm.agent import Agent
from fitness.swarm.utils.world_objects import *
from fitness.swarm.utils.potentialFields import PotentialField
#from pydge.genetic import Grammar

from fitness.swarm.utils.xml.parseRules import ParseRules
import argparse
import ast
#import random
import pickle


#parser = argparse.ArgumentParser(description = "Evolution run or viewer run")
#parser.add_argument('--viewer',default=False)
#parser.add_argument('--evolution',default=False)
#parser.add_argument('--rules',default="rules/gen_rules.xml")
#parser.add_argument('--rules')

#args = parser.parse_args()
#args.viewer = ast.literal_eval(str(args.viewer))
#args.evolution = ast.literal_eval(str(args.evolution))

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
width = 1600
height = 800
np.random.seed(123)

class Testing:
    def __init__():
        self.r = None


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

"""
All functions used for paralel processing
"""
def create_agents(i):
    #return Agent(i,[width/2+np.random.rand()*10,height/2+np.random.rand()*10])
    #return Agent(i,[np.random.random_integers(-width/2,width/2),np.random.random_integers(-height/2,height/2)])
    return Agent(i,[np.random.random()*30,np.random.random()*30])

def get_agent_dict(agent):
    agent_dict = {}
    agent_dict["x"] = agent.location[0]
    agent_dict["y"] = agent.location[1]
    agent_dict["id"] = agent.name
    agent_dict["direction"] = agent.direction
    agent_dict["state"] = list(agent.current_behaviors)[0]
    ##Signal json
    if agent.signal.grid:
        agent_dict["signal"] = 1
        agent_dict["signal_radius"] = 40
    else:
        agent_dict["signal"] = 0
        agent_dict["signal_radius"] = 0
    #eprint (agent.signal.location)
    return agent_dict    
    
def world_objects_to_json(pobjects):
    #objects = []
    #for i in pobjects:
        #print (hub)
    object_temp = {}
    object_temp["x"] = pobjects.location[0]
    object_temp["y"] = pobjects.location[1]
    object_temp["radius"] = pobjects.radius
    try:
        object_temp["q_value"] = pobjects.q_value
    except:
        pass
    #objects.append(object_temp)
    return object_temp

def random_walk(i):
    #i.direction = np.random.random() * (2*np.pi)
    #i.direction = np.random.uniform(0,2*np.pi)
    i.location[0] = i.location[0] + np.cos(i.direction) * 2
    i.location[1] = i.location[1] + np.sin(i.direction) * 2
    #i.location = check_s(i.location)
    #print (i.location)
    return i

class Environment:
    def __init__(self,width=1600,height=800,position=(0,0),grid_size=10,name='env',rules_stream=None):
        self.width = width
        self.height = height
        self.x_limit = width/2
        self.y_limit = height/2
        self.grid_size = grid_size
        self.agents = {}
        self.filename = os.path.join(ROOT_DIR, "world.json")
        #self.grammar_filename = os.path.join(ROOT_DIR,"pydge/grammars/task_partitioning.bnf")
        #self.grammar_filename = os.path.join(ROOT_DIR,"pydge/grammars/letter.bnf")
        #self.grammar = Grammar(self.grammar_filename)
        self.hub = {}
        self.sites = {}
        self.obstacles = {}
        self.traps = {}
        self.rough = {}
        self.cues = {}
        self.food = {}
        self.draw_food = {}
        self.cue_id = 1
        self.food_id = 0
        #self.obstacles = None
        #self.rules_filename = os.path.join(ROOT_DIR, args.rules)
        self.rules_stream = self.xml_filter(rules_stream)
        self.rules = []
        self.fitness = 0
        self.potential_fields = []
        self.signal_radius = 40
        self.cue_radius = 10
        self.GEVA = True

        if self.width % self.grid_size != 0 or self.height % self.grid_size != 0:
            print ("grid size invalid")
            exit(1)
        self.grid = {}
        self.grid_objects = {}   
        #list_xcords = np.arange(0,self.width,self.grid_size).tolist() 
        #list_ycords = np.arange(0,self.height,self.grid_size).tolist()
        list_xcords = np.arange(-self.width/2,self.width/2,self.grid_size).tolist() 
        list_ycords = np.arange(-self.height/2,self.height/2,self.grid_size).tolist()
        i = 1
        for ycord in list_ycords:
            for xcord in list_xcords:
                x1 = xcord; y1 = ycord; x2 = xcord+self.grid_size; y2 = ycord+self.grid_size
                self.grid[(x1,y1),(x2,y2)] = i
                self.grid_objects[i] = []
                i += 1
        self.grid_len = i - 1
        

    def xml_filter(self,output):
        #print (type(output))
        output = output.replace('[','<')
        output = output.replace('/]','/>')
        output = output.replace(']','>')
        output = output.replace('%','"')
        return output


    def parse_grammar(self, filename, xmlstring = None):
        p1 = ParseRules(filename,xmlstring)
        rules = p1.convert()
        i = 0
        rules_list = []
        for rule in rules:
            r1 = Rules(i,rule[0],rule[1],rule[2])
            #print (rule[0]['behaviors'])
            #self.rules.append(r1)
            rules_list.append(r1)
            i += 1
        #print (self.rules[0].behaviours)
        if xmlstring:
            return rules_list
        else:
            self.rules = rules_list
        """                    
        p1 = ParseRules(filename,xmlstring)
        rules = p1.convert()
        i = 0
        rules_list = []
        for rule in rules:
            r1 = Rules(i,rule)
            rules_list.append(r1)
            i += 1
        if xmlstring:
            return rules_list
        else:
            self.rules = rules_list
            return self.rules
        """
    def build_json_environment(self):
        json_data = open(self.filename).read()

        data = json.loads(json_data)
        #Uncomment this to randomize sites
        #generator = worldGenerator()
        #js = generator.to_json()
        #data = json.loads(js)

        #self.x_limit = data["dimensions"]["x_length"] / 2
        #self.y_limit = data["dimensions"]["y_length"] / 2
        #self.hub = data["hub"]
        i = 0
        #print (data["hub"])
        for hub in data["hub"]:
            self.hub[i] = Hub(i,(hub["x"],hub["y"]),hub["radius"])
            self.hub[i].grid = self.get_adjcent_grid(self.hub[i].location,self.hub[i].radius)
            for grid in self.hub[i].grid:
                self.grid_objects[grid].append(self.hub[i]) # = self.hub[i]
            i += 1
        self.required_distance = np.sqrt((self.hub[0].location[0]-600)**2 + (self.hub[0].location[1]-400)**2)            
        for site in data["sites"]:
            self.sites[i] = Sites(i,(site["x"],site["y"]),site["radius"],site["q_value"])
            self.sites[i].grid = self.get_adjcent_grid(self.sites[i].location,self.sites[i].radius)
            for grid in self.sites[i].grid:
                self.grid_objects[grid].append(self.sites[i]) # = self.hub[i]
            i += 1
        for obstacle in data["obstacles"]:
            self.obstacles[i] = Obstacles(i,(obstacle["x"],obstacle["y"]),obstacle["radius"])
            self.obstacles[i].potential_field = self.create_potential_field(self.obstacles[i].location,self.obstacles[i].radius)
            self.obstacles[i].grid = self.get_adjcent_grid(self.obstacles[i].location,self.obstacles[i].radius)
            for grid in self.obstacles[i].grid:
                self.grid_objects[grid].append(self.obstacles[i]) # = self.hub[i]
            i += 1

        for trap in data["traps"]:
            self.traps[i] = Traps(i,(trap["x"],trap["y"]),trap["radius"])
            self.traps[i].grid = self.get_adjcent_grid(self.traps[i].location,self.traps[i].radius)
            for grid in self.traps[i].grid:
                self.grid_objects[grid].append(self.traps[i]) # = self.hub[i]            
            i += 1          
        """      
        ##Draw some obstacles around the nest
        high_cord = np.arange(55,175)
        low_cord = np.arange(-55,-175)
        comb_cord = high_cord.tolist() + low_cord.tolist()
        for i in range(200):
            #xloc = np.random.random()*200*np.random.choice([-1,1]) + self.hub[0].location[0]
            #yloc = np.random.random()*200*np.random.choice([-1,1]) + self.hub[0].location[1]
            #loc = [int(xloc),int(yloc)]            
            x = int(np.random.choice(comb_cord) * np.random.choice([1,-1]))
            y = int(np.random.choice(comb_cord) * np.random.choice([1,-1]))          
            food = self.add_food([x,y])
            self.add_food(food.location,food)
        """

    def create_potential_field(self,location,radius):
        spread = 20  #  What should this be?
        strength = .25  #  Dictates the strength of the field
        return PotentialField(location, radius, spread, strength, type='repulsor')

    def potential_field_sum(self,location):
        dx = 0
        dy = 0
        for field in self.potential_fields:
            delta = field.effect(location)
            dx += delta[0]
            dy += delta[1]
        #  return [0, 0]
        return [dx, dy]        

    def world_objects_to_json(self,pobjects):
        #return Parallel(n_jobs=8)(delayed(world_objects_to_json)(pobjects[i]) for i in pobjects)          
        objects = []
        for i in pobjects:
            object_temp = {}
            object_temp["x"] = pobjects[i].location[0]
            object_temp["y"] = pobjects[i].location[1]
            object_temp["radius"] = pobjects[i].radius
            try:
                object_temp["q_value"] = pobjects[i].q_value
            except:
                pass
            objects.append(object_temp)
        return objects

    def fitness_function(self):
        fitness_value = 0
        for food in self.food:
            dx = self.food[food].location[0] - self.hub[0].location[0]
            dy = self.food[food].location[1] - self.hub[0].location[1]
            curr_dist = np.sqrt(dx**2 + dy**2)
            if curr_dist > self.required_distance:
                fitness_value += 1
        return fitness_value

    def create_agents(self,i):
        xloc = np.random.random()*100 + self.hub[0].location[0]
        yloc = np.random.random()*100 + self.hub[0].location[1]
        loc = [xloc,yloc]
        grid_key,grid_val = self.findGrid(loc)
        return Agent(i,[xloc,yloc],{grid_key:grid_val},self.rules)

    def add_agents(self,num_agents=100):
        for i in range(num_agents):
            #self.agents.append(self.create_agents(i))
            self.agents[i] = self.create_agents(i)
            self.grid_objects[list(self.agents[i].grid.values())[0]].append(self.agents[i])
            ##Since the signal is not broadcaseted, the grid is empty
            self.agents[i].signal = Signal(i,self.agents[i].location,self.signal_radius,[]) 
            self.agents[i].rules = self.parse_grammar(None,self.rules_stream)
        #eprint (len(self.agents[0].rules))
        #eprint (self.agents[0].rules[0].behaviours)

    def add_cue(self,location,direction):
        cue_grid = self.get_adjcent_grid(location,self.cue_radius)        
        self.cues[self.cue_id] = Cue(self.cue_id,location,self.cue_radius,cue_grid)
        self.cues[self.cue_id].direction = direction
        for grid in cue_grid:
            self.grid_objects[grid].append(self.cues[self.cue_id])
        self.cue_id += 1

    def add_food(self,location,food = None):
        _,food_grid = self.findGrid(location)        
        if food is None:
            self.food_id += 1            
            self.food[self.food_id] = Food(self.food_id,location,2,food_grid)
            return self.food[self.food_id]
        else:
            food.location = location
            self.grid_objects[food_grid].append(food)
            self.draw_food[food.id] = food

    def remove_food(self,location,food):
        #eprint (location,food)
        _,food_grid = self.findGrid(location)   
        #eprint (self.grid_objects[food_grid])             
        self.grid_objects[food_grid].remove(food)
        self.draw_food.pop(food.id)


    def modify_points(self,point):
        x,y = point[0],point[1]
        if point[0] % self.grid_size == 0:
            x = point[0] + 1
        if point[1] % self.grid_size == 0:
            y = point[1] + 1  
        return (x,y)

    def find_lowerbound(self,point):
        point = self.modify_points(point)
        #print ('lb',point)
        return ((point[0] // self.grid_size) * self.grid_size, (point[1] // self.grid_size) * self.grid_size)

    def find_upperbound(self,point):
        point = self.modify_points(point)        
        #print ('ub',point)
        return (math.ceil(point[0] / self.grid_size) * self.grid_size, math.ceil(point[1] / self.grid_size) * self.grid_size)        
    
    def findGrid(self,point):
        grid_key = (self.find_lowerbound(point),self.find_upperbound(point))
        #eprint (grid_key)
        try:
            return grid_key, self.grid[grid_key]
        except KeyError:
            #print ('Grid not found',grid_key)
            #exit(1)
            return None,None
    
    def get_adjcent_grid(self,point,radius):
        all_grid = []
        center_grid_key,center_grid = self.findGrid(point)
        #print ('grid size and radius, point,center_grid',self.grid_size,radius,point,center_grid)
        if self.grid_size > radius:
            return [center_grid]
        else:
            scale = math.ceil(radius/self.grid_size)
            #_,left_grid = self.findGrid((point[0]-radius,point[1]))
            #_,right_grid = self.findGrid((point[0]+radius,point[1]))
            #print (left_grid,right_grid)
            #_,up_grid = self.findGrid((point[0],point[1]+radius)) 
            #_,down_grid = self.findGrid((point[0],point[1]-radius))
            #print (left_grid,right_grid)
            #print (down_grid,up_grid)
            horizontal_grid = list(range(center_grid-scale,center_grid+scale,1))
            width_scale = int(self.width / self.grid_size)
            #print (width_scale)
            vertical_grid = list(range(center_grid-scale*width_scale,center_grid+scale*width_scale,width_scale))
            h_v_grid = []
            for grid in vertical_grid:
                h_v_grid += list(range(grid-scale,grid+scale,1))
            all_grid = h_v_grid + horizontal_grid
            #print (all_grid)
            all_grid = [grid for grid in all_grid if grid > 0 and grid <= self.grid_len]
            #all_grid = horizontal_grid
        return set(all_grid)

    def addAgentGrid(self,grid_key,agent):
        self.grid[grid_key].append(agent)
    #def findAgentsIngrid(self,point)

    def removeAgentGrid(self,grid_key,agent):
        self.grid[grid_key].remove(agent)

    def check_limits(self,i,d):   
        #eprint (i)     
        if i[0] > (width/2):
            #i[0] -=   width
            i[0] = i[0] - (i[0] - self.x_limit) - 2
            d = np.pi + d
        elif i[0] < (width/2)  * -1:
            #i[0] +=   width
            #return np.pi + d
            i[0] = i[0] - (i[0] + self.x_limit) + 2
            d = np.pi + d
        if i[1] > (height/2):
            #i[1] -=  height
            i[1] = i[1] - (i[1] - self.y_limit) - 2
            d = np.pi + d            
            #return np.pi + d
        elif i[1] < (height/2) * -1:
            #i[1] +=  height
            i[1] = i[1] - (i[1] + self.y_limit) + 2
            d = np.pi + d            
            #return np.pi + d
        return (i,d)

    def move_agents(self):
        self.agents = Parallel(n_jobs=8)(delayed(random_walk)(i) for i in self.agents)

    def pack_chromosomes(self,epoch,allUnique=False):
        ##First find the unique chromosomes
        chromosomes = {}        
        if allUnique:
            #unique_chromosome = list({self.agents[i].chromosome.gene.phenotype for i in self.agents})
            for i in self.agents:
                if self.agents[i].chromosome.gene.phenotype not in chromosomes:
                    chromosomes[self.agents[i].chromosome.gene.phenotype] = 0
                chromosomes[self.agents[i].chromosome.gene.phenotype] += 1.0 / len(self.agents)
            #print (unique_chromosome)            
        else:
            ##Only get top 10 chromosomes
            #unique_chromosome = list(set([self.agents[i].chromosome.gene.phenotype for i in self.agents].sort(reverse = True)))
            unique_chromosome = [self.agents[i].chromosome.gene.phenotype for i in self.agents]
            unique_chromosome.sort(reverse=True)
            unique_chromosome = list(set(unique_chromosome))
            proportion_list = [0.3,0.25,0.15,0.08,0.07,0.05,0.04,0.03,0.02,0.01]
            if len(unique_chromosome) > 10:
                unique_chromosome = unique_chromosome[:10]
                for i in range(0,10):
                    chromosomes[unique_chromosome[i]] = proportion_list[i]
            else:
                unique_chromosome = unique_chromosome[:len(unique_chromosome)]
                chrososomes[unique_chromosome[0]] = 0.5
                chrososomes[unique_chromosome[1]] = 0.25                
                chrososomes[unique_chromosome[2]] = 0.15
                chrososomes[unique_chromosome[3]] = 0.10                                

        with open (ROOT_DIR+"/rules/"+str(epoch)+".xml",'wb') as handle:
            pickle.dump(chromosomes,handle,-1)
    
    def unpack_chromosomes(self):
        #pass
        #print (self.rules_filename)
        #with open (self.rules_filename) as handle:
        #    rules = pickle.load(handle)        
        handle = open(self.rules_filename,'rb')
        rules = pickle.load(handle)
        #eprint (rules)
        return rules

    def load_chromosomes(self):
        pass
    #def fitness_check(self):
        #if self.fitness >= self.sites[1].food_unit or 

    def looper(self):
        #logic outsite the environment class
        for i in range(len(self.agents)):
            self.agents[i].limit_check(self)            
            self.agents[i].sense(self)
            self.agents[i].apply_rules()
            #self.agents[i].apply_internal_rules(self)
            
            self.agents[i].apply_actions(self)
            #self.agents[i].avoid_obstacles(self)
            
            ##Genetic
            #self.agents[i].act(self)
            ##Communication
            self.agents[i].move(self)
            
            #if self.cues:
            #    eprint (self.cues,self.cues[1].location)
                #eprint (self.cue_id,len(self.cues))
                #eprint (self.cues[1],self.cues[1].location)

            #eprint(self.food)
            #self.fitness_check(sel)
            #exit()
            #self.agents[i].random_walk(self)
            self.agents[i].update(self)
            #self.agents[i].increment_timestep()
            #self.agents[i].follow(self)
            #self.findGrid(self.agent[i].location)
    """
    def logic(self):
        self.win.draw_visited_grid()        
        self.win.draw_agents()
        #self.move_agents()
        #self.
        self.looper()
        self.win.agents=self.agents
        #self.win.drawFunction()
    """

    def simulator(self,epoch):
        self.frames_per_sec = 120
        ticks = 30000
        while ticks/len(self.agents) > 50 :
            self.looper()
            ticks -= len(self.agents)
        #eprint (int(self.fitness))
        return int(self.fitness)
        
    def to_json(self):
        print(
            json.dumps(
            {
                "type": "update",
                "data":
                {
                    "x_limit"   : self.width/2,
                    "y_limit"   : self.height/2,
                    "hub"       : self.world_objects_to_json(self.hub),
                    "sites"     : self.world_objects_to_json(self.sites),
                    "obstacles" : self.world_objects_to_json(self.obstacles),
                    "traps"     : self.world_objects_to_json(self.traps),
                    "cues"      : self.world_objects_to_json(self.cues),
                    "food"      : self.world_objects_to_json(self.draw_food),
                    #"rough"     : self.rough,
                    #"attractors": list(map(lambda a: a.toJson(), self.attractors)),
                    #"repulsors" : list(map(lambda r: r.toJson(), self.repulsors )),
                    "agents"    : self.agents_to_json(),
                    #"dead_agents": self.dead_agents_to_json(),
                    #"pheromones": self.pheromone_trails_to_json()
                }
            })
        )   


    def agents_to_json(self):
        return Parallel(n_jobs=8)(delayed(get_agent_dict)(self.agents[i]) for i in self.agents)  

        
def main(epoch):
    #global env
    with open('rules/handcoded_rules_chromo.xml', 'r') as f:
        rules_stream = f.read() 
    #print (rules_stream)
    env = Environment(width=width,height=height,rules_stream=rules_stream)
    #print (env.grid)
    env.build_json_environment()
    #env.parse_grammar(os.path.join(ROOT_DIR, args.rules))     
    env.add_agents(150)
    #first_agent = np.random.choice(env.agents)
    #first_agent.information = True
    env.simulator(epoch)


if __name__ == '__main__':
    main(1)

