# vim: et sw=4 ts=4:

import os
import subprocess

def patch_makefile_librpath(options, buildout, environ=None):
    expr = r"s/LIBRPATH='.*'/LIBRPATH='\\\$\$\$\$\$\$\$\$ORIGIN\/..\/lib'/g"
    args = ['sed', '-i', '-e', expr, 'Makefile']
    subprocess.check_call(args)

