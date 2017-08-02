class Hub:
    def __init__(self,id=1,location=(0,0),radius=20,grid=[1]):
        self.id = id
        self.location = location
        self.radius = radius
        self.grid = grid
        self.carryable = False

class Sites:
    def __init__(self,id=1,location=(0,0),radius=20,q_value=0.5,grid=[1]):
        self.id = id
        self.location = location
        self.radius = radius
        self.q_value = q_value
        self.food_unit = self.q_value * 1000
        self.grid = grid
        self.carryable = False        

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
        self.carrable = False

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
        self.carryable = False        
        #self.potential_field = None        

class Cue:
    def __init__(self,id=1,location=(0,0),radius=20, grid=[1]):
        self.id = id
        self.location = location
        self.radius = radius
        self.grid = grid
        ##Communication parameter for cue
        self.velocity = 5
        self.direction = 0
        self.carryable = False        
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
        self.carryable = False        

class Rules:
    def __init__ (self,id=1,json_data=None):
        self.id = id
        #self.behaviours = behaviours
        #self.preconditions = preconditions
        #self.actions = actions
        #print (json_data[0])
        self.luggage = Luggage(id,json_data[0]['luggage'])
        self.movement = Movement(id,json_data[1]['movement'])
        self.communicate = None

class Luggage:
    def __init__ (self,id=id,luggage_data=None):
        self.luggage_data = luggage_data
        self.carry = Carry(id,self.luggage_data['carry'])
        self.drop = Drop(id,self.luggage_data['drop'])

class Movement:
    def __init__ (self,id=id,movement_data=None):
        self.movement_data = movement_data
        self.conditions = self.movement_data['conditions']
        self.move = self.movement_data['move']
        self.orientation = self.movement_data['orientation']
        #self.carry = Carry(id,self.movement_data['carry'])
        #self.drop = Drop(id,self.movement_data['drop'])
        #print (self.conditions,self.move,self.orientation)

class Carry:
    def __init__ (self,id=id,carry_data=None):
        self.carry_data = carry_data
        self.conditions = self.carry_data[0]
        self.action = self.carry_data[1]
        #print (self.condition,self.action)
class Drop:
    def __init__ (self,id=id,drop_data=None):
        self.drop_data = drop_data
        self.conditions = self.drop_data[0]
        self.action = self.drop_data[1]
        #print (self.conditions,self.action)

class Food:
    def __init__(self,id=1,location=(0,0),radius=2,grid=[1]):
        self.id = id
        self.location = location
        self.radius = radius
        self.grid = grid   
        self.carryable = True 
