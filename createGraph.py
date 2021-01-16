# -*- coding: utf-8 -*-
"""
Created on Sat Jan 16 11:00:52 2021

@author: Alexander
"""

import urllib.request
import json
from urllib.parse import quote
import time
import networkx as nx
import atexit
import re

def exit_handler():
    global queriesExecuted
    print("QueriesExecuted: " + str(queriesExecuted))

def getContent(query,key):
        global queriesExecuted
        url = query + key             
        req = urllib.request.Request(url)
        resp = urllib.request.urlopen(req).read()
        content = json.loads(resp.decode('utf-8'))
        queriesExecuted = queriesExecuted + 1;
        return content
    
def getIdsByName(name,key):
    name_clean = re.sub(r"[^a-zA-Z0-9]+", ' ',name)
    name_query = "https://api.labs.cognitive.microsoft.com/academic/v1.0/evaluate?expr=Ti='" \
                 + quote(name_clean.lower()) + \
                 "'&model=latest&count=10&offset=0&attributes=Id,Ti&subscription-key="
    results = getContent(name_query,key)   
    namesIds = []
    for result in results['entities']:
        namesIds.append({'Id':result['Id'],'name':result['Ti']})
    return namesIds
    
def getNamesById(Id,key):
    id_query = "https://api.labs.cognitive.microsoft.com/academic/v1.0/evaluate?&expr=Id=" \
                     + Id + "&count=10&attributes=Id,Ti&subscription-key="
    results = getContent(id_query,key)
    namesIds = []
    for result in results['entities']:
        namesIds.append({'Id':result['Id'],'name':result['Ti']})
    return namesIds
    
    
def getReferencesById(Id,key):
    backward_query = "https://api.labs.cognitive.microsoft.com/academic/v1.0/evaluate?&expr=Id=" \
                     + Id + "&count=1000&attributes=RId&subscription-key="
    referenceResults = getContent(backward_query,key)
    if referenceResults:
        if len(referenceResults['entities']) != 1:
            raise ValueError("Unexpected number of results from reference search")
        else:
            return referenceResults['entities'][0]['RId']
    else:
        raise ValueError("Unexpected number of results from reference search")

    
def getCitationsById(Id,key):
    #This gets all papers that cite this paer
    #forward_query = "https://api.labs.cognitive.microsoft.com/academic/v1.0/evaluate?&expr=RId=2807461834&count=1000&attributes=Ti,RId&subscription-key="
    pass
'''
Create section to parse input arguments
* key that should be used
* bibtex file (first paper name)
* forward search yes or no
* outfile name
'''

print("Executing this script can significantly/completely drain the free 10000 Transactions you have each month")
answer = input('Do You Want To Continue? Y/N')
if answer == 'Y':
   print("Continuing execution")
else:
   print("Exiting...")
   exit


key = "XXX"
myPapers = [];
myPapers.append("Translocation of a globular polymer through a hairy pore");
myPapers.append("Polymer-brush lubrication: a review of recent theoretical advances")
#This thing should always tell me how many queries have been run
atexit.register(exit_handler)
queriesExecuted = 0

#Check if all papers exist and get their ids
myPaperIds = dict() 
allFound = True
for name in myPapers:
    namesIds = getIdsByName(name, key)
    if len(namesIds) == 1:
        #This should alway be the case
        magId = namesIds[0]['Id']
        myPaperIds[str(magId)] = name       
    elif len(namesIds == 0):
        print("No results found for: " + name)
        allFound = False
    else:
        print("Multiple results found for: " + name)
        for nameId in namesIds:
            print("Found: " + nameId['name'])
        print("\n")
        allFound = False
    #Microsofts Trial API does not allow more than one access per second
    time.sleep(1)

if not allFound:
    print("WARNING! Not all papers where found by name.")
    answer = input('Do You Want To Continue? Y/N')
    if answer == 'Y':
       print("Continuing execution")
    else:
       print("Exiting...")
       exit

#Now get all papers referenced by those papers
allEdges = []
for Id in myPaperIds.keys():
    referenceList = getReferencesById(Id, key)
    #Microsofts Trial API does not allow more than one access per second
    for reference in referenceList:
        allEdges.append((reference,int(Id)))
    time.sleep(1)

#Now we get the names of all papers referenced
allReferences = [str(Id) for (x,Id) in allEdges];
referencesUnique = list(set(allReferences))
print("Removed " + str(len(allReferences)-len(referencesUnique)) \
      + " duplicate References")
if len(referencesUnique) > 100:
    print("WARNING! This will execute " + str(len(referencesUnique)) + " queries.")
    answer = input('Do You Want To Continue? Y/N')
    if answer == 'Y':
       print("Continuing execution")
    else:
       print("Exiting...")
       exit    
    
    
referenceNames = dict()
for reference in referencesUnique:
    namesIds = getNamesById(reference,key);
    if len(namesIds) == 1:
        #This should alway be the case
        referenceNames[reference] = namesIds[0]['name'];
    else:
        referenceNames[reference] = "NOT FOUND OR MULTIPLE";        
    #Microsofts Trial API does not allow more than one access per second
    time.sleep(1)


print("QueriesExecuted: " + str(queriesExecuted))


G = nx.DiGraph()

#Add all nodes for my Papers
for Id,name in myPaperIds.items():
    G.add_node(int(Id), label = name, source = "bib")
    
for Id,name in referenceNames.items():
    G.add_node(int(Id), label = name, source = "backward" )

#Now add all edges
G.add_edges_from(allEdges)
    
nx.write_graphml(G,"Graph_citations_"+time.strftime('%Y%m%d%H%M%S')+".graphml")




