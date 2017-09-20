import os
import shutil
import tempfile
import unittest

from siarddk.docmanager import LocalDocumentManager
from tiff.converter import Converter


class TestConverter(unittest.TestCase):

    def setUp(self):
        self.source = os.path.abspath('test/resources/root')
        self.target = os.path.join(tempfile.gettempdir(), 'tiff-converter')
        self.converter = Converter(self.source, self.target, 'AVID.MAG.1000',
                                   LocalDocumentManager())

    def tearDown(self):
        if os.path.isdir(self.target):
            shutil.rmtree(self.target)

    def test_should_store_source_in_attribute(self):
        self.assertEqual(self.source, self.converter.source)

    def test_should_store_target_in_attribute(self):
        self.assertEqual(self.target, self.converter.target)

    def test_should_create_folders_AVID_MAG_1000_1_and_Document(self):
        self.converter.convert()
        self.assertTrue(os.path.isdir(
            os.path.join(self.target, 'AVID.MAG.1000.1', 'Documents')))

    def test_should_create_folder_AVID_MAG_1000_2_and_Documents(self):
        self.converter.docmanager.MAX = 2
        self.converter.convert()
        self.assertTrue(os.path.isdir(
            os.path.join(self.target, 'AVID.MAG.1000.2', 'Documents')))

    def test_folder_docCollection1_should_exists_after_file_conversion(self):
        self.converter.convert()
        self.assertTrue(os.path.isdir(
            os.path.join(self.target, 'AVID.MAG.1000.1', 'Documents',
                         'docCollection1')))

    def test_folder_docCollection2_should_exists_after_file_conversion2(self):
        self.converter.docmanager.MAX = 2
        self.converter.convert()
        self.assertTrue(os.path.isdir(
            os.path.join(self.target, 'AVID.MAG.1000.1', 'Documents',
                         'docCollection2')))

    def test_docCollection1_1_should_exist_after_file_conversion(self):
        self.converter.convert()
        self.assertTrue(os.path.isdir(
            os.path.join(self.target, 'AVID.MAG.1000.1', 'Documents',
                         'docCollection1', '1')))

    def test_docCollection1_2_should_exist_after_file_conversion(self):
        self.converter.convert()
        self.assertTrue(os.path.isdir(
            os.path.join(self.target, 'AVID.MAG.1000.1', 'Documents',
                         'docCollection1', '2')))

    def test_should_create_folder_AVID_XYZ_2000_1(self):
        self.converter = Converter(self.source, self.target, 'AVID.XYZ.2000',
                                   LocalDocumentManager())
        self.converter.convert()
        self.assertTrue(os.path.isdir(
            os.path.join(self.target, 'AVID.XYZ.2000.1')))

    @unittest.skip('big bang')
    def test_should_convert_root_folder_correctly(self):
        self.converter.convert()

        self.assertTrue(os.path.isfile(
            os.path.join(target,
                         'AVID.MAG.1000.1/Documents/docCollection1/1/1.tif')))
        self.assertTrue(os.path.isfile(
            os.path.join(target,
                         'AVID.MAG.1000.1/Documents/docCollection1/1/2.tif')))
        self.assertTrue(os.path.isfile(
            os.path.join(target,
                         'AVID.MAG.1000.1/Documents/docCollection1/1/3.tif')))
        self.assertTrue(os.path.isfile(
            os.path.join(target,
                         'AVID.MAG.1000.1/Documents/docCollection1/1/4.tif')))
        self.assertFalse(os.path.isfile(
            os.path.join(target,
                         'AVID.MAG.1000.1/Documents/docCollection1/1/5.tif')))


        # Run test where MAX is changed from 10000 to 2
