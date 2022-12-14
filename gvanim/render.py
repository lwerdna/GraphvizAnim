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

from subprocess import Popen, PIPE, STDOUT, call
from multiprocessing import Pool, cpu_count

def render_single(params):
    path, fmt, size, graph = params
    with open(path , 'w') as out:
        pipe = Popen([ 'dot',  '-Gsize=1,1!', '-Gdpi={}'.format(size), '-T', fmt ], stdout = out, stdin = PIPE, stderr = None)
        pipe.communicate(input = graph.encode())
    return path

def render(graphs, basename, ext = 'png', size = 320):
    paths = []

    # single core
    for (n,graph) in enumerate(graphs):
        path = f'/tmp/{basename}_{n:03}.{ext}'
        print(f'rendering frame {n+1}/{len(graphs)} to {path}')
        render_single((path, ext, size, graph))
        paths.append(path)

    return paths

    try:
        _map = Pool(processes = cpu_count()).map
    except NotImplementedError:
        _map = map
    return _map(render_single, [ ('{}_{:03}.{}'.format(basename, n, fmt), fmt, size, graph) for n, graph in enumerate(graphs) ])

def gif(files, basename, delay = 100, size = 320):
    for file in files:
        call([ 'mogrify', '-gravity', 'center', '-background', 'white', '-extent', str(size), file ])
    cmd = [ 'convert' ]
    for file in files:
        cmd.extend(('-delay', str(delay), file))
    cmd.append(basename + '.gif')
    print(' '.join(cmd))
    call(cmd)
