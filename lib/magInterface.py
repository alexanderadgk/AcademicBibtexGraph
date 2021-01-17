# -*- coding: utf-8 -*-
"""
Created on Sat Jan 16 21:11:23 2021

@author: Alexander
"""

import urllib.request
import json
from urllib.parse import quote

class magAPI():
    
    queriesExecuted = 0
    
    @classmethod
    def showNumberOfQueries(cls):
        print("Queries executed: "+str(cls.queriesExecuted))
    
    @classmethod
    def getContent(cls,query,key):
        url = query + key             
        req = urllib.request.Request(url)
        resp = urllib.request.urlopen(req).read()
        content = json.loads(resp.decode('utf-8'))
        cls.queriesExecuted += 1;
        return content
     
    @staticmethod
    def getEntityByName(name,key):
        name_query = "https://api.labs.cognitive.microsoft.com/academic/v1.0/evaluate?expr=Ti='" \
                     + quote(name.lower()) + \
                     "'&model=latest&count=10&offset=0&attributes=Id,Ti,DN,RId&subscription-key="
        results = magAPI.getContent(name_query,key)   
        #Check if anything came back
        try:
            entities = results['entities']
        except:
            entities = []
        
        if len(entities) == 1:
            #This should alway be the case
            return entities[0]
        elif len(entities == 0):
            print("------------------")
            print("No results found for: " + name)
            return []
        else:
            print("------------------")
            print("Multiple results found for: " + name)
            for entity in entities:
                print("Found: " + entity['Ti'])
            return []
        
    
    @staticmethod
    def getEntityById(Id,key):
        id_query = "https://api.labs.cognitive.microsoft.com/academic/v1.0/evaluate?&expr=Id=" \
                         + Id + \
                   "&count=10&attributes=Id,Ti,DN,RId&subscription-key="
        results = magAPI.getContent(id_query,key)
        try:
            entities = results['entities']
        except:
            entities = []
        
        if len(entities) == 1:
            return entities[0]
        else:
            return []
        
  
    @staticmethod   
    def getCitationsById(Id,key):
        #This gets all papers that cite this paer
        forward_query = "https://api.labs.cognitive.microsoft.com/academic/v1.0/evaluate?&expr=RId="\
                        + Id + \
                        "&count=1000&attributes=Id&subscription-key="
        entities = magAPI.getContent(forward_query,key)
        Ids = []
        try:
            Ids = [entity['Id'] for entity in entities]
        except:
            pass
        return Ids
