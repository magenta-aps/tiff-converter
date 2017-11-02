import os
import tempfile
import unittest
import shutil
import mock

from tiff.filehandler import LocalFilePathStrategy, InPlaceFilePathStrategy


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


class TestLocalFilePathStrategy(unittest.TestCase):
    @mock.patch('tiff.filehandler.os.walk')
    def setUp(self, mock):
        mock.return_value = folder_structure_generator()
        self.handler = LocalFilePathStrategy(os.path.abspath('/base'))

    def test_should_return_folder1_file1(self):
        self.assertEqual(os.path.abspath('/base/folder1/file1'),
                         self.handler.get_source_path())

    def test_should_return_folder1_file2(self):
        self.handler.get_source_path()
        self.assertEqual(os.path.abspath('/base/folder1/file2'),
                         self.handler.get_source_path())

    def test_should_return_folder1_sub1_file3(self):
        self.handler.get_source_path()
        self.handler.get_source_path()
        self.assertEqual(os.path.abspath('/base/folder1/sub1/file3'),
                         self.handler.get_source_path())

    def test_should_return_folder2_sub4_file10(self):
        self.next(9)
        self.assertEqual(os.path.abspath('/base/folder2/sub4/file10'),
                         self.handler.get_source_path())

    def test_should_return_None_when_no_more_files(self):
        self.next(10)
        self.assertEqual(None, self.handler.get_source_path())

    def next(self, n):
        for i in range(n):
            self.handler.get_source_path()


class TestInPlaceFilePathStrategy(unittest.TestCase):
    def setUp(self):
        self.target = os.path.join(tempfile.gettempdir(), '_fps')
        self.tearDown()
        shutil.copytree(
            'test/resources/siarddk_multiple_medias_and_docCollections',
            self.target)
        self.file_path_strategy = InPlaceFilePathStrategy(self.target,
                                                          'AVID.MAG.1000')

    def tearDown(self):
        if os.path.isdir(self.target):
            shutil.rmtree(self.target)

    def test_next_file_is_11_sample_doc(self):
        self.assertEqual(
            os.path.join(self.target, 'AVID.MAG.1000.1', 'Documents',
                         'docCollection1', '1', 'sample.doc'),
            self.file_path_strategy._get_source_path())

    def test_next_file_is_12_sample_pdf(self):
        self.file_path_strategy._get_source_path()
        self.assertEqual(
            os.path.join(self.target, 'AVID.MAG.1000.1', 'Documents',
                         'docCollection1', '2', 'sample.pdf'),
            self.file_path_strategy._get_source_path())

    def test_next_file_is_23_sample_doc(self):
        self.file_path_strategy._get_source_path()
        self.file_path_strategy._get_source_path()
        self.assertEqual(
            os.path.join(self.target, 'AVID.MAG.1000.2', 'Documents',
                         'docCollection2', '3', 'sample.doc'),
            self.file_path_strategy._get_source_path())

    def test_next_file_is_24_sample_pdf(self):
        self.file_path_strategy._get_source_path()
        self.file_path_strategy._get_source_path()
        self.file_path_strategy._get_source_path()
        self.assertEqual(
            os.path.join(self.target, 'AVID.MAG.1000.2', 'Documents',
                         'docCollection2', '4', 'sample.pdf'),
            self.file_path_strategy._get_source_path())

    def test_next_file_is_35_sample_pdf(self):
        self.file_path_strategy._get_source_path()
        self.file_path_strategy._get_source_path()
        self.file_path_strategy._get_source_path()
        self.file_path_strategy._get_source_path()
        self.assertEqual(
            os.path.join(self.target, 'AVID.MAG.1000.2', 'Documents',
                         'docCollection3', '5', 'sample.doc'),
            self.file_path_strategy._get_source_path())

    def test_next_file_is_36_sample_pdf(self):
        self.file_path_strategy._get_source_path()
        self.file_path_strategy._get_source_path()
        self.file_path_strategy._get_source_path()
        self.file_path_strategy._get_source_path()
        self.file_path_strategy._get_source_path()
        self.assertEqual(
            os.path.join(self.target, 'AVID.MAG.1000.2', 'Documents',
                         'docCollection3', '6', 'sample.pdf'),
            self.file_path_strategy._get_source_path())


class TestSetWalker(unittest.TestCase):
    def setUp(self):
        self.target = os.path.join(tempfile.gettempdir(), '_temp')
        os.makedirs(os.path.join(self.target, 'AVID.MAG.1000.1', 'dummy'))
        os.makedirs(os.path.join(self.target, 'AVID.MAG.1000.1_old', 'dummy'))
        os.makedirs(os.path.join(self.target, 'AVID.MAG.1000.2', 'dummy'))
        os.makedirs(os.path.join(self.target, 'XYZ', 'dummy'))
        self.file_path_strategy = InPlaceFilePathStrategy(self.target,
                                                          'AVID.MAG.1000')

    def tearDown(self):
        shutil.rmtree(self.target)

    def test_should_prepare_walker_with_AVID_MAG_1000_1(self):
        self.file_path_strategy._set_walker()
        self.assertEqual(
            os.path.join(self.target, 'AVID.MAG.1000.1', 'Documents'),
            self.file_path_strategy._set_walker())

    def test_should_return_none_when_folder_AVID_MAG_1000_1_old(self):
        self.file_path_strategy.i = 1
        self.file_path_strategy._set_walker()
        self.assertIsNone(self.file_path_strategy._set_walker())

    def test_should_prepare_walker_with_AVID_MAG_1000_2(self):
        self.file_path_strategy.i = 2
        self.file_path_strategy._set_walker()
        self.assertEqual(
            os.path.join(self.target, 'AVID.MAG.1000.2', 'Documents'),
            self.file_path_strategy._set_walker())

    def test_should_return_none_when_folder_XYZ(self):
        self.file_path_strategy.i = 3
        self.file_path_strategy._set_walker()
        self.assertIsNone(self.file_path_strategy._set_walker())

    def test_should_return_none_when_i_is_4(self):
        self.file_path_strategy.i = 4
        self.file_path_strategy._set_walker()
        self.assertIsNone(self.file_path_strategy._set_walker())
