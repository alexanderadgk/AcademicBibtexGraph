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
    def getIdsByName(name,key):
        name_query = "https://api.labs.cognitive.microsoft.com/academic/v1.0/evaluate?expr=Ti='" \
                     + quote(name_clean.lower()) + \
                     "'&model=latest&count=10&offset=0&attributes=Id,Ti&subscription-key="
        results = magAPI.getContent(name_query,key)   
        namesIds = []
        for result in results['entities']:
            namesIds.append({'Id':result['Id'],'name':result['Ti']})
        return namesIds
    
    @staticmethod
    def getNamesById(Id,key):
        id_query = "https://api.labs.cognitive.microsoft.com/academic/v1.0/evaluate?&expr=Id=" \
                         + Id + \
                   "&count=10&attributes=Id,Ti&subscription-key="
        results = magAPI.getContent(id_query,key)
        namesIds = []
        for result in results['entities']:
            namesIds.append({'Id':result['Id'],'name':result['Ti']})
        return namesIds
        
    @staticmethod    
    def getReferencesById(Id,key):
        backward_query = "https://api.labs.cognitive.microsoft.com/academic/v1.0/evaluate?&expr=Id=" \
                         + Id + \
                         "&count=1000&attributes=RId&subscription-key="
        referenceResults = magAPI.getContent(backward_query,key)
        if referenceResults:
            if len(referenceResults['entities']) != 1:
                raise ValueError("Unexpected number of results from reference search")
            else:
                return referenceResults['entities'][0]['RId']
        else:
            raise ValueError("Unexpected number of results from reference search")
    
    @staticmethod   
    def getCitationsById(Id,key):
        #This gets all papers that cite this paer
        #forward_query = "https://api.labs.cognitive.microsoft.com/academic/v1.0/evaluate?&expr=RId=2807461834&count=1000&attributes=Ti,RId&subscription-key="
        raise NotImplementedError
