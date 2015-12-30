import os
from termcolor import colored as coloured
"""Provides utilities for dropbox and other misc. things"""


def is_file(file):
    """Returns true if the given item is dropbox file"""
    return hasattr(file, 'size')

def print_error(msg):
    print(coloured(msg, 'red'))

def print_succ(msg):
    print(coloured(msg, 'green'))

class directory(object):
    """Represents a directory in the user's dropbox"""

    def __init__(self, dir):
        self.dir = self.normalize_dir(dir)

    def normalize_dir(self, dir):
        if not dir.startswith('/'):
            dir = '/' + dir
        dir = os.path.normpath(dir)

        if not dir.endswith('/'):
            dir = dir + '/'

        return dir

    def get_dir(self):
        if self.get_directory() == '/':
            return ''
        if self.get_directory().endswith('/'):
            return self.get_directory()[:-1]
        return self.get_directory()

    def get_directory(self):
        return self.dir

    def change_directory(self, newdir):
        """Sets the current directory to directory given"""
        self.dir = self.normalize_dir(self.dir + newdir)

    def is_valid_directory(self, dir):
        """Checks to see if a given directory is valid"""
        return os.path.exists(dir)


class file_path(object):
    """Represents a file in the users dropbox, or on their machine"""

    def __init__(self, path, filename):
        self.path = self.normalize_file(self.normalize_path(path) + filename)

    def normalize_path(self, path):
        if not path.startswith('/'):
            path = '/' + path
        path = os.path.normpath(path)

        if not path.endswith('/'):
            path = path + '/'

        return path

    def normalize_file(self, file):
        return os.path.normpath(file)

    def get_dir_name(self):
        """Returns the path of the directory the file is in"""
        return os.path.dirname(self.path)

    def get_full_path(self):
        """Returns the path to the file, including the file name"""
        return self.path

    def get_filename(self):
        """Returns the name of the file"""
        return os.path.basename(self.path)
