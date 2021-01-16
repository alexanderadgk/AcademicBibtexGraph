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


#Parse command line input
parser = argparse.ArgumentParser()
parser.add_argument('--file', help='Bibtex Input File', required=True)
parser.add_argument('--key', help='Microsoft Academics API key', required=True)
parser.add_argument('--forward', help='Perform forward search',action='store_true')
parser.add_argument('--backward',help='Perform backwards search',action='store_true')
parser.add_argument('--output',help='You can specify the output file name')
parser.add_argument('--silent',help='Execute without asking questions...',action='store_true')
args = parser.parse_args()
print(args)

#Need to include also links between those papers
if args.forward or args.backward:
    raise NotImplementedError()

#Make sure the user understands what he does
if not args.silent:
    print("Executing this script can significantly/completely drain the free 10000 Transactions you have each month")
    answer = input('Do You Want To Continue? Y/N: ')
    if answer == 'Y':
        print("Continuing execution")
    else:
        print("Exiting...")
        exit

#Now load the bibtex-File and create a list of names
atexit.register(magAPI.showNumberOfQueries)
myPaperNames = getBibtexTitles(args.file)

#Check if all papers exist and get their ids
myPapers = dict() 
allFound = True
for name in myPaperNames:
    namesIds = magAPI.getIdsByName(name, args.key)
    if len(namesIds) == 1:
        #This should alway be the case
        magId = namesIds[0]['Id']
        myPapers[str(magId)] = name       
    elif len(namesIds == 0):
        print("------------------")
        print("No results found for: " + name)
        allFound = False
    else:
        print("------------------")
        print("Multiple results found for: " + name)
        for nameId in namesIds:
            print("Found: " + nameId['name'])
        allFound = False
    #Microsofts Trial API does not allow more than one access per second
    time.sleep(1)

if not allFound and not args.silent:
    print("WARNING! Not all papers where found by name.")
    answer = input('Do You Want To Continue? Y/N: ')
    if answer == 'Y':
        print("Continuing execution")
    else:
        print("Exiting...")
        exit

#Now get all papers referenced by those papers
allEdges = []
for Id in myPapers.keys():
    referenceList = magAPI.getReferencesById(Id, args.key)
    #Microsofts Trial API does not allow more than one access per second
    for reference in referenceList:
        allEdges.append((reference,int(Id)))
    time.sleep(1)

if args.backward:
    #Now we get the names of all papers referenced
    allReferences = [str(Id) for (x,Id) in allEdges];
    referencesUnique = list(set(allReferences))
    print("Removed " + str(len(allReferences)-len(referencesUnique)) \
          + " duplicate References")
    if len(referencesUnique) > 100 and not args.silent:
        print("WARNING! This will execute " + str(len(referencesUnique)) + " queries.")
        answer = input('Do You Want To Continue? Y/N: ')
        if answer == 'Y':
            print("Continuing execution")
        else:
            print("Exiting...")
            exit    
    
    backwardPapers = dict()
    for reference in referencesUnique:
        #This call needs to be adapted to get all the papers RIds also
        namesIds = magAPI.getNamesById(reference,args.key);
        if len(namesIds) == 1:
            #This should alway be the case
            backwardPapers[reference] = namesIds[0]['name'];
        else:
            backwardPapers[reference] = "NOT FOUND OR MULTIPLE";        
        #Microsofts Trial API does not allow more than one access per second
        time.sleep(1)
else:
    #Remove entries that do not belong to the list
    allEdgesSwap = allEdges;
    allEdges = [];
    for edge in allEdgesSwap:
        try:
            name = myPapers[str(edge[0])]
            allEdges.append(edge)
        except:
            pass
        

if args.forward:
    pass
          
    
G = nx.DiGraph()

#Add all nodes for my Papers
for Id,name in myPapers.items():
    G.add_node(int(Id), label = name, source = "bib")

if args.backward:
    for Id,name in backwardPapers.items():
        G.add_node(int(Id), label = name, source = "backward" )
        
if args.forward:
    pass

#Now add all edges
G.add_edges_from(allEdges)
#Wirte to graph to an output file
if args.output:
    outfile = args.output
else:
    outfile = "Graph_citations_"+time.strftime('%Y%m%d%H%M%S')+".graphml"
nx.write_graphml(G,outfile)

magAPI.showNumberOfQueries()




