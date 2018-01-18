import xml.etree.ElementTree as ET
import sys
import os
import glob

import fitness.swarm.utils.xml.definitions as GESwarm
import fitness.swarm.utils.xml.conversions as Conv
#import definitions as GESwarm
#import conversions as Conv

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

"""
[
    {'behaviors':['RANDOM_WALK','GO_TO_NEST'],
     'preconditions':[{'HAS_FOOD':True},{'ON_SLOPE':True},'ON_GRASS'],
     'actions':{'AB':[0.05,'GO_TO_NEST'],'AIS':[0.1,'+','STAY_UP_MOTIVATION',0.5]}
    }
]
"""
#directoryToParse = os.path.expandvars('$ARGOSINSTALLDIR') + '/user/eliseofe/xml/task_partitioning/rules/';
class ParseRules:
    def __init__(self, filename, xmlstring = None):
        self.rules_filename = filename
        self.xmlstring = xmlstring            
        #if xmlstring is not None:
        #    self.read_from_buffer = True


    def convert(self):
        ruleSet = [];
        if self.xmlstring is not None:
            #print ("From parseRules",self.xmlstring)
            tree = ET.fromstring(self.xmlstring)
            root = tree
        else:
            tree = ET.parse(self.rules_filename);
            root = tree.getroot();            
        #print (tree)
        for ruleElement in root:
            if ruleElement.tag == 'rule':
                rule = GESwarm.Rule();
                for prvStateElement in ruleElement.find('previous_states'):
                    prvStateId = prvStateElement.get('id');
                    behavior = GESwarm.Behavior(int(prvStateId));
                    rule.behaviors.add(behavior);
                for precondElement in ruleElement.find('preconditions'):
                    precondId = precondElement.get('id');
                    precondValue = precondElement.get('value');
                    boolPrecond = True if precondValue == 'true' else False;
                    #print (precondId,precondValue,boolPrecond)
                    i=0
                    #print (precondId)
                    for bit in precondId:
                        #print (bit)
                        if bit == '1':
                            precondition = GESwarm.Precondition(i,True);
                            #print (precondition)
                            rule.preconditions.add(precondition);                            
                        elif bit == '0':
                            precondition = GESwarm.Precondition(i,False);
                            rule.preconditions.add(precondition);
                        i +=1
                        #elif bit == '-':

                for actionElement in ruleElement.find('actions'):
                    actType = actionElement.get('type');
                    actProb = actionElement.get('prob');
                    #print (actType)
                    if actType == '1':
                        nextBehaviorId = actionElement.get('nxt_state_id');
                        action = GESwarm.BehaviorAction(float(actProb),GESwarm.Behavior(int(nextBehaviorId)));
                        rule.actions.append(action);
                    elif actType == '2':
                        isId = actionElement.get('variable_id')
                        isValue = actionElement.get('value')
                        boolISPrecond = True if isValue == 'true' else False;
                        action = GESwarm.ISAction(float(actProb),GESwarm.InternalState(int(isId)),boolISPrecond);
                        rule.actions.append(action);
                    else:
                        print ('Error! Invalid action type!')
                explainElement = ruleElement.find('explain')
                if explainElement != None:
                    rule.explanation = explainElement.text
                ruleSet.append(rule);
        i = 0;
        rules_json = []
        for rule in ruleSet:
            i+=1;
            #print('[RULE '+str(i) + '] of RuleSet [' + fileName +'] Simplification:');
            rule.__simplifyActions__();
            #print (rule)
            str(rule)
            rules_json.append(rule.__manual__())

        if self.xmlstring is None:
            Conv.convertToText(self.rules_filename, ruleSet);
        else:
            Conv.convertToText("handcoded1.xml", ruleSet);
            
        #Conv.convertToLatex(ROOT_DIR,self.rules_filename,ruleSet);
        #print (rules_json)
        return rules_json        
        


if __name__=='__main__':
    rules = ParseRules(os.path.join(ROOT_DIR, "test_rules.xml"))
    #Conv.convertToText(ROOT_DIR,)
    print (rules.convert())



  