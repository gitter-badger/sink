#!/usr/bin/env python3

import os
import shutil
from subprocess import call

'''
    Module to provide shell-like commands
'''
def copy(source, dest):
    shutil.copy(source, dest)

def join_paths(first, second):
    return os.path.join(first, second)

def get_home_dir():
    return os.path.expanduser('~')

def get_cwd():
    return os.getcwd()

def get_var(var, default):
    return os.getenv(var, default)

def set_var(var, val):
    os.environ[var] = val
