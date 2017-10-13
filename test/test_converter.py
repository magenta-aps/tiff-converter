import os
import platform
import shutil
import tempfile
import unittest
import mock
import freezegun

from siarddk.docmanager import LocalDocumentManager
from tiff.converter import Converter, ComplexConverter
from siarddk.docindex import DocIndexReader


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
                                   os.path.join(self.conversion_dir,
                                                'temp.tif')))

    def test_should_convert_pdf_correctly(self):
        source = os.path.abspath('test/resources/sample.pdf')
        self.assertTrue(
            self.converter.convert(source,
                                   os.path.join(self.conversion_dir,
                                                'temp.tif')))

    def test_should_convert_PDF_correctly(self):
        source = os.path.abspath('test/resources/sample.PDF')
        self.assertTrue(
            self.converter.convert(source,
                                   os.path.join(self.conversion_dir,
                                                'temp.tif')))

    def test_should_convert_doc_correctly(self):
        source = os.path.abspath('test/resources/sample.doc')
        self.assertTrue(
            self.converter.convert(source,
                                   os.path.join(self.conversion_dir,
                                                'temp.tif')))

    def test_should_convert_xls_correctly(self):
        source = os.path.abspath('test/resources/sample.xls')
        self.assertTrue(
            self.converter.convert(source,
                                   os.path.join(self.conversion_dir,
                                                'temp.tif')))

    def test_should_convert_pptx_correctly(self):
        source = os.path.abspath('test/resources/sample.pptx')
        self.assertTrue(
            self.converter.convert(source,
                                   os.path.join(self.conversion_dir,
                                                'temp.tif')))

    def test_should_convert_ppt_correctly(self):
        source = os.path.abspath('test/resources/sample.ppt')
        self.assertTrue(
            self.converter.convert(source,
                                   os.path.join(self.conversion_dir,
                                                'temp.tif')))

    def test_should_convert_jpg_correctly(self):
        source = os.path.abspath('test/resources/sample.jpg')
        self.assertTrue(
            self.converter.convert(source,
                                   os.path.join(self.conversion_dir,
                                                'temp.tif')))


@unittest.skipIf(platform.system() == 'Linux', 'Since MS Word is Windows only')
class TestConverter(unittest.TestCase):
    def setUp(self):
        self.settings = {
            'tiff': {
                'resolution': '150'
            },
            'append': False
        }
        self.source = os.path.abspath('test/resources/root')
        self.target = os.path.join(tempfile.gettempdir(), 'tiff-conversion')
        if os.path.isdir(self.target):
            shutil.rmtree(self.target)
        self.conversion_dir = os.path.join(tempfile.gettempdir(), '_conversion')
        self.converter = Converter(self.source, self.target,
                                   self.conversion_dir, 'AVID.MAG.1000',
                                   LocalDocumentManager(), self.settings)

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
                              LocalDocumentManager(), self.settings)
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
                         '2', '1.tif')))
        self.assertTrue(os.path.isfile(
            os.path.join(self.target, 'AVID.MAG.1000.1', 'Documents',
                         'docCollection1', '3', '1.tif')))
        self.assertTrue(os.path.isfile(
            os.path.join(self.target, 'AVID.MAG.1000.1', 'Documents',
                         'docCollection1', '4', '1.tif')))
        self.assertFalse(os.path.isfile(
            os.path.join(self.target, 'AVID.MAG.1000.1', 'Documents',
                         'docCollection1', '5', '1.tif')))

    def test_should_convert_root_folder_correctly_when_MAX_2(self):
        self.converter.docmanager.MAX = 2
        self.converter.run()
        self.assertTrue(os.path.isfile(
            os.path.join(self.target, 'AVID.MAG.1000.1', 'Documents',
                         'docCollection1', '1', '1.tif')))
        self.assertTrue(os.path.isfile(
            os.path.join(self.target,
                         'AVID.MAG.1000.1', 'Documents', 'docCollection1',
                         '2', '1.tif')))
        self.assertTrue(os.path.isfile(
            os.path.join(self.target, 'AVID.MAG.1000.1', 'Documents',
                         'docCollection2', '3', '1.tif')))
        self.assertTrue(os.path.isfile(
            os.path.join(self.target, 'AVID.MAG.1000.1', 'Documents',
                         'docCollection2', '4', '1.tif')))
        self.assertFalse(os.path.isfile(
            os.path.join(self.target, 'AVID.MAG.1000.1', 'Documents',
                         'docCollection3', '5', '1.tif')))
        self.assertFalse(os.path.isfile(
            os.path.join(self.target, 'AVID.MAG.1000.2', 'Documents',
                         'docCollection3', '5', '1.tif')))

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
                              LocalDocumentManager(), self.settings)
        converter.run()
        self.converter.close()
        self.assertEqual([], os.listdir(self.conversion_dir))

    def test_should_clean_conversion_folder_in_constructor(self):
        os.mkdir(os.path.join(self.conversion_dir, 'folder'))
        open(os.path.join(self.conversion_dir, 'file.empty'), 'w').close()
        converter = Converter(self.source, self.target,
                              self.conversion_dir, 'AVID.MAG.1000',
                              LocalDocumentManager(), self.settings)
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

    def test_should_store_settings(self):
        self.assertTrue(hasattr(self.converter, 'settings'))
        self.assertEqual('150', self.converter.settings['tiff']['resolution'])
        self.converter.close()

    def test_should_create_target_folder_in_constructor(self):
        self.assertTrue(os.path.isdir(self.target))
        self.converter.close()

    @freezegun.freeze_time('2017-01-01 12:00:00')
    def test_should_rename_target_folder_if_exists(self):
        path_to_rename = os.path.join(self.target, 'AVID.MAG.1000.1')
        os.makedirs(path_to_rename)
        self.source = os.path.abspath('test/resources/root2')
        converter = Converter(self.source, self.target,
                              self.conversion_dir, 'AVID.MAG.1000',
                              LocalDocumentManager(), self.settings)
        converter.close()
        self.converter.close()
        self.assertFalse(os.path.isdir(path_to_rename))
        self.assertTrue(os.path.isdir(
            os.path.join(self.target, 'AVID.MAG.1000.1_2017-01-01_120000')))


@unittest.skipIf(platform.system() == 'Linux', 'Since MS Word is Windows only')
class TestConverterAppend(unittest.TestCase):
    def test_should_append_new_file_to_an_existing_av(self):
        settings = {
            'tiff': {
                'resolution': '150'
            },
            'append': False
        }
        source = os.path.abspath('test/resources/root')
        target = os.path.join(tempfile.gettempdir(), 'tiff-conversion')
        if os.path.isdir(target):
            shutil.rmtree(target)
        conversion_dir = os.path.join(tempfile.gettempdir(), '_conversion')
        converter = Converter(source, target, conversion_dir, 'AVID.MAG.1000',
                              LocalDocumentManager(), settings)
        converter.run()

        # Add new file to the existing AV

        settings['append'] = True
        source = os.path.abspath('test/resources/root3')
        docindex_reader = DocIndexReader(
            os.path.join(target, 'AVID.MAG.1000.1', 'Indices', 'docIndex.xml'))
        mID, dCf, dID = docindex_reader.get_ids()
        docindex = docindex_reader.get_index()

        converter = Converter(source, target, conversion_dir, 'AVID.MAG.1000',
                              LocalDocumentManager(mID, dCf, dID), settings,
                              docindex)
        converter.run()

        # Check that the tiffs exist

        self.assertTrue(os.path.isfile(
            os.path.join(target, 'AVID.MAG.1000.1', 'Documents',
                         'docCollection1', '1', '1.tif')))
        self.assertTrue(os.path.isfile(
            os.path.join(target,
                         'AVID.MAG.1000.1', 'Documents', 'docCollection1',
                         '2', '1.tif')))
        self.assertTrue(os.path.isfile(
            os.path.join(target, 'AVID.MAG.1000.1', 'Documents',
                         'docCollection1', '3', '1.tif')))
        self.assertTrue(os.path.isfile(
            os.path.join(target, 'AVID.MAG.1000.1', 'Documents',
                         'docCollection1', '4', '1.tif')))
        self.assertTrue(os.path.isfile(
            os.path.join(target, 'AVID.MAG.1000.1', 'Documents',
                         'docCollection1', '5', '1.tif')))

        # Check docIndex.xml

        self.assertEqual(5, len(docindex))
        for i in range(1, 5):
            doc = docindex[i - 1]
            self.assertEqual(str(i), doc[0].text)
            self.assertEqual('1', doc[1].text)
            self.assertEqual('docCollection1', doc[2].text)
            self.assertEqual('sample%s.docx' % (1 if i % 2 == 1 else 2),
                             doc[3].text)
            self.assertEqual('tif', doc[4].text)
        doc = docindex[4]
        self.assertEqual('5', doc[0].text)
        self.assertEqual('1', doc[1].text)
        self.assertEqual('docCollection1', doc[2].text)
        self.assertEqual('spreadsheet1.xlsx', doc[3].text)
        self.assertEqual('tif', doc[4].text)

        if os.path.isdir(target):
            shutil.rmtree(target)
        if os.path.isdir(conversion_dir):
            shutil.rmtree(conversion_dir)
