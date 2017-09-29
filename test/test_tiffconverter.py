import os
import unittest
import tempfile

from tiff.tiffconverter import TiffConverter


class TestTiffConverter(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.gettempdir()
        self.converter = TiffConverter(self.temp_dir)

    def test_should_convert_pdf_to_tiff(self):
        tiff = os.path.join(self.temp_dir, 'temp.tif')
        self.assertTrue(
            self.converter.convert('test/resources/sample.pdf', tiff))
        self.assertTrue(os.path.isfile(tiff))
        os.remove(tiff)

    def test_should_return_False_when_conversion_fails(self):
        tiff = os.path.join(self.temp_dir, 'temp.tif')
        self.assertFalse(
            self.converter.convert('test/resources/corrupted.pdf', tiff))
        self.assertFalse(os.path.isfile(tiff))
