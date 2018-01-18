
class Hub:
    def __init__(self,id=1,location=(0,0),radius=20,grid=[1]):
        self.id = id
        self.location = location
        self.radius = radius
        self.grid = grid

class Sites:
    def __init__(self,id=1,location=(0,0),radius=20,q_value=0.5,grid=[1]):
        self.id = id
        self.location = location
        self.radius = radius
        self.q_value = q_value
        self.food_unit = self.q_value * 1000
        self.grid = grid

class Obstacles:
    #Type 1 is circular
    #Type 2 is rectangular
    #Type 3 is square
    def __init__(self,id=1,location=(0,0),radius=20,grid=[1]):
        self.id = id
        self.location = location
        self.radius = radius
        self.grid = grid
        self.potential_field = None

##For now only a single type of signal
class Signal:
    def __init__(self,id=1,location=(0,0),radius=20,grid=[1]):
        self.id = id
        self.location = location
        self.radius = radius
        self.grid = grid
        ##Communication parameters for signal
        self.site = None
        self.direction = 0 
        #self.potential_field = None        

class Cue:
    def __init__(self,id=1,location=(0,0),radius=20, grid=[1]):
        self.id = id
        self.location = location
        self.radius = radius
        self.grid = grid
        self.activity=30
        ##Communication parameter for cue
        self.velocity = 5
        self.direction = 0
        #self.potential_field = None                

class Traps:
    #Type 1 is circular
    #Type 2 is rectangular
    #Type 3 is square
    def __init__(self,id=1,location=(0,0),radius=20,grid=[1]):
        self.id = id
        self.location = location
        self.radius = radius
        self.grid = grid

class Rules:
    
    def __init__ (self,id=1,behaviours=None,preconditions=None,actions=None):
        self.id = id
        self.behaviours = behaviours
        self.preconditions = preconditions
        self.actions = actions

class Food:
    def __init__(self,id=1,location=(0,0),radius=2,grid=[1]):
        self.id = id
        self.location = location
        self.radius = radius
        self.grid = grid    
