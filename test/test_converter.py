import os
import platform
import shutil
import tempfile
import unittest
import mock

from siarddk.docmanager import LocalDocumentManager
from tiff.converter import Converter, ComplexConverter


@unittest.skipIf(platform.system() == 'Linux', 'Since MS Word is Windows only')
class TestComplexConverter(unittest.TestCase):
    def setUp(self):
        self.conversion_dir = os.path.join(tempfile.gettempdir(), '_conversion')
        if not os.path.isdir(self.conversion_dir):
            os.makedirs(self.conversion_dir)
        self.converter = ComplexConverter(self.conversion_dir)

    def tearDown(self):
        self.converter.close()
        if os.path.isdir(self.conversion_dir):
            shutil.rmtree(self.conversion_dir)

    def test_should_convert_xlsx_correctly(self):
        source = os.path.abspath('test/resources/root3/spreadsheet1.xlsx')
        self.assertTrue(
            self.converter.convert(source,
                              os.path.join(self.conversion_dir, 'temp.tif')))

    def test_should_convert_pdf_correctly(self):
        source = os.path.abspath('test/resources/sample.pdf')
        self.assertTrue(
            self.converter.convert(source,
                              os.path.join(self.conversion_dir, 'temp.tif')))

    def test_should_convert_PDF_correctly(self):
        source = os.path.abspath('test/resources/sample.PDF')
        self.assertTrue(
            self.converter.convert(source,
                              os.path.join(self.conversion_dir, 'temp.tif')))

    def test_should_convert_doc_correctly(self):
        source = os.path.abspath('test/resources/sample.doc')
        self.assertTrue(
            self.converter.convert(source,
                              os.path.join(self.conversion_dir, 'temp.tif')))

    def test_should_convert_xls_correctly(self):
        source = os.path.abspath('test/resources/sample.xls')
        self.assertTrue(
            self.converter.convert(source,
                              os.path.join(self.conversion_dir, 'temp.tif')))

    def test_should_convert_pptx_correctly(self):
        source = os.path.abspath('test/resources/sample.pptx')
        self.assertTrue(
            self.converter.convert(source,
                              os.path.join(self.conversion_dir, 'temp.tif')))

    def test_should_convert_ppt_correctly(self):
        source = os.path.abspath('test/resources/sample.ppt')
        self.assertTrue(
            self.converter.convert(source,
                              os.path.join(self.conversion_dir, 'temp.tif')))

    def test_should_convert_jpg_correctly(self):
        source = os.path.abspath('test/resources/sample.jpg')
        self.assertTrue(
            self.converter.convert(source,
                              os.path.join(self.conversion_dir, 'temp.tif')))


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
        self.converter.close()

    def test_should_store_target_in_attribute(self):
        self.assertEqual(self.target, self.converter.target)
        self.converter.close()

    def test_should_store_temp_conversion_folder(self):
        self.assertEqual(self.conversion_dir, self.converter.conversion_dir)
        self.converter.close()

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
        converter = Converter(self.source, self.target,
                              self.conversion_dir, 'AVID.XYZ.2000',
                              LocalDocumentManager())
        converter.run()
        self.converter.close()
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

    @mock.patch('tiff.tiffconverter.TiffConverter.pdf_convert')
    def test_pdf_conversion_succeeds_tiff_conversion_fails(self, mock_convert):
        mock_convert.side_effect = [True, False, True, False]

        self.converter.run()

        docIndex = self.converter.docindex_builder.build()
        doc1 = docIndex[0]
        doc2 = docIndex[1]

        self.assertEqual(2, len(docIndex))

        self.assertEqual('1', doc1[0].text)
        self.assertEqual('1', doc1[1].text)
        self.assertEqual('docCollection1', doc1[2].text)
        self.assertEqual('sample1.docx', doc1[3].text)
        self.assertEqual('tif', doc1[4].text)

        self.assertEqual('2', doc2[0].text)
        self.assertEqual('1', doc2[1].text)
        self.assertEqual('docCollection1', doc2[2].text)
        self.assertEqual('sample1.docx', doc2[3].text)
        self.assertEqual('tif', doc1[4].text)

    def test_should_delete_temporary_files_after_conversion(self):
        self.source = os.path.abspath('test/resources/root2')
        converter = Converter(self.source, self.target,
                              self.conversion_dir, 'AVID.MAG.1000',
                              LocalDocumentManager())
        converter.run()
        self.converter.close()
        self.assertEqual([], os.listdir(self.conversion_dir))

    def test_should_clean_conversion_folder_in_constructor(self):
        os.mkdir(os.path.join(self.conversion_dir, 'folder'))
        open(os.path.join(self.conversion_dir, 'file.empty'), 'w').close()
        converter = Converter(self.source, self.target,
                              self.conversion_dir, 'AVID.MAG.1000',
                              LocalDocumentManager())
        converter.close()
        self.converter.close()
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
