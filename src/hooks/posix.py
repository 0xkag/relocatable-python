# vim: et sw=4 ts=4:

from glob import glob
import os
from os import path, curdir

def _dist_path():
    dist = path.join(os.getcwd(), path.abspath(path.join('.',  # Python-2.7.5
                                                         path.pardir,  # python__compile__,
                                                         path.pardir,  # parts,
                                                         path.pardir,  # python-build
                                                         "dist")))
    return dist

def purge_sysconfigdata(options, buildout, environ):
    TRICK = """
# isolated-python trick
import sys
prefix = sys.real_prefix if hasattr(sys, 'real_prefix') else sys.prefix  # virtualenv
old_prefix = build_time_vars.get("prefix", "_some_path_that_does_not_exist")

for key, value in build_time_vars.items():
    build_time_vars[key] = value.replace(old_prefix, prefix) if isinstance(value, basestring) else value
"""
    dist = _dist_path()
    print 'dist = {}'.format(dist)
    print 'sysconfig = {!r}'.format(glob(path.join(dist, "*", "*", "_sysconfigdata.py")))
    [_sysconfigdata] = glob(path.join(dist, "*", "*", "_sysconfigdata.py"))
    with open(_sysconfigdata, 'a') as fd:
        fd.write(TRICK)

def patch_python_config(options, buildout, environ):
    PYTHON_CONFIG=r"""#!/bin/bash
P=$(cd "$(dirname "$0")"; pwd)
exec "$P/python" "$P/.$(basename "$0")" $*
"""
    dist = _dist_path()
    binpath = path.join(dist, 'bin')
    pyconf27 = path.join(binpath, 'python2.7-config')
    dotpyconf = path.join(binpath, '.python-config')
    dotpyconf2 = path.join(binpath, '.python2-config')
    dotpyconf27 = path.join(binpath, '.python2.7-config')
    os.rename(pyconf27, dotpyconf27)
    with open(pyconf27, 'w') as f:
        f.write(PYTHON_CONFIG)
    os.chmod(pyconf27, os.stat(dotpyconf27).st_mode)
    os.symlink(os.path.split(dotpyconf2)[1], dotpyconf)
    os.symlink(os.path.split(dotpyconf27)[1], dotpyconf2)

def patch(options, buildout, environ):
    purge_sysconfigdata(options, buildout, environ)
    patch_python_config(options, buildout, environ)

