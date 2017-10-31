import os
import platform
import shutil
import tempfile
import unittest
import mock
import freezegun

from tiff.converter import Converter, ComplexConverter
from siarddk.docindex import DocIndexHandler
from tiff.filehandler import LocalFilePathStrategy
from ff.folder import LocalInitializationStrategy


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

    def test_should_convert_png_correctly(self):
        source = os.path.abspath('test/resources/sample.png')
        self.assertTrue(
            self.converter.convert(source,
                                   os.path.join(self.conversion_dir,
                                                'temp.tif')))

    def test_should_convert_bmp_correctly(self):
        source = os.path.abspath('test/resources/sample.bmp')
        self.assertTrue(
            self.converter.convert(source,
                                   os.path.join(self.conversion_dir,
                                                'temp.tif')))

    def test_should_convert_gif_correctly(self):
        source = os.path.abspath('test/resources/sample.gif')
        self.assertTrue(
            self.converter.convert(source,
                                   os.path.join(self.conversion_dir,
                                                'temp.tif')))

    def test_should_convert_tif_correctly(self):
        source = os.path.abspath(
            'test/resources/siarddk/AVID.MAG.1000.1/'
            'Documents/docCollection1/1/1.tif')
        self.assertTrue(
            self.converter.convert(source,
                                   os.path.join(self.conversion_dir,
                                                'temp.tif')))

    def test_should_convert_tiff_correctly(self):
        source = os.path.abspath('test/resources/sample.tiff')
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
            'append': False,
            'in-place': False
        }
        self.source = os.path.abspath('test/resources/root')
        self.target = os.path.join(tempfile.gettempdir(), 'tiff-conversion')
        self.name = 'AVID.MAG.1000'
        if os.path.isdir(self.target):
            shutil.rmtree(self.target)
        self.conversion_dir = os.path.join(tempfile.gettempdir(), '_conversion')
        self.converter = Converter(self.source, self.target,
                                   self.conversion_dir,
                                   self.name,
                                   self.settings,
                                   LocalFilePathStrategy(self.source),
                                   LocalInitializationStrategy(),
                                   DocIndexHandler(self.target, self.name))

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

    def test_should_store_filepathstrategy_in_attribute(self):
        self.assertEqual(
            'LocalFilePathStrategy',
            self.converter.file_path_strategy.__class__.__name__)
        self.converter.close()

    def test_should_store_initializationstrategy_in_attribute(self):
        self.assertEqual(
            'LocalInitializationStrategy',
            self.converter.initialization_strategy.__class__.__name__)
        self.converter.close()

    def test_should_create_folders_AVID_MAG_1000_1_and_Document(self):
        self.converter.run()
        self.assertTrue(os.path.isdir(
            os.path.join(self.target, 'AVID.MAG.1000.1', 'Documents')))

    def test_should_create_folder_AVID_MAG_1000_2_and_Documents(self):
        # self.converter.docmanager.MAX = 2
        self.converter.docindex_handler.docmanager.MAX = 2
        self.converter.run()
        self.assertTrue(os.path.isdir(
            os.path.join(self.target, 'AVID.MAG.1000.2', 'Documents')))

    def test_folder_docCollection1_should_exists_after_file_conversion(self):
        self.converter.run()
        self.assertTrue(os.path.isdir(
            os.path.join(self.target, 'AVID.MAG.1000.1', 'Documents',
                         'docCollection1')))

    def test_folder_docCollection2_should_exists_after_file_conversion2(self):
        # self.converter.docmanager.MAX = 2
        self.converter.docindex_handler.docmanager.MAX = 2
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
                              self.settings, LocalFilePathStrategy(self.source),
                              LocalInitializationStrategy(),
                              DocIndexHandler(self.target, 'AVID.XYZ.2000'))
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
                         'docCollection1', '4', '1.tif')))
        self.assertTrue(os.path.isfile(
            os.path.join(self.target, 'AVID.MAG.1000.1', 'Documents',
                         'docCollection1', '5', '1.tif')))
        self.assertFalse(os.path.isdir(
            os.path.join(self.target, 'AVID.MAG.1000.1', 'Documents',
                         'docCollection1', '6')))
        self.assertFalse(os.path.isfile(
            os.path.join(self.target, 'AVID.MAG.1000.1', 'Documents',
                         'docCollection1', '6', '1.tif')))

    def test_should_convert_root_folder_correctly_when_MAX_2(self):
        self.converter.docindex_handler.docmanager.MAX = 2
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
                         'docCollection2', '4', '1.tif')))
        self.assertTrue(os.path.isfile(
            os.path.join(self.target, 'AVID.MAG.1000.2', 'Documents',
                         'docCollection3', '5', '1.tif')))
        self.assertFalse(os.path.isfile(
            os.path.join(self.target, 'AVID.MAG.1000.2', 'Documents',
                         'docCollection3', '6', '1.tif')))
        self.assertFalse(os.path.isfile(
            os.path.join(self.target, 'AVID.MAG.1000.2', 'Documents',
                         'docCollection3', '6', '1.tif')))

    @mock.patch('tiff.tiffconverter.TiffConverter.pdf_convert')
    def test_pdf_conversion_succeeds_tiff_conversion_fails(self, mock_convert):
        mock_convert.side_effect = [True, False, True, False]

        self.converter.run()

        docIndex = self.converter.docindex_handler.build()
        doc1 = docIndex[0]
        doc2 = docIndex[1]

        self.assertEqual(2, len(docIndex))

        self.assertEqual('1', doc1[0].text)
        self.assertEqual('1', doc1[1].text)
        self.assertEqual('docCollection1', doc1[2].text)
        self.assertEqual('sample1.docx', doc1[3].text)
        self.assertEqual('tif', doc1[4].text)

        self.assertEqual('4', doc2[0].text)
        self.assertEqual('1', doc2[1].text)
        self.assertEqual('docCollection1', doc2[2].text)
        self.assertEqual('sample1.docx', doc2[3].text)
        self.assertEqual('tif', doc1[4].text)

    def test_should_delete_temporary_files_after_conversion(self):
        self.source = os.path.abspath('test/resources/root2')
        converter = Converter(self.source, self.target,
                              self.conversion_dir, 'AVID.MAG.1000',
                              self.settings, LocalFilePathStrategy(self.source),
                              LocalInitializationStrategy(),
                              DocIndexHandler(self.target, 'AVID.MAG.1000'))
        converter.run()
        self.converter.close()
        self.assertEqual([], os.listdir(self.conversion_dir))

    def test_should_clean_conversion_folder_in_constructor(self):
        os.mkdir(os.path.join(self.conversion_dir, 'folder'))
        open(os.path.join(self.conversion_dir, 'file.empty'), 'w').close()
        converter = Converter(self.source, self.target,
                              self.conversion_dir, 'AVID.MAG.1000',
                              self.settings, LocalFilePathStrategy(self.source),
                              LocalInitializationStrategy(),
                              DocIndexHandler('', ''))
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
                   '<aFt>tif</aFt></doc><doc><dID>4</dID>' \
                   '<mID>1</mID><dCf>docCollection1</dCf>' \
                   '<oFn>sample1.docx</oFn>' \
                   '<aFt>tif</aFt></doc><doc><dID>5</dID><mID>1</mID>' \
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

    def test_should_create_target_folder(self):
        self.source = os.path.abspath('test/resources/root3')
        converter = Converter(self.source, self.target,
                              self.conversion_dir, 'AVID.MAG.1000',
                              self.settings, LocalFilePathStrategy(self.source),
                              LocalInitializationStrategy(),
                              DocIndexHandler(self.target, 'AVID.MAG.1000'))
        converter.run()
        self.converter.close()
        self.assertTrue(os.path.isdir(self.target))

    @freezegun.freeze_time('2017-01-01 12:00:00')
    def test_should_rename_target_folder_if_exists(self):
        path_to_rename = os.path.join(self.target, 'AVID.MAG.1000.1')
        os.makedirs(path_to_rename)
        self.source = os.path.abspath('test/resources/root2')
        converter = Converter(self.source, self.target,
                              self.conversion_dir, 'AVID.MAG.1000',
                              self.settings, LocalFilePathStrategy(self.source),
                              LocalInitializationStrategy(),
                              DocIndexHandler(self.target, 'AVID.MAG.1000'))
        converter.run()
        self.converter.close()
        self.assertTrue(os.path.isdir(
            os.path.join(self.target, 'AVID.MAG.1000.1_2017-01-01_120000')))


@unittest.skipIf(platform.system() == 'Linux', 'Since MS Word is Windows only')
class TestConverterAppend(unittest.TestCase):
    def test_should_append_new_file_to_an_existing_av(self):
        settings = {
            'tiff': {
                'resolution': '150'
            },
            'append': False,
            'in-place': False
        }
        source = os.path.abspath('test/resources/root')
        target = os.path.join(tempfile.gettempdir(), 'tiff-conversion')
        name = 'AVID.MAG.1000'
        if os.path.isdir(target):
            shutil.rmtree(target)
        conversion_dir = os.path.join(tempfile.gettempdir(), '_conversion')
        converter = Converter(source, target, conversion_dir,
                              name,
                              settings,
                              LocalFilePathStrategy(source),
                              LocalInitializationStrategy(),
                              DocIndexHandler(target, name))

        converter.run()

        # Add new file to the existing AV

        settings['append'] = True
        source = os.path.abspath('test/resources/root3')
        converter = Converter(source, target, conversion_dir,
                              name,
                              settings,
                              LocalFilePathStrategy(source),
                              LocalInitializationStrategy(),
                              DocIndexHandler(target, name))

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
                         'docCollection1', '4', '1.tif')))
        self.assertTrue(os.path.isfile(
            os.path.join(target, 'AVID.MAG.1000.1', 'Documents',
                         'docCollection1', '5', '1.tif')))
        self.assertTrue(os.path.isfile(
            os.path.join(target, 'AVID.MAG.1000.1', 'Documents',
                         'docCollection1', '6', '1.tif')))

        # Check docIndex.xml

        docindex_handler = DocIndexHandler(target, name)
        docindex = docindex_handler.get_index()

        self.assertEqual(5, len(docindex))

        doc = docindex[0]
        self.assertEqual('1', doc[0].text)
        self.assertEqual('1', doc[1].text)
        self.assertEqual('docCollection1', doc[2].text)
        self.assertEqual('sample1.docx', doc[3].text)
        self.assertEqual('tif', doc[4].text)

        doc = docindex[1]
        self.assertEqual('2', doc[0].text)
        self.assertEqual('1', doc[1].text)
        self.assertEqual('docCollection1', doc[2].text)
        self.assertEqual('sample2.docx', doc[3].text)
        self.assertEqual('tif', doc[4].text)

        doc = docindex[2]
        self.assertEqual('4', doc[0].text)
        self.assertEqual('1', doc[1].text)
        self.assertEqual('docCollection1', doc[2].text)
        self.assertEqual('sample1.docx', doc[3].text)
        self.assertEqual('tif', doc[4].text)

        doc = docindex[3]
        self.assertEqual('5', doc[0].text)
        self.assertEqual('1', doc[1].text)
        self.assertEqual('docCollection1', doc[2].text)
        self.assertEqual('sample2.docx', doc[3].text)
        self.assertEqual('tif', doc[4].text)

        doc = docindex[4]
        self.assertEqual('6', doc[0].text)
        self.assertEqual('1', doc[1].text)
        self.assertEqual('docCollection1', doc[2].text)
        self.assertEqual('spreadsheet1.xlsx', doc[3].text)
        self.assertEqual('tif', doc[4].text)

        if os.path.isdir(target):
            shutil.rmtree(target)
        if os.path.isdir(conversion_dir):
            shutil.rmtree(conversion_dir)


# @unittest.skipIf(platform.system() == 'Linux', 'Since MS Word is Windows only')
# class TestSourceEqualsTargetConversion(unittest.TestCase):
#     """
#     Testing in-place conversion
#     """
#
#     def setUp(self):
#         self.settings = {
#             'tiff': {
#                 'resolution': '150'
#             },
#             'append': False,
#             'in-place': True
#         }
#         self.folder = os.path.join(tempfile.gettempdir(), 'tiff-conversion')
#         if os.path.isdir(self.folder):
#             shutil.rmtree(self.folder)
#         self.source = self.folder
#
#         # TODO: clean this up a bit...
#         shutil.copytree(
#             os.path.abspath('test/resources/siarddk2/AVID.MAG.1000.1/'),
#             os.path.join(self.folder, 'AVID.MAG.1000.1'))
#         shutil.copytree(
#             os.path.abspath('test/resources/siarddk2/AVID.MAG.1000.2/'),
#             os.path.join(self.folder, 'AVID.MAG.1000.2'))
#
#         self.conversion_dir = os.path.join(tempfile.gettempdir(), '_conversion')
#         self.converter = Converter(self.source, self.folder,
#                                    self.conversion_dir, 'AVID.MAG.1000',
#                                    self.settings,
#                                    LocalFilePathStrategy(self.source),
#                                    LocalInitializationStrategy(),
#                                    DocIndexHandler(self.folder, 'AVID.MAG.1000'))
#
#     def tearDown(self):
#         if os.path.isdir(self.folder):
#             shutil.rmtree(self.folder)
#         if os.path.isdir(self.conversion_dir):
#             shutil.rmtree(self.conversion_dir)
#
#     def test_sample_tif_should_exist_after_conversion(self):
#         self.converter.run()
#
#         self.assertTrue(os.path.isfile(
#             os.path.join(self.folder, 'AVID.MAG.1000.1', 'Documents',
#                          'docCollection1', '1', '1.tif')))
#         self.assertFalse(os.path.isfile(
#             os.path.join(self.folder, 'AVID.MAG.1000.1', 'Documents',
#                          'docCollection1', '1', 'sample.doc')))
#         self.assertTrue(os.path.isfile(
#             os.path.join(self.folder, 'AVID.MAG.1000.1', 'Documents',
#                          'docCollection1', '2', '1.tif')))
#         self.assertFalse(os.path.isfile(
#             os.path.join(self.folder, 'AVID.MAG.1000.1', 'Documents',
#                          'docCollection1', '2', 'sample.doc')))
#
#         self.assertTrue(os.path.isfile(
#             os.path.join(self.folder, 'AVID.MAG.1000.2', 'Documents',
#                          'docCollection2', '3', '1.tif')))
#         self.assertFalse(os.path.isfile(
#             os.path.join(self.folder, 'AVID.MAG.1000.2', 'Documents',
#                          'docCollection2', '3', 'sample.doc')))
#         self.assertTrue(os.path.isfile(
#             os.path.join(self.folder, 'AVID.MAG.1000.2', 'Documents',
#                          'docCollection2', '4', '1.tif')))
#         self.assertFalse(os.path.isfile(
#             os.path.join(self.folder, 'AVID.MAG.1000.2', 'Documents',
#                          'docCollection2', '4', 'sample.doc')))
#
#     @mock.patch('tiff.pdfconverter.MSOfficeToPdfConverter.convert')
#     def test_should_not_remove_sample_doc_when_conversion_fails(self, mock):
#         mock.return_value = None
#         self.converter.run()
#
#         self.assertFalse(os.path.isfile(
#             os.path.join(self.folder, 'AVID.MAG.1000.1', 'Documents',
#                          'docCollection1', '1', '1.tif')))
#         self.assertTrue(os.path.isfile(
#             os.path.join(self.folder, 'AVID.MAG.1000.1', 'Documents',
#                          'docCollection1', '1', 'sample.doc')))
#         self.assertTrue(os.path.isfile(
#             os.path.join(self.folder, 'AVID.MAG.1000.1', 'Documents',
#                          'docCollection1', '2', '1.tif')))
#         self.assertFalse(os.path.isfile(
#             os.path.join(self.folder, 'AVID.MAG.1000.1', 'Documents',
#                          'docCollection1', '2', 'sample.doc')))
#
#         self.assertFalse(os.path.isfile(
#             os.path.join(self.folder, 'AVID.MAG.1000.2', 'Documents',
#                          'docCollection2', '3', '1.tif')))
#         self.assertTrue(os.path.isfile(
#             os.path.join(self.folder, 'AVID.MAG.1000.2', 'Documents',
#                          'docCollection2', '3', 'sample.doc')))
#         self.assertTrue(os.path.isfile(
#             os.path.join(self.folder, 'AVID.MAG.1000.2', 'Documents',
#                          'docCollection2', '4', '1.tif')))
#         self.assertFalse(os.path.isfile(
#             os.path.join(self.folder, 'AVID.MAG.1000.2', 'Documents',
#                          'docCollection2', '4', 'sample.doc')))
