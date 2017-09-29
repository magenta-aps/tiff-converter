import os
import platform
import shutil
import tempfile
import unittest

from tiff.pdfconverter import MSOfficeToPdfConverter


@unittest.skipIf(platform.system() == 'Linux', 'Since MS Word is Windows only')
class TestMSOfficeToPdfConverter(unittest.TestCase):
    def setUp(self):
        self.temp_dir = os.path.join(tempfile.gettempdir(), '_conversion')
        if not os.path.isdir(self.temp_dir):
            os.makedirs(self.temp_dir)
        self.converter = MSOfficeToPdfConverter(self.temp_dir,
                                                MSOfficeToPdfConverter.WORD)

    def tearDown(self):
        self.converter.close()
        if os.path.isdir(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def test_should_return_tmp_doc1_pdf(self):
        doc_path = os.path.abspath('test/resources/root/folder1/sample1.docx')
        self.assertEqual(os.path.join(self.temp_dir, 'sample1.pdf'),
                         self.converter.convert(doc_path))

    def test_should_return_tmp_doc2_pdf(self):
        doc_path = os.path.abspath('test/resources/root/folder1/sample2.docx')
        self.assertEqual(os.path.join(self.temp_dir, 'sample2.pdf'),
                         self.converter.convert(doc_path))

    def test_should_return_(self):
        doc_path = os.path.abspath(
            'test/resources/root/folder1/sample3_corrupted.docx')
        self.assertIsNone(self.converter.convert(doc_path))

    def test_should_raise_exception_when_file_does_not_exists(self):
        doc_path = os.path.abspath('path/to/no/file')
        self.assertRaises(FileNotFoundError, self.converter.convert, doc_path)

    def test_should_store_powerpoint_app_string(self):
        self.assertEqual('Powerpoint.Application',
                         MSOfficeToPdfConverter.POWERPOINT)

    def test_should_return_temp_pptx_pdf(self):
        converter = MSOfficeToPdfConverter(self.temp_dir,
                                           MSOfficeToPdfConverter.POWERPOINT)
        pptx_path = os.path.abspath('test/resources/sample.pptx')
        self.assertEqual(os.path.join(self.temp_dir, 'sample.pdf'),
                         converter.convert(pptx_path))
        converter.close()


@unittest.skipIf(platform.system() == 'Linux', 'Since MS Word is Windows only')
class TestPdfConverter(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.gettempdir()
        self.converter = MSOfficeToPdfConverter(self.temp_dir,
                                                MSOfficeToPdfConverter.EXCEL)

    def test_should_return_tmp_xls1_pdf(self):
        xls_path = os.path.abspath('test/resources/root3/spreadsheet1.xlsx')
        self.assertEqual(os.path.join(self.temp_dir, 'spreadsheet1.pdf'),
                         self.converter.convert(xls_path))
