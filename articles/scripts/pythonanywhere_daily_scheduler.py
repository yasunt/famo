#!/usr/bin/env python3.5
activate_this = '/home/yasunt/.virtualenvs/VIRTUALENV/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

import sys

# explicitly set package path
path = '/home/ACCOUNT/CLONEDIR/'
if path not in sys.path:
    sys.path.append(path)

import subprocess

subprocess.Popen(['python', '/home/ACCOUNT/CLONEDIR/SCRIPT.py'] + sys.argv[1:])
