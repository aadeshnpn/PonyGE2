import sys
import os

def convertToLatex(directoryToParse,fileName,ruleSet):
    ruleSetString = '[Rule Set '+fileName+']\n\n';
    directoryToSave = '/home/eferrante/Dropbox/papers/evo_tp/tables/';
    #fileRules = open(directoryToParse+fileName+".tex", "w");
    fileRules = open(directoryToSave+fileName+".tex", "w");
    fileRules.write("\\begin{table}[!t]\n");
    fileRules.write('\\begin{center}\n');
    #fileRules.write('\\begin{small}\n');
    #fileRules.write('\\begin{footnotesize}\n');
    fileRules.write('\\begin{scriptsize}\n');
    fileRules.write('\\begin{tabular*}{0.965\\textwidth}{|p{14}|p{107}|p{107}|p{135}|}\n');
    fileRules.write('\n');
    i=0
    for rule in ruleSet:
        i += 1;
        fileRules.write('\\hline\n');
        if rule.explanation == '':
            #fileRules.write('\\multicolumn{4}{|p{400}|}{$R_{'+str(i)+'}$: \\quad \\textbf{EDIT ME}} \\\\\n');
            fileRules.write('\\multicolumn{4}{|p{400}|}{$R_{'+str(i)+'}$: \\quad } \\\\\n');
        else:
            fileRules.write('\\multicolumn{4}{|p{400}|}{$R_{'+str(i)+'}$: \\quad ' + rule.explanation + '}\\\\\n');
        fileRules.write('\\hline\n');
        
        fileRules.write('$\\mathcal{P}_{' +str(i) +'}$ & ');
        countPrecond=0;
        if not rule.preconditions:
            fileRules.write('$\\varepsilon$');
            countPrecond+=1;
            fileRules.write(' & & ');
        for precond in rule.preconditions:
            countPrecond+=1;
            if countPrecond < 4:
                fileRules.write(precond.__toLatex__());
            if countPrecond < 3:
                fileRules.write(' & ');
        if countPrecond > 3:
            print('[' +fileName+ '] Rule '+ str(i) + ' has ' + str(countPrecond) +' preconditions');
        while countPrecond < 2 :
            fileRules.write(' & ');
            countPrecond+=1;
        fileRules.write('\\\\\n');
        fileRules.write('\\hline\n');
        
        fileRules.write('$\\mathcal{B}_{' +str(i) +'}$ & ');
        countBehaviors = 0;
        if not rule.behaviors:
            fileRules.write('$\\varepsilon$');
            countBehaviors+=1;
            fileRules.write(' & & ');
        for behav in rule.behaviors:
            countBehaviors+=1;
            if countBehaviors < 4:
                fileRules.write(behav.__toLatex__());
            if countBehaviors < 3:
                fileRules.write(' & ');
        if countBehaviors > 3:
            print('[' +fileName+ '] Rule '+ str(i) + ' has ' + str(countBehaviors) +' behaviors');
        while countBehaviors < 2 :
            fileRules.write(' & ');
            countBehaviors+=1;
        fileRules.write('\\\\\n');
        fileRules.write('\\hline\n');
        
        fileRules.write('$\\mathcal{A}_{' +str(i) +'}$');
        if not rule.actions:
            fileRules.write(' & $\\varepsilon$');
            fileRules.write(' & & ');
        for act in rule.actions:
            fileRules.write(' & ');
            fileRules.write(act.__toLatex__());
        fileRules.write('\\hline\n\n');
        
    fileRules.write('\\end{tabular*}\n');
    fileRules.write('\\end{small}\n');
    #fileRules.write('\\caption{' + fileName +' \\textbf{EDIT ME}}\n');
    fileRules.write('\\caption{' + fileName +'}\n');
    fileRules.write('\\label{table:'+fileName +'}\n');
    fileRules.write('\\end{center}\n');
    fileRules.write('\\end{table}\n');
    

def convertToText(fileName,ruleSet):
    ruleSetString = '[Rule Set '+fileName+']\n\n';
    #fileRules = open(directoryToParse+fileName+".txt", "w");
    fileRules = open(fileName+".txt", "w");
    i = 0;
    for rule in ruleSet:
        i += 1;
        ruleSetString += '== RULE ' + str(i) + ' ==\n';
        ruleSetString += str(rule) + '\n';
        fileRules.write(ruleSetString);
        ruleSetString = '';
    fileRules.close();