import os
import platform
import tempfile
import unittest

from tiff.pdfconverter import MSOfficeToPdfConverter


@unittest.skipIf(platform.system() == 'Linux', 'Since MS Word is Windows only')
class TestMSOfficeToPdfConverter(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.gettempdir()
        self.converter = MSOfficeToPdfConverter(self.temp_dir,
                                                'Word.Application')

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

    def tearDown(self):
        self.converter.close()
