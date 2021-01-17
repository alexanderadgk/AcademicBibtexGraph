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