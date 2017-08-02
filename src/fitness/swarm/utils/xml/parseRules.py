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
        ruleSet = set();
        if self.xmlstring is not None:
            #print ("From parseRules",self.xmlstring)
            tree = ET.fromstring(self.xmlstring)
            root = tree
        else:
            tree = ET.parse(self.rules_filename);
            root = tree.getroot();            
        #print (tree)
        state_cnt = 0
        for ruleElement in root:
            if ruleElement.tag == 'state':
                rule = GESwarm.Rule()
                state = ruleElement.find('state1')
                #print ('State',state_cnt)
                #print ('---------------')
                ##Parsing Luggage Values
                luggage = state.find('luggage')
                #print (state.find('luggage').text)
                carry = luggage.find('carry1')                
                drop = luggage.find('drop1')    
                drop_condition =  drop.find('condition').text
                drop_value =  drop.find('value').text                
                carry_condition =  carry.find('condition').text
                carry_value =  carry.find('value').text                                
                #print (carry_condition,carry_value)
                carry = (carry_condition,carry_value)
                drop = (drop_condition,drop_value)
                luggage = GESwarm.Luggage(carry,drop)
                #print (luggage)
                rule.luggage = luggage
                #print (luggage.to_engine())                
                #exit()
                ##Parsing Movement values
                movement = state.find('movement')
                m_condition = movement.find('condition').text 
                m_value = movement.find('value').text
                m_orientation = movement.find('orientation').text                
                #print ('M',m_condition,m_value,m_orientation)                  
                movement = GESwarm.Move(m_value,m_condition,m_orientation)
                rule.movement = movement
                #print (movement)
                #print (movement.to_engine())
                #print (luggage,movement)
                #print (movement)
                #print ('---------------\n\n')   
                state_cnt += 1  
                ruleSet.add(rule)
        #i = 0;
        rules_json = []
        for rule in ruleSet:
            #i+=1;
            #print('[RULE '+str(i) + '] of RuleSet [' + fileName +'] Simplification:');
            #rule.__simplifyActions__();
            rules_json.append(rule.__manual__())
            #str(rule)
            #rules_json.append(rule.__manual__())

        if self.xmlstring is None:
            Conv.convertToText(self.rules_filename, ruleSet);
        else:
            Conv.convertToText("testing.xml", ruleSet);    
        #Conv.convertToLatex(ROOT_DIR,self.rules_filename,ruleSet);
        #print (rules_json)

        return rules_json        
        


if __name__=='__main__':
    rules = ParseRules(os.path.join(ROOT_DIR, "new_rules.xml"))
    #Conv.convertToText(ROOT_DIR,)
    print (rules.convert())



  