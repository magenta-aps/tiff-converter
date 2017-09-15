import os
import platform
import tempfile
import unittest

from tiff.pdfconverter import DocToPdfConverter


@unittest.skipIf(platform.system() == 'Linux', 'Since MS Word is not present here')
class TestDocToPdfConverter(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.gettempdir()
        self.converter = DocToPdfConverter(self.temp_dir)

    def test_should_return_tmp_doc1_pdf(self):
        doc_path = os.path.abspath('test/resources/demo.docx')
        self.assertEqual(os.path.join(self.temp_dir, 'demo.pdf'), self.converter.convert(doc_path))

    def test_should_return_tmp_doc2_pdf(self):
        doc_path = os.path.abspath('test/resources/demo2.docx')
        self.assertEqual(os.path.join(self.temp_dir, 'demo2.pdf'), self.converter.convert(doc_path))

    def test_should_return_(self):
        doc_path = os.path.abspath('test/resources/corrupted.docx')
        self.assertIsNone(self.converter.convert(doc_path))

    def tearDown(self):
        self.converter.close()