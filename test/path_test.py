import unittest
import sys
sys.path.append('../sink')

from sink import util

class TestPathMethods(unittest.TestCase):

    def test_cd(self):
        mydir = util.directory('test')
        self.assertEqual(mydir.get_directory(), '/test/')

        mydir.change_directory('main')
        self.assertEqual(mydir.get_directory(), '/test/main/')

        mydir.change_directory('..')
        self.assertEqual(mydir.get_directory(), '/test/')

        mydir.change_directory('..')
        self.assertEqual(mydir.get_directory(), '/')

        mydir.change_directory('..')
        self.assertEqual(mydir.get_directory(), '/')

        mydir.change_directory('test/help')
        self.assertEqual(mydir.get_directory(), '/test/help/')

if __name__ == '__main__':
    unittest.main()

