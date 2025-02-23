#!/usr/bin/env python

# exercise many gvanim options

from gvanim import Animation, render, gif

ga = Animation()

# A
ga.add_node('a')
ga.next_step()

#
ga.add_node_property('a', 'shape', 'triangle')
ga.next_step()

ga.add_node_property('a', 'shape', 'box')
ga.next_step()

ga.add_node_property('a', 'shape', 'egg')
ga.next_step()

ga.label_node('a', '')
ga.add_node_property('a', 'shape', '"none"')
ga.add_node_property('a', 'image', '"node_image0.png"')
ga.next_step()

ga.add_node_property('a', 'image', '"node_image1.png"')
ga.next_step()

ga.add_node_property('a', 'image', '"node_image2.png"')
ga.next_step()

ga.add_node_property('a', 'image', '"node_image3.png"')
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
files = render(graphs, 'exercise', 'png')
gif(files, 'exercise', 50)
