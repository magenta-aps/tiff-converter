import os
import unittest
import mock

from tiff.filehandler import LocalFileHandler


def folder_structure_generator():
    """
    For mocking the filesystem
    """
    yield (os.path.abspath('/base'), ['folder1', 'folder2'], [])
    yield (
        os.path.abspath('/base/folder1'), ['sub1', 'sub2'], ['file1', 'file2'])
    yield (os.path.abspath('/base/folder1/sub1'), [], ['file3', 'file4'])
    yield (os.path.abspath('/base/folder1/sub2'), [], ['file5', 'file6'])
    yield (
        os.path.abspath('/base/folder2'), ['sub3', 'sub4'], ['file7', 'file8'])
    yield (os.path.abspath('/base/folder2/sub3'), [], [])
    yield (os.path.abspath('/base/folder2/sub4'), [], ['file9', 'file10'])


class TestLocalFileHandler(unittest.TestCase):
    @mock.patch('tiff.filehandler.os.walk')
    def setUp(self, mock):
        mock.return_value = folder_structure_generator()
        self.handler = LocalFileHandler(os.path.abspath('/base'))

    def test_should_return_folder1_file1(self):
        self.assertEqual(os.path.abspath('/base/folder1/file1'),
                         self.handler.get_next_file())

    def test_should_return_folder1_file2(self):
        self.handler.get_next_file()
        self.assertEqual(os.path.abspath('/base/folder1/file2'),
                         self.handler.get_next_file())

    def test_should_return_folder1_sub1_file3(self):
        self.handler.get_next_file()
        self.handler.get_next_file()
        self.assertEqual(os.path.abspath('/base/folder1/sub1/file3'),
                         self.handler.get_next_file())

    def test_should_return_folder2_sub4_file10(self):
        self.next(9)
        self.assertEqual(os.path.abspath('/base/folder2/sub4/file10'),
                         self.handler.get_next_file())

    def test_should_return_None_when_no_more_files(self):
        self.next(10)
        self.assertEqual(None, self.handler.get_next_file())

    def next(self, n):
        for i in range(n):
            self.handler.get_next_file()
