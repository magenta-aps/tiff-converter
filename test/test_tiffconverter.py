import os
import unittest

from tiff.tiffconverter import convert


class TestTiffConverter(unittest.TestCase):

    def test_should_convert_pdf_to_tiff(self):
        self.assertTrue(os.path.isfile(convert('test/resources/sample.pdf')))