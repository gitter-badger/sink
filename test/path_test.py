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

    def test_file_name(self):
        path = '/media/music/'
        filename = 'bad_blood.mp3'
        myfile = util.file_path(path, filename)

        self.assertEqual(myfile.get_filename(), 'bad_blood.mp3')
        self.assertEqual(myfile.get_full_path(), '/media/music/bad_blood.mp3')
        self.assertEqual(myfile.get_dir_name(), '/media/music')

        path = '/media/music'
        myfile = util.file_path(path, filename)

        self.assertEqual(myfile.get_filename(), 'bad_blood.mp3')
        self.assertEqual(myfile.get_full_path(), '/media/music/bad_blood.mp3')
        self.assertEqual(myfile.get_dir_name(), '/media/music')

        path = '/media/music/taytay/'
        filename = 'singles/blank_space.mp3'
        myfile = util.file_path(path, filename)

        self.assertEqual(myfile.get_filename(), 'blank_space.mp3')
        self.assertEqual(myfile.get_full_path(),
                         '/media/music/taytay/singles/blank_space.mp3')
        self.assertEqual(myfile.get_dir_name(), '/media/music/taytay/singles')

        path = '/media/music/oldtaytay/'
        filename = '../taytay/singles/wildest_dreams.mp3'
        myfile = util.file_path(path, filename)

        self.assertEqual(myfile.get_filename(), 'wildest_dreams.mp3')
        self.assertEqual(myfile.get_full_path(),
                         '/media/music/taytay/singles/wildest_dreams.mp3')
        self.assertEqual(myfile.get_dir_name(), '/media/music/taytay/singles')


if __name__ == '__main__':
    unittest.main()
