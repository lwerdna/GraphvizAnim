#!/usr/bin/env python

# produce an animation of a build of the simple graph from:
# https://en.wikipedia.org/wiki/DOT_(graph_description_language)

from gvanim import Animation, render, gif

ga = Animation()

# A
ga.add_node('a')
ga.next_step()

# [A]
ga.highlight_node('a')
ga.next_step()

# [A] -> B
ga.add_edge('a', 'b')
ga.next_step()

# A -> [B]
ga.unhighlight_node('a')
ga.highlight_node('b')
ga.next_step()

# A -> [B] -> C
ga.add_edge('b', 'c')
ga.next_step()

# A -> [B] -> C
#          -> D
ga.add_edge('b', 'd')
ga.next_step()

# A -> [foo] -> C
#            -> D
ga.label_node('b', 'foo')
ga.next_step()

# A -> foo [->] C
#           ->  D
ga.unhighlight_node('b')
ga.highlight_edge('b', 'c')
ga.next_step()

# A -> foo  ->  C
#          [->] D
ga.unhighlight_edge('b', 'c')
ga.highlight_edge('b', 'd')
ga.next_step()


graphs = ga.graphs()
files = render(graphs, 'simple', 'png')
gif(files, 'simple', 50)
