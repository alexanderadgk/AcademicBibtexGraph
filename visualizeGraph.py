# -*- coding: utf-8 -*-
"""
Created on Sat Jan 16 16:01:17 2021

@author: Alexander
"""

import networkx as nx
import matplotlib.pyplot as plt
import pygraphviz
from networkx.drawing.nx_agraph import graphviz_layout
from lib.utils import insertNewlines


filename = 'Graph_citations_20210117103908.graphml';
G = nx.read_graphml(filename)

print("Creating dot layout")
pos = graphviz_layout(G, prog = "dot",args="-Gmindist=200")

#Prepare labels and colors
labels=dict((n,insertNewlines(d['label'],14)) for n,d in G.nodes(data=True))
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