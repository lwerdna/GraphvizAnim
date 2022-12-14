#!/usr/bin/env python

# produce an animation of a build of the simple graph from:
# https://en.wikipedia.org/wiki/DOT_(graph_description_language)

from gvanim import Animation, render, gif

ga = Animation()

ga.add_node('a')
ga.next_step()

ga.highlight_node('a')
ga.next_step()

ga.highlight_node('a')
ga.add_edge('a', 'b')
ga.next_step()

ga.highlight_node('b')
ga.next_step()

ga.highlight_node('b')
ga.add_edge('b', 'c')
ga.next_step()

ga.highlight_node('b')
ga.add_edge('b', 'd')
ga.next_step()

ga.label_node('b', 'label for b')
ga.next_step()

graphs = ga.graphs()
files = render(graphs, 'simple', 'png')
gif(files, 'simple', 50)
