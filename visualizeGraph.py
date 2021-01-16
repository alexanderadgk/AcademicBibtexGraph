# -*- coding: utf-8 -*-
"""
Created on Sat Jan 16 16:01:17 2021

@author: Alexander
"""

import networkx as nx
import matplotlib.pyplot as plt
import pygraphviz
from networkx.drawing.nx_agraph import graphviz_layout

def insert_newlines(string, every=64):
    #Make the first 13-lettes bold
    #string = r"$\bf{" + string[:13] + "}$" + string[13:]
    return '\n'.join(string[i:i+every] for i in range(0, len(string), every))

filename = 'Graph_citations_20210116155738.graphml';
G = nx.read_graphml(filename)

print("Creating dot layout")
pos = graphviz_layout(G, prog = "dot",args="-Gmindist=200")

labels=dict((n,insert_newlines(d['label'],14)) for n,d in G.nodes(data=True))
sources=dict((n,d['source']) for n,d in G.nodes(data=True))
colors=[]
for key,value in sources.items():
    if value == "bib":
        colors.append((1, 0.5, 0.5))
    elif value == "backward":
        colors.append((0.9, 0.9, 0.9))
    else:
        colors.append((0.5, 0.5, 1))

#At least 180 times 120 is needed for the complete plot
plt.figure(figsize=(180,120))

print("Drawing network.....")
nx.draw_networkx(G, pos, arrows=True, with_labels = False,  node_shape = "s", node_color = colors ,node_size = 1200, arrowsize=12, connectionstyle='arc3, rad=0.1')
nx.draw_networkx_labels(G,pos,labels = labels, font_size = 3.5)
plt.savefig("graph.pdf")