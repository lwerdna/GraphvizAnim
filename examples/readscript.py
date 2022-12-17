#!/usr/bin/env python

import os, sys
import re

# exercise many gvanim options

from gvanim import Animation, render, gif

ga = Animation()

for line in open(sys.argv[1]).readlines():
    if line.startswith('//'):
        continue

    line = line.rstrip()
    
    if m:= re.match(r'ADD_NODE\((.*)\)$', line):
        node_name = m.group(1)
        ga.add_node(node_name)
    elif line in ['NEXT_FRAME()', 'NEXT_STEP()']:
        ga.next_step()
    elif m:= re.match(r'ADD_EDGE\((.*),\s*(.*)\)$', line):
        a, b = m.group(1, 2)
        ga.add_edge(a, b)
    elif m:= re.match(r'SET_NODE_LABEL\((.*),\s*"(.*)"\)$', line):
        node, label = m.group(1, 2)
        ga.label_node(node, label)
    elif m:= re.match(r'LABEL_NODE\((.*),\s*"(.*)"\)$', line):
        node, label = m.group(1, 2)
        ga.label_node(node, label)        
    elif m:= re.match(r'SET_NODE_PROPERTY\((.*),\s*"(.*)",\s*(".*")\)$', line):
        node, pname, pvalue = m.group(1, 2, 3)
        ga.add_node_property(node, pname, pvalue)
    elif m:= re.match(r'HIGHLIGHT_NODE\((.*)\)$', line):
        node_name = m.group(1)
        ga.highlight_node(node_name)
    elif m:= re.match(r'HIGHLIGHT_EDGE\((.*),\s*(.*)\)$', line):
        a, b = m.group(1, 2)
        ga.highlight_edge(a, b)
    else:
        print(f'ERROR: {line}')
        assert False

graphs = ga.graphs()
files = render(graphs, 'readscript', 'png', size=None)
gif(files, 'readscript', 50, size=None)
