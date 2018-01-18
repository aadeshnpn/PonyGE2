import sys
import os

class Behavior(object):
    def __init__(self,id):
        self.id = id;
        self.vocab = {0 : 'RANDOM_WALK', 
                      1 : 'GO_TO_NEST', 
                      2 : 'GO_TO_SOURCE',
                      #3 : 'DROP_CUES',
                      3 : 'PICK_CUES',
                      #5 : 'SEND_SIGNALS',
                      4 : 'RECEIVE_SIGNALS'
                      };
   
    def __str__(self):
        return self.vocab[self.id];
    
    def __toLatex__(self):
        return '$B_\mathit{' +self.vocab[self.id] +'}$';
  
    def __eq__(self, ob):
        if self.id == ob.id:
            return True;
        else:
            return False;
        
    def __hash__(self):
        return self.id;

class InternalState(object):
    motivationalStateList = { 'STAY_UP_MOTIVATION', 'STAY_DOWN_MOTIVATION' };
    
    def __init__(self,id):
        self.id = id;
        self.vocab = {1 : 'DROP_FOOD',
                      #2 : 'STAY_DOWN_MOTIVATION',
                      #3 : 'STAY_UP_MOTIVATION',
                      2 : 'WANT_FOOD'};
                      #5 : 'STAY_DOWN',
                      #6 : 'STAY_UP'};
    
    def __str__(self):
        return self.vocab[self.id];
    
    def __eq__(self, ob):
        if self.id == ob.id:
            return True;
        else:
            return False;
        
    def __hash__(self):
        return self.id;

class Precondition(object):
    motivationalStateList = { 'STAY_UP', 'STAY_DOWN' };
    def __init__(self,id,value):
        self.id = id;
        self.value = value;
        self.vocab = {0 : 'HAS_FOOD', 
                      1 : 'ON_NEST', 
                      #2 : 'ON_GRASS',
                      2 : 'ON_SOURCE',
                      #4 : 'GOT_STUCK',
                      #5 : 'STAY_UP',
                      #6 : 'SAW_RED',
                      #7 : 'ON_SLOPE',
                      #8 : 'STAY_DOWN',
                      3 : 'DROP_FOOD',
                      #5 : 'DROP_FOOD',
                      #10 : 'NO_PRECONDITION',
                      #6 : 'NO_PRECONDITION',
                      #11 : 'GIONNI_TP',
                      #12 : 'WANT_FOOD'};
                      4 : 'WANT_FOOD',
                      5 : 'ON_SIGNALS',
                      6 : 'ON_CUE'
                      #5 : 'SEND_SIGNALS',
                      #6 : 'RECEIVE_SIGNALS',
                      #7: 'PUT_CUES',
                      #8: 'GET_CUES'
                      };  

        self.splitsymbol = None
    def __str__(self):
        strResult = self.vocab[self.id];
        if self.vocab[self.id] in Precondition.motivationalStateList:
            #print str(self.value);
            if self.value == True:
                strResult += ' > 0.5';
                self.splitsymbol = ' > '
            else:
                strResult += ' <= 0.5';
                self.splitsymbol = ' <= '
        else:
            strResult += ' is ' + str(self.value);
            self.splitsymbol = ' is '
        return strResult;
    
    def __toLatex__(self):
        strResult = '$P_\mathit{' +self.vocab[self.id] +'}';
        if self.vocab[self.id] in Precondition.motivationalStateList:
            if self.value == True:
                strResult += ' > 0.5$';
            else:
                strResult += ' <= 0.5$';
        else:
            strResult += ' == ' + str(self.value) + '$';
        return strResult;
    
    def __eq__(self, ob):
        if self.id == ob.id and self.value == ob.value:
            return True;
        else:
            return False;
    def __hash__(self):
        return self.__str__().__hash__();
        
class Action(object):
    def __init__(self,type,prob):
        self.type = type;
        self.prob = prob;
        self.typeVocab = {0 : 'DO_NOTHING',
                          1 : 'CHANGE_BEHAVIOR',
                          2 : 'SET_INTERNAL_VARIABLE'};
                          
    def __str__(self):
        return 'Action type: ' + self.typeVocab[self.type] + ' with p = ' + str(self.prob);
    
    def __eq__(self, ob):
        if self.type == ob.type and self.prob == ob.prob:
            return True;
        else:
            return False;
        
    def __hash__(self):
        return self.__str__().__hash__();
        
class BehaviorAction(Action):
    def __init__(self,prob,behavior):
        super(BehaviorAction,self).__init__(1,prob);
        self.newBehavior = behavior;
        
    def __str__(self):
        return 'AB: With p = ' + str(self.prob) + ' change behavior to ' + str(self.newBehavior);
        #return 
    
    def __toLatex__(self):
        return '$A_\\mathit{B}$ & $p=' + str(self.prob) + '$ & $B_\\mathit{'+str(self.newBehavior)+'}$\\\\\n';
    
    def __eq__(self,ob):
        if isinstance(ob, self.__class__):
            return super(BehaviorAction,self).__eq__(ob) and self.newBehavior == ob.newBehavior;
        else:
            return False;
    def __sameButProbability__(self,ob):
        if isinstance(ob,self.__class__):
            return self.newBehavior == ob.newBehavior;
        else:
            return False;
    
    def __manual__(self):
        #return {'AB':(self.prob,str(self.newBehavior))}
        return ('AB',self.prob,str(self.newBehavior))
    
class ISAction(Action):
    def __init__(self,prob,istate,value):
        super(ISAction,self).__init__(2,prob);
        self.istate = istate;
        self.value = value;
        self.increase = 0
        self.change = None

    def __toLatex__(self):
        strResult = '$A_\\mathit{IS}$ & $p=' + str(self.prob) + '$ & $IS_\\mathit{'+str(self.istate)+'}';
        if str(self.istate) in self.istate.motivationalStateList:
            if self.value == True:
                #strResult += '+= 0.05';
                strResult += '+';  
            else:
                #strResult += '-= 0.05';
                strResult += '-';
        else:
            #strResult += '';
            strResult += '\\leftarrow \\mathit{' + str(self.value) + '}$';
        strResult += '\\\\\n';
        return strResult
        
    def __str__(self):
        strResult = 'AIS: With p  = ' + str(self.prob);
        if str(self.istate) in self.istate.motivationalStateList:
            if self.value == True:
                strResult += ' increase internal state ' + str(self.istate) + ' by 0.05 ';
                self.increase = +1
                self.change = 0.05
            else:
                strResult += ' decrease internal state ' + str(self.istate) + ' by 0.05 ';
                self.increase = -1
                self.change = 0.05
        else:
            strResult += ' change internal state ' + str(self.istate) + ' to ' + str(self.value);
            self.increase = 0
            self.change = str(self.value)
        return strResult;
    
    def __eq__(self,ob):
        if isinstance(ob,self.__class__):
            return super(ISAction,self).__eq__(ob) and self.istate == ob.istate and self.value == ob.value;
        else:
            return False;
    def __sameButProbability__(self,ob):
        if isinstance(ob,self.__class__):
            return self.istate == ob.istate and self.value == ob.value;
        else:
            return False;

    def __manual__(self):
        #return {'AIS':[self.prob,self.increase,str(self.istate),0.05]}
        return ('AIS',self.prob,self.increase,str(self.istate),self.change)

class Rule(object):
    def __init__(self):
        self.behaviors = set();
        self.preconditions = set();
        self.actions = list();
        self.explanation = '';
        self.rule_json = None

    def __str__(self):
        strResult = '';
        strResult += '[Behaviors:]\n';
        behavior = set()
        #behavior['behaviors'] = []
        precond1 = set()
        #precond1['preconditions'] = []
        act = set()
        #act['actions'] = []
        for behave in self.behaviors:
            behavior.add(str(behave))
            strResult += str(behave) + '\n';
        strResult += '[Preconditions:]\n';
        for precond in self.preconditions:
            strResult += str(precond) + '\n';
            #temp = str(precond).split(precond.splitsymbol)
            temp = str(precond).split(' ')
            #print (temp)
            precond1.add(tuple(temp))            
        strResult += '[Actions:]\n';
        for action in self.actions:
            strResult += str(action) + '\n';
            act.add(action.__manual__())
        self.rule_json = [behavior,precond1,act]
        return strResult;
    
    def __manual__(self):
        return self.rule_json

    def __simplifyActions__(self):
        done = False;
        while not done:
            act1ToRemove = None;
            act2ToRemove = None;
            foundOne = False
            for action1 in self.actions:
                if foundOne:
                    break;
                for action2 in self.actions:
                    if not action1 is action2 and action1.__sameButProbability__(action2):
                        act1ToRemove = action1;
                        act2ToRemove = action2;
                        done = False;
                        foundOne = True;
                        break;
            if foundOne:
                #print('Modifying action: '+ str(act1ToRemove));
                act1ToRemove.prob = 1 - ((1 - act1ToRemove.prob) * (1 - act2ToRemove.prob));
                #print('New action: '+ str(act1ToRemove));
                #print('Removing action: '+ str(act2ToRemove));
                self.actions.remove(act2ToRemove);
            else:
                done = True;
