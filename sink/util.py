def is_file(file):
    """Returns true if the given item is file"""
    return hasattr(file, 'size')

import os

class directory(object):
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


class file_path(object):
    def __init__(self, path):
        self.path = path

    def get_location(self):
        """Returns the path of the directory the file is in"""
        return os.path.dirname(self.path)

    def get_full_path(self):
        """Returns the path to the file, including the file name"""
        return self.path

    def get_filename(self):
        """Returns the name of the file"""
        return os.path.basename(self.path)


