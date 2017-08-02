import sys
import os

def convertToText(fileName,ruleSet):
    ruleSetString = '[Rules Set '+fileName+']\n\n';
    #fileRules = open(directoryToParse+fileName+".txt", "w");
    fileRules = open(fileName+".txt", "w");
    i = 0;
    for rule in ruleSet:
        i += 1;
        ruleSetString += '== State ' + str(i) + ' ==\n';
        ruleSetString += str(rule) + '\n\n';
        fileRules.write(ruleSetString);
        ruleSetString = '';
    fileRules.close();