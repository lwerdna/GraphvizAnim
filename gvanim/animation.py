# Copyright 2016, Massimo Santini <santini@di.unimi.it>
#
# This file is part of "GraphvizAnim".
#
# "GraphvizAnim" is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# "GraphvizAnim" is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# "GraphvizAnim". If not, see <http://www.gnu.org/licenses/>.

from __future__ import absolute_import

from email.utils import quote
import shlex

from gvanim import action

class ParseException(Exception):
    pass

class Step(object):
    def __init__(self, step=None):
        # the previous step is given to us as an argument, replicate it
        if step:
            self.V = step.V.copy()
            self.E = step.E.copy()
            self.lV = step.lV.copy()
            self.lE = step.lE.copy()
            self.hV = step.hV.copy()
            self.hE = step.hE.copy()
            self.node_properties = {}
            for node_name in step.node_properties:
                self.node_properties[node_name] = step.node_properties[node_name].copy()

        # no previous step is given (NextStep() was called with "clean") to clear shit
        else:
            self.V = set()
            self.E = set()
            self.lV = dict()
            self.lE = dict()
            self.hV = dict()
            self.hE = dict()
            self.node_properties = dict()

    def node_format(self, v):
        fmt = []
        if v in self.lV:
            fmt.append('label="{}"'.format(quote(str(self.lV[ v ]))))
        if v in self.hV:
            fmt.append('color={}'.format(self.hV[ v ]))
        if v in self.node_properties:
            for (name, value) in self.node_properties[v].items():
                fmt.append(f'{name}={value}')
        elif v not in self.V:
            fmt.append('style=invis')
        if fmt:
            return '[{}]'.format(', '.join(fmt))
        return ''

    def edge_format(self, e):
        fmt = []
        if e in self.lE:
            fmt.append('label="{}"'.format(quote(str(self.lE[ e ]))))
        if e in self.hE:
            fmt.append('color={}'.format(self.hE[ e ]))
        elif e not in self.E:
            fmt.append('style=invis')
        if fmt:
            return '[{}]'.format(', '.join(fmt))
        return ''

    def __repr__(self):
        # vertices, edges
        # highlighted vertices, highlighted edges
        #    labelled vertices,    labelled edges
        return '{{ V={}, E={}, hV={}, hE={}, lV={}, lE={} properties={}}}'.format(self.V, self.E, self.hV, self.hE, self.lV, self.lE, self.node_properties)

class Animation(object):
    def __init__(self):
        self._actions = []

    def next_step(self, clean=False):
        self._actions.append(action.NextStep(clean))

    def add_node(self, v):
        self._actions.append(action.AddNode(v))

    def add_node_property(self, v, name, value):
        self._actions.append(action.AddNodeProperty(v, name, value))

    def remove_node_property(self, v, name):
        self._actions.append(action.RemoveNodeProperty(v, name))

    def highlight_node(self, v, color='red'):
        self._actions.append(action.HighlightNode(v, color=color))

    def unhighlight_node(self, v):
        self._actions.append(action.UnHighlightNode(v))

    def label_node(self, v, label):
        self._actions.append(action.LabelNode(v, label))

    def unlabel_node(self, v):
        self._actions.append(action.UnlabelNode(v))

    def remove_node(self, v):
        self._actions.append(action.RemoveNode(v))

    def add_edge(self, u, v):
        self._actions.append(action.AddEdge(u, v))

    def highlight_edge(self, u, v, color='red'):
        self._actions.append(action.HighlightEdge(u, v, color=color))

    def unhighlight_edge(self, u, v):
        self._actions.append(action.UnHighlightEdge(u, v))

    def label_edge(self, u, v, label):
        self._actions.append(action.LabelEdge(u, v, label))

    def unlabel_edge(self, u, v):
        self._actions.append(action.UnlabelEdge(u, v))

    def remove_edge(self, u, v):
        self._actions.append(action.RemoveEdge(u, v))

    def parse(self, lines):
        action2method = {
            'ns' : self.next_step,
            'an' : self.add_node,
            'hn' : self.highlight_node,
            'uhn' : self.unhighlight_node,
            'ln' : self.label_node,
            'un' : self.unlabel_node,
            'rn' : self.remove_node,
            'ae' : self.add_edge,
            'he' : self.highlight_edge,
            'uhe' : self.unhighlight_edge,
            'le' : self.label_edge,
            'ue' : self.unlabel_edge,
            're' : self.remove_edge,
        }
        for line in lines:
            parts = shlex.split(line.strip(), True)
            if not parts: continue
            action, params = parts[ 0 ], parts[ 1: ]
            try:
                action2method[ action ](*params)
            except KeyError:
                raise ParseException('unrecognized command: {}'.format(action))
            except TypeError:
                raise ParseException('wrong number of parameters: {}'.format(line.strip()))
                return

    def steps(self):
        steps = [ Step() ]
        for action in self._actions:
            action(steps)
        return steps

    def graphs(self):
        steps = self.steps()
        V, E = set(), set()
        for step in steps:
            V |= step.V
            E |= step.E
        graphs = []
        for n, s in enumerate(steps):
            graph = [ 'digraph G {' ]
            for v in V: graph.append('"{}" {};'.format(quote(str(v)), s.node_format(v)))
            for e in E: graph.append('"{}" -> "{}" {};'.format(quote(str(e[ 0 ])), quote(str(e[ 1 ])), s.edge_format(e)))
            graph.append('}')
            graphs.append('\n'.join(graph))
        
        return graphs
