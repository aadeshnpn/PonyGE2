import sys
import os


class Move:
    def __init__(self,value,condition,orientation):
        self.value = value
        self.condition = condition
        self.orientation = orientation
        self.vocab_value = {'0' : 'RANDOM_WALK', 
                            '1' : 'GO_TO_HUB', 
                            '2' : 'GO_TO_SOURCE',
                            '3' : 'FOLLOW_SIGNAL',
                            '4' : 'FOLLOW_CUE',
                            '5' : 'FOLLOW_OBJECT',
                            '-' : 'DO_NOT_MOVE'
                            }

        self.vocab_condition = {
                            0 : 'WANT_TO_GO_TO_HUB',
                            1 : 'SOURCE_KNOWN',
                            2 : 'SIGNAL_ACTIVE',
                            3 : 'CUE_ACTIVE',
                            4 : 'OBJECT_ACTIVE'
                            }
    
        self.vocab_orientation = {
                            '0' : 'AWAY',
                            '1' : 'TOWARDS'
                            }

        self.move = self.vocab_value[self.value]
        self.conditions = set()
        for i in range(len(self.condition)):
            if self.condition[i] == '1':
                self.conditions.add((self.vocab_condition[i],True))
            elif self.condition[i] == '0':
                self.conditions.add((self.vocab_condition[i],False))                 
        self.orientation = self.vocab_orientation[self.orientation]

    def __str__(self):
        #return self.vocab[self.id]
        #return 'Conditions\n----------\n' + str(self.conditions + ,'move':self.move,'orientation':self.orientation
        readable = '\n\n[Movement:]\n-----------\n[Conditions:]\n'
        for a in self.conditions:
            readable += '\n' + str(a)
        readable += '\n\n[Move:]\n' + str(self.move)
        readable += '\n\n[Orientation:]\n' + str(self.orientation)
        return readable
    
    def to_engine(self):
        return {'movement':{'conditions':self.conditions,'move':self.move,'orientation':self.orientation}}
    
    def __toLatex__(self):
        return '$B_\mathit{' +self.vocab[self.id] +'}$'
  
    def __eq__(self, ob):
        if self.id == ob.id:
            return True
        else:
            return False
        
    def __hash__(self):
        return self.id


class Luggage:
    def __init__(self,carry,drop):
        self.carry = carry
        self.drop = drop
        #print (self.carry,self.drop)
        #self.move = self.vocab_value[self.value]
        self.carry_conditions = set()
        self.drop_conditions = set()

        self.carry_condition = { 0 : 'CARRIABLE_OBJECT',
                                 1 : 'OBJECT_WEIGHT'
                            }

        self.drop_condition = { 0 : 'CARRYING_OBJECT',
                                1 : 'ON_OTHER_OBJECT',
                                2 : 'ON_OTHER_AGENT',
                                3 : 'ON_NEST'
                        }
        self.carry_value = { '0' : 'NO_CARRY',
        '1' : 'CARRY',
        '-' : 'None'
        }

        self.drop_value = { '0' : 'DROP_ON_OTHER_OBJECT',
                            '1' : 'DROP_ON_OTHER_AGENT',
                            '2' : 'DROP_ON_NEST',
                            '-' : 'None'
        }

        for i in range(len(self.carry[0])):
            #print (self.carry[0][i])
            if self.carry[0][i] == '1':
               self.carry_conditions.add((self.carry_condition[i],True))               
            elif self.carry[0][i] == '0':
               self.carry_conditions.add((self.carry_condition[i],False))
        self.carryval = self.carry_value[self.carry[1]]

        for i in range(len(self.drop[0])):
            #print (self.carry[0][i])
            if self.drop[0][i] == '1':
               self.drop_conditions.add((self.drop_condition[i],True))               
            elif self.drop[0][i] == '0':
               self.drop_conditions.add((self.drop_condition[i],False))
        #print ('Drop value',self.drop_value[self.drop[1]])
        self.dropval = self.drop_value[self.drop[1]]
        #print (self.drop_conditions)


    def __str__(self):
        #return self.vocab[self.id]
        #return 'Conditions\n----------\n' + str(self.conditions + ,'move':self.move,'orientation':self.orientation
        readable = '[Luggage:]\n-----------'
        readable += '\n[Carry:]\n'
        #print (self.carry[1])
        readable += self.carry_value[self.carry[1]]
        #print (self.carry_conditions)
        #print (self.drop_conditions)
        readable += '\n\n[Conditions:]'
        for a in self.carry_conditions:
            readable += '\n' + str(a)
        readable += '\n\n[Drop:]\n'
        readable += self.drop_value[self.drop[1]]        
        readable += '\n\n[Conditions:]'        
        for a in self.drop_conditions:
            readable += '\n' + str(a)
        #print (readable)        
        #readable += '\n\nMove\n-----------\n' + str(self.move)
        #readable += '\n\nOrientation\n---------\n' + str(self.orientation)
        return readable
    
    def to_engine(self):
        #return 'ttt'
        return {'luggage':{'drop':(self.drop_conditions,self.dropval),'carry':(self.carry_conditions,self.carryval)}}

class Rule(object):
    def __init__(self):
        self.luggage = None
        self.movement = None
        self.communication = None
        self.explanation = ''
        self.rule_json = None

    def __str__(self):
        strResult = ''
        return str(self.luggage) + str(self.movement)
        #print ('hello')
        #for len

    def __manual__(self):
        return (self.luggage.to_engine(),self.movement.to_engine())

    def __simplifyActions__(self):
        done = False
        while not done:
            act1ToRemove = None
            act2ToRemove = None
            foundOne = False
            for action1 in self.actions:
                if foundOne:
                    break
                for action2 in self.actions:
                    if not action1 is action2 and action1.__sameButProbability__(action2):
                        act1ToRemove = action1
                        act2ToRemove = action2
                        done = False
                        foundOne = True
                        break
            if foundOne:
                #print('Modifying action: '+ str(act1ToRemove))
                act1ToRemove.prob = 1 - ((1 - act1ToRemove.prob) * (1 - act2ToRemove.prob))
                #print('New action: '+ str(act1ToRemove))
                #print('Removing action: '+ str(act2ToRemove))
                self.actions.remove(act2ToRemove)
            else:
                done = True
