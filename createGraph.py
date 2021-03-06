# -*- coding: utf-8 -*-
"""
Created on Sat Jan 16 11:00:52 2021

@author: Alexander
"""
import time
import networkx as nx
import argparse
import atexit
from lib.magInterface import magAPI
from lib.utils import getBibtexTitles
import os
'''
================================================
1. Parse command line arguments and get bibtex file
================================================
'''

#Parse command line input
parser = argparse.ArgumentParser()
parser.add_argument('--file', help='Bibtex Input File', required=True)
parser.add_argument('--key', help='Microsoft Academics API key', required=True)
parser.add_argument('--forward', help='Perform forward search',action='store_true')
parser.add_argument('--backward',help='Perform backwards search',action='store_true')
parser.add_argument('--output',help='You can specify the output file name')
parser.add_argument('--silent',help='Execute without asking questions...',action='store_true')
args = parser.parse_args()

#Make sure the user understands what he does
if not args.silent:
    print("Executing this script can significantly/completely drain the free 10000 Transactions you have each month")
    while True:
        answer = input('Do You Want To Continue? Y/N: ')
        if answer == 'Y':
            print("Continuing execution")
            break
        elif answer == 'N':
            print("Exiting...")
            exit
        else:
            print("Please answer Y or N")

#Now load the bibtex-File and create a list of names
atexit.register(magAPI.showNumberOfQueries)
myPaperNames = getBibtexTitles(args.file)
warningLimit = 100 #Ask again if you execute that many queries on refs

'''
================================================
2. Perform first backward search to get connections
between the papers
================================================
'''

#Check if all papers exist and get their ids
allFound = True
firstBackwardEdges = []
myPapers = dict() 
for name in myPaperNames:
    entity = magAPI.getEntityByName(name, args.key)  
    if entity:
        myId = entity['Id']
        myPapers[str(myId)] = entity['DN']
        try:
            RIds = entity['RId']
        except:
            RIds = []
        for RId in RIds:
            firstBackwardEdges.append((RId,myId))
    else:
        allFound = False
    #Microsofts Trial API does not allow more than one access per second
    time.sleep(1)

if not allFound and not args.silent and (args.backward or args.forward):
    print("WARNING! Not all papers where found by name.")
    while True:
        answer = input('Do You Want To Continue? Y/N: ')
        if answer == 'Y':
            print("Continuing execution")
            break
        elif answer == 'N':
            print("Exiting...")
            exit
        else:
            print("Please answer Y or N")


'''
================================================
3. Perform a second backward search needed to get
the names of the above papers and the connections
in between.
================================================
'''

secondBackwardEdges = []
backwardPapers = dict()
if args.backward:
    #Now we get the names of all papers referenced
    backwardReferences = [str(Id) for (Id,x) in firstBackwardEdges];
    backwardReferencesUnique = list(set(backwardReferences))
    print("Removed " + str(len(backwardReferences)-len(backwardReferencesUnique)) \
          + " duplicate References")
    continueFlag = True
    if len(backwardReferencesUnique) > warningLimit and not args.silent:
        print("WARNING! Backward search will execute " + str(len(backwardReferencesUnique)) + " queries.")
        while True:
            answer = input('Do You Want To Continue? Y/N: ')
            if answer == 'Y':
                print("Continuing execution")
                break
            elif answer == 'N':
                print("Skipping backward search...")
                continueFlag = False
            else:
                print("Please answer Y or N")  
    
    if continueFlag:
        for reference in backwardReferencesUnique:
            #This call needs to be adapted to get all the papers RIds also
            entity = magAPI.getEntityById(reference,args.key);
            if entity:
                #This should alway be the case
                backwardPapers[reference] = entity['DN'];
                try:
                    RIds = entity['RId']
                except:
                    RIds = []
                for RId in RIds:
                    secondBackwardEdges.append((RId,int(reference)))
            else:
                backwardPapers[reference] = "NOT FOUND OR MULTIPLE";        
            #Microsofts Trial API does not allow more than one access per second
            time.sleep(1)

'''
================================================
4. Perform a forward search if needed and a 
consecutive backward search to get the connections
between the forward Papers
================================================
'''

forwardEdges = []
forwardPapers = dict()
forwardBackwardEdges = []     
if args.forward:
    for Id in myPapers.keys():
        citationIds = magAPI.getCitationsById(Id,args.key)
        for citationId in citationIds:
            forwardEdges.append((int(Id),citationId))
        time.sleep(1)

    forwardReferences = [str(Id) for (x,Id) in forwardEdges]
    forwardReferencesUnique = list(set(forwardReferences))
    print("Removed " + str(len(forwardReferences)-len(forwardReferencesUnique)) \
          + " duplicate References")
    continueFlag = True
    if len(forwardReferencesUnique) > warningLimit and not args.silent:
        print("WARNING! Forward search will execute " + str(len(forwardReferencesUnique)) + " queries.")
        while True:
            answer = input('Do You Want To Continue? Y/N: ')
            if answer == 'Y':
                print("Continuing execution")
                break
            elif answer == 'N':
                print("Skipping Forward search...")
                continueFlag = False
            else:
                print("Please answer Y or N")
                
    if continueFlag:
        for reference in forwardReferencesUnique:
            entity = magAPI.getEntityById(reference, args.key)
            if entity:
                forwardPapers[reference] = entity['DN']
                try:
                    RIds = entity['RId']
                except:
                    RIds = []
                for RId in RIds:
                    forwardBackwardEdges.append((RId,int(reference)))
            else:
                forwardPapers[reference] = "NOT FOUND OR MULTIPLE"
            time.sleep(1)


'''
================================================
5. Clean the results you got
================================================
'''

#Clean nodes
forwardPapers = dict(set(forwardPapers.items())-set(myPapers.items()))
backwardPapers = dict(set(backwardPapers.items())-set(myPapers.items())-set(forwardPapers.items()))

#Collect Edges and remove the ones not pointing to included papers
allEdgesTemp = list(set(firstBackwardEdges + secondBackwardEdges + forwardEdges + forwardBackwardEdges))
allNodes = dict(list(myPapers.items())+list(backwardPapers.items())+list(forwardPapers.items()))
allEdges = []
for edge in allEdgesTemp:
    try:
        name = allNodes[str(edge[0])]
        allEdges.append(edge)
    except:
        pass   


'''
================================================
6. Create a graph and save it 
================================================
'''


G = nx.DiGraph()

#Add all nodes for my Papers
for Id,name in myPapers.items():
    G.add_node(int(Id), label = name, source = "bib")

for Id,name in backwardPapers.items():
    G.add_node(int(Id), label = name, source = "backward" )
        
for Id,name in forwardPapers.items():
    G.add_node(int(Id), label = name, source = "forward" )

#Now add all edges
G.add_edges_from(allEdges)
#Wirte to graph to an output file
if args.output:
    outfile = args.output
else:
    outfile = "output" + os.sep + "Graph_citations_"+time.strftime('%Y%m%d%H%M%S')+".graphml"
nx.write_graphml(G,outfile)
#Last but not least show all queries
magAPI.showNumberOfQueries()




