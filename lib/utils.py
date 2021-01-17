# -*- coding: utf-8 -*-
"""
Created on Sat Jan 16 21:27:03 2021

@author: Alexander
"""

import bibtexparser
import re

def getBibtexTitles(filename):    
    
    with open(filename, encoding='utf8') as bibfile:
        bibresult = bibtexparser.load(bibfile)

    titles = [re.sub(r"[^a-zA-Z0-9]+", ' ',x['title']) for x in bibresult.entries];
    return titles

def insertNewlines(string, every=64):
    # This is a ridicoulusly complex routine
    # There must be something easier but textwrap does not do hyphens
    resultString = ""
    words = string.split()
    charCount = 0
    for word in words:
        word += " "
        if (charCount+len(word)+2) < every:
            resultString += word
            charCount += (len(word)+1) 
        else:
            if (len(word)+2) < every:
                resultString += "\n"
                resultString += word
                charCount = len(word)
            else:
                if charCount+2 == every or \
                   charCount+3 == every:
                    resultString += "\n"
                    charCount = 0
                word += " "                
                for char in word:
                    if (charCount+3) < every:
                        resultString += char
                        charCount += 1
                    elif (charCount+3) == every:
                        resultString += "-\n"
                        charCount = 0
                    else:
                        raise ValueError("Internal error while parsing label text")
                                
    return resultString