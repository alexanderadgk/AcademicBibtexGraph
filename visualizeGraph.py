# -*- coding: utf-8 -*-
"""
Created on Sat Jan 16 16:01:17 2021

@author: Alexander
"""
import time
import networkx as nx
import matplotlib.pyplot as plt
import pygraphviz
from networkx.drawing.nx_agraph import graphviz_layout
from textwrap import fill as wrapText
import argparse
import os

'''
================================================
1. Parse command line arguments and get load Graph
================================================
'''

parser = argparse.ArgumentParser()
parser.add_argument('--file', help='GraphML Input File', required=True)
parser.add_argument('--output',help='You can specify the output file name')
parser.add_argument('--brightedges',help='Hide the edges',action='store_true')
parser.add_argument('--omitforward',help='Do not plot the forward search',action='store_true')
parser.add_argument('--omitbackward',help='Do not plot the backward search',action='store_true')
parser.add_argument('--size', type=str, help='Size of the figure e.g. --size=180,120')
args = parser.parse_args()

filename = args.file
G = nx.read_graphml(filename)


'''
================================================
2. Remove Nodes if given
================================================
'''

removeNodes = []
if args.omitforward:
    removeNodes += [key for (key,value) in \
        dict(G.nodes(data='source')).items() if value=='forward']                    
if args.omitbackward:
    removeNodes += [key for (key,value) in \
        dict(G.nodes(data='source')).items() if value=='backward']  
if removeNodes:
    G.remove_nodes_from(removeNodes)

'''
================================================
3. Prepare everything for the plot (colors, labels)
================================================
'''
#Prepare labels and colors
labels=dict((n,wrapText(d['label'],14,break_long_words=False)) for n,d in G.nodes(data=True))
sources=dict((n,d['source']) for n,d in G.nodes(data=True))
colors=[]
for key,value in sources.items():
    if value == "bib":
        colors.append((0.9, 0.9, 0.9))
    elif value == "backward":
        colors.append((0.7,0.7,1))
    elif value == "forward":
        colors.append((0.7,1,0.7))
    else:
        #Unkknown attribute
        colors.append((1, 0.7, 0.7))

if args.brightedges:
    color_edge = (0.95,0.95,0.95)
else:
    color_edge = (0.5, 0.5,0.5)

'''
================================================
4. Create Layout, Save and Plot the graph
================================================
'''

print("Creating dot layout")
pos = graphviz_layout(G, prog = "dot",args="-Gmindist=200")

#At least 180 times 120 is needed for the complete plot if there are many nodes
print("Drawing network.....")
if args.size:
    stringtuple = args.size.split(',')
    xsize = int(stringtuple[0])
    ysize = int(stringtuple[1])
    plt.figure(figsize=(xsize,ysize))
else:    
    plt.figure(figsize=(180,120))
nx.draw_networkx(G, pos, arrows=True, with_labels = False,  node_shape = "s", node_color = colors, edge_color = color_edge ,node_size = 1200, arrowsize=2, connectionstyle='arc3, rad=0.1')
nx.draw_networkx_labels(G,pos,labels = labels, font_size = 3.5)
if args.output:
    outfile = args.output
else:
    outfile = "output" + os.sep + "Plot_"+time.strftime('%Y%m%d%H%M%S')+".pdf"
plt.savefig(outfile)