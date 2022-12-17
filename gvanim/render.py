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

def shellout(cmd, input_text=None):
    process = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    if input_text == None:
        (stdout, stderr) = process.communicate()
    else:
        if type(input_text) == str:
            input_text = input_text.encode('utf-8')
        (stdout, stderr) = process.communicate(input=input_text)
    stdout = stdout.decode("utf-8")
    stderr = stderr.decode("utf-8")
    process.wait()
    return (stdout, stderr)

def render_to_svg(dot):
    cmd = ['dot', '-T', 'svg']
    stdout, stderr = shellout(cmd, dot)
    assert not stderr
    return stdout

def render_single(path, ext, size, dot):
    cmd = ['dot']
    if size != None:
        cmd.extend(['-Gsize=1,1!', f'-Gdpi={size}'])
    cmd.extend(['-T', ext, '-o', path])
    print(' '.join(cmd))
    stdout, stderr = shellout(cmd, dot)
    assert not stderr
    return stdout

def render(graphs, basename, ext='png', size=320):
    paths = []

    # single core
    for (i, dot) in enumerate(graphs):
        path = f'/tmp/{basename}_{i:04}.{ext}'
        #breakpoint()
        print(f'rendering frame {i+1}/{len(graphs)} to {path}')
        render_single(path, ext, size, dot)
        paths.append(path)

    return paths

    try:
        _map = Pool(processes = cpu_count()).map
    except NotImplementedError:
        _map = map
    return _map(render_single, [ ('{}_{:04}.{}'.format(basename, n, fmt), fmt, size, graph) for n, graph in enumerate(graphs) ])

def gif(files, basename, delay=100, size=320):
    if size != None:
        for file in files:
            call(['mogrify', '-gravity', 'center', '-background', 'white', '-extent', str(size), file])
    cmd = [ 'convert' ]
    for file in files:
        cmd.extend(('-delay', str(delay), file))
    cmd.append(basename + '.gif')
    print(' '.join(cmd))
    call(cmd)
