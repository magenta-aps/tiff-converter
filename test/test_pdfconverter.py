import unittest

from tiff.pdfconverter import DocToPdfConverter


class TestDocToPdfConverter(unittest.TestCase):

    def test_should_return_tmp_doc1_pdf(self):
        conv = DocToPdfConverter()
        self.assertEqual('/tmp/doc1.pdf', conv.convert('doc1.docx'))

    # def test_should_return_tmp_doc2_pdf(self):
    #     conv = DocToPdfConverter()
    #     self.assertEqual('/tmp/doc2.pdf', conv.convert('doc2.docx'))