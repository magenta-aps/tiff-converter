import os
import platform
import shutil
import tempfile
import unittest
import mock

from tiff.tiffconverter import convert as true_tiff_convert
from siarddk.docmanager import LocalDocumentManager
from tiff.converter import Converter


@unittest.skipIf(platform.system() == 'Linux', 'Since MS Word is Windows only')
class TestConverter(unittest.TestCase):
    def setUp(self):
        self.source = os.path.abspath('test/resources/root')
        self.target = os.path.join(tempfile.gettempdir(), 'tiff-converter')
        if os.path.isdir(self.target):
            shutil.rmtree(self.target)
        self.conversion_dir = os.path.join(tempfile.gettempdir(), '_conversion')
        self.converter = Converter(self.source, self.target,
                                   self.conversion_dir, 'AVID.MAG.1000',
                                   LocalDocumentManager())

    def tearDown(self):
        if os.path.isdir(self.target):
            shutil.rmtree(self.target)
        if os.path.isdir(self.conversion_dir):
            shutil.rmtree(self.conversion_dir)

    def test_should_store_source_in_attribute(self):
        self.assertEqual(self.source, self.converter.source)

    def test_should_store_target_in_attribute(self):
        self.assertEqual(self.target, self.converter.target)

    def test_should_store_temp_conversion_folder(self):
        self.assertEqual(self.conversion_dir, self.converter.conversion_dir)

    def test_should_create_folders_AVID_MAG_1000_1_and_Document(self):
        self.converter.run()
        self.assertTrue(os.path.isdir(
            os.path.join(self.target, 'AVID.MAG.1000.1', 'Documents')))

    def test_should_create_folder_AVID_MAG_1000_2_and_Documents(self):
        self.converter.docmanager.MAX = 2
        self.converter.run()
        self.assertTrue(os.path.isdir(
            os.path.join(self.target, 'AVID.MAG.1000.2', 'Documents')))

    def test_folder_docCollection1_should_exists_after_file_conversion(self):
        self.converter.run()
        self.assertTrue(os.path.isdir(
            os.path.join(self.target, 'AVID.MAG.1000.1', 'Documents',
                         'docCollection1')))

    def test_folder_docCollection2_should_exists_after_file_conversion2(self):
        self.converter.docmanager.MAX = 2
        self.converter.run()
        self.assertTrue(os.path.isdir(
            os.path.join(self.target, 'AVID.MAG.1000.1', 'Documents',
                         'docCollection2')))

    def test_docCollection1_1_should_exist_after_file_conversion(self):
        self.converter.run()
        self.assertTrue(os.path.isdir(
            os.path.join(self.target, 'AVID.MAG.1000.1', 'Documents',
                         'docCollection1', '1')))

    def test_docCollection1_2_should_exist_after_file_conversion(self):
        self.converter.run()
        self.assertTrue(os.path.isdir(
            os.path.join(self.target, 'AVID.MAG.1000.1', 'Documents',
                         'docCollection1', '2')))

    def test_should_create_folder_AVID_XYZ_2000_1(self):
        self.converter = Converter(self.source, self.target,
                                   self.conversion_dir, 'AVID.XYZ.2000',
                                   LocalDocumentManager())
        self.converter.run()
        self.assertTrue(os.path.isdir(
            os.path.join(self.target, 'AVID.XYZ.2000.1')))

    def test_should_convert_root_folder_correctly(self):
        self.converter.run()
        self.assertTrue(os.path.isfile(
            os.path.join(self.target, 'AVID.MAG.1000.1', 'Documents',
                         'docCollection1', '1', '1.tif')))
        self.assertTrue(os.path.isfile(
            os.path.join(self.target,
                         'AVID.MAG.1000.1', 'Documents', 'docCollection1',
                         '2', '2.tif')))
        self.assertTrue(os.path.isfile(
            os.path.join(self.target, 'AVID.MAG.1000.1', 'Documents',
                         'docCollection1', '3', '3.tif')))
        self.assertTrue(os.path.isfile(
            os.path.join(self.target, 'AVID.MAG.1000.1', 'Documents',
                         'docCollection1', '4', '4.tif')))
        self.assertFalse(os.path.isfile(
            os.path.join(self.target, 'AVID.MAG.1000.1', 'Documents',
                         'docCollection1', '5', '5.tif')))

    def test_should_convert_root_folder_correctly_when_MAX_2(self):
        self.converter.docmanager.MAX = 2
        self.converter.run()
        self.assertTrue(os.path.isfile(
            os.path.join(self.target, 'AVID.MAG.1000.1', 'Documents',
                         'docCollection1', '1', '1.tif')))
        self.assertTrue(os.path.isfile(
            os.path.join(self.target,
                         'AVID.MAG.1000.1', 'Documents', 'docCollection1',
                         '2', '2.tif')))
        self.assertTrue(os.path.isfile(
            os.path.join(self.target, 'AVID.MAG.1000.1', 'Documents',
                         'docCollection2', '3', '3.tif')))
        self.assertTrue(os.path.isfile(
            os.path.join(self.target, 'AVID.MAG.1000.1', 'Documents',
                         'docCollection2', '4', '4.tif')))
        self.assertFalse(os.path.isfile(
            os.path.join(self.target, 'AVID.MAG.1000.1', 'Documents',
                         'docCollection3', '5', '5.tif')))
        self.assertFalse(os.path.isfile(
            os.path.join(self.target, 'AVID.MAG.1000.2', 'Documents',
                         'docCollection3', '5', '5.tif')))

    @mock.patch('tiff.tiffconverter.convert')
    def test_pdf_conversion_succeeds_tiff_conversion_fails(self, mock_convert):
        def tiff_convert_stub(pdf: os.path.abspath,
                              tiff: os.path.abspath) -> bool:
            if os.path.basename(pdf) == 'sample2.pdf':
                return False
            else:
                return true_tiff_convert(pdf, tiff)

        mock_convert.side_effect = tiff_convert_stub

        self.converter.run()
        self.assertTrue(os.path.isfile(
            os.path.join(self.target, 'AVID.MAG.1000.1', 'Documents',
                         'docCollection1', '1', '1.tif')))
        self.assertTrue(os.path.isfile(
            os.path.join(self.target,
                         'AVID.MAG.1000.1', 'Documents', 'docCollection1',
                         '2', '2.tif')))
        self.assertFalse(os.path.isfile(
            os.path.join(self.target, 'AVID.MAG.1000.1', 'Documents',
                         'docCollection1', '3', '3.tif')))

    def test_should_delete_temporary_files_after_conversion(self):
        self.source = os.path.abspath('test/resources/root2')
        self.converter = Converter(self.source, self.target,
                                   self.conversion_dir, 'AVID.MAG.1000',
                                   LocalDocumentManager())
        self.converter.run()
        self.assertEqual([], os.listdir(self.conversion_dir))

    def test_should_clean_conversion_folder_in_constructor(self):
        os.mkdir(os.path.join(self.conversion_dir, 'folder'))
        open(os.path.join(self.conversion_dir, 'file.empty'), 'w').close()
        self.converter = Converter(self.source, self.target,
                                   self.conversion_dir, 'AVID.MAG.1000',
                                   LocalDocumentManager())
        self.assertEqual([], os.listdir(self.conversion_dir))

    def test_should_create_docIndex(self):
        self.converter.run()
        expected = '<docIndex xmlns:xsi="http://www.w3.org/2001/XMLSchema-' \
                   'instance" xmlns="http://www.sa.dk/xmlns/diark/1.0" ' \
                   'xsi:schemaLocation="http://www.sa.dk/xmlns/diark/1.0 ' \
                   '../Schemas/standard/docIndex.xsd"><doc><dID>1</dID>' \
                   '<mID>1</mID><dCf>docCollection1</dCf>' \
                   '<oFn>sample1.docx</oFn>' \
                   '<aFt>tif</aFt></doc><doc><dID>2</dID><mID>1</mID>' \
                   '<dCf>docCollection1</dCf><oFn>sample2.docx</oFn>' \
                   '<aFt>tif</aFt></doc><doc><dID>3</dID>' \
                   '<mID>1</mID><dCf>docCollection1</dCf>' \
                   '<oFn>sample1.docx</oFn>' \
                   '<aFt>tif</aFt></doc><doc><dID>4</dID><mID>1</mID>' \
                   '<dCf>docCollection1</dCf><oFn>sample2.docx</oFn>' \
                   '<aFt>tif</aFt></doc></docIndex>'
        docIndex = os.path.join(self.target, 'AVID.MAG.1000.1', 'Indices',
                                'docIndex.xml')
        self.assertTrue(os.path.isfile(docIndex))
        with open(docIndex, 'r') as docindex:
            content = docindex.read()
        self.assertEqual(expected, content)
