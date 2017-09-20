import os
import unittest
import tempfile

from tiff.tiffconverter import convert


class TestTiffConverter(unittest.TestCase):

    def test_should_convert_pdf_to_tiff(self):
        temp_dir = tempfile.gettempdir()
        tiff = os.path.join(temp_dir, 'temp.tif')
        self.assertTrue(convert('test/resources/sample.pdf', tiff))
        self.assertTrue(os.path.isfile(tiff))
        os.remove(tiff)

    def test_should_return_False_when_conversion_fails(self):
        temp_dir = tempfile.gettempdir()
        tiff = os.path.join(temp_dir, 'temp.tif')
        self.assertFalse(convert('test/resources/corrupted.pdf', tiff))
        self.assertFalse(os.path.isfile(tiff))
