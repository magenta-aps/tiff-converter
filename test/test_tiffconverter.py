import os
import unittest
import tempfile

from tiff.tiffconverter import convert


class TestTiffConverter(unittest.TestCase):
    def test_should_convert_pdf_to_tiff(self):
        # Check that extension is tif

        temp_dir = tempfile.gettempdir()
        tiff = os.path.join(temp_dir, 'temp.tif')
        convert('test/resources/sample.pdf', tiff)
        self.assertTrue(os.path.isfile(tiff))

        # Clean tempdir
