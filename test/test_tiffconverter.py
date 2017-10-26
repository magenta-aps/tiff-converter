import os
import shutil
import unittest
import tempfile

import mock

from tiff.tiffconverter import TiffConverter


class TestTiffConverter(unittest.TestCase):
    def setUp(self):
        self.temp_dir = os.path.join(tempfile.gettempdir(), '_conversion')
        if not os.path.isdir(self.temp_dir):
            os.makedirs(self.temp_dir)
        self.converter = TiffConverter(self.temp_dir)
        self.tiff = os.path.join(self.temp_dir, 'temp.tif')

    def tearDown(self):
        if os.path.isdir(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def test_should_convert_pdf_to_tiff(self):
        self.assertTrue(
            self.converter.pdf_convert('test/resources/sample.pdf', self.tiff))
        self.assertTrue(os.path.isfile(self.tiff))

    def test_should_return_False_when_conversion_fails(self):
        self.assertFalse(
            self.converter.pdf_convert('test/resources/corrupted.pdf',
                                       self.tiff))
        self.assertFalse(os.path.isfile(self.tiff))

    def test_should_create_tiff_folder(self):
        tiff_dir = os.path.join(self.temp_dir, 'folder')
        self.assertTrue(
            self.converter.pdf_convert('test/resources/sample.pdf',
                                       os.path.join(tiff_dir, 'temp.tif')))
        self.assertTrue(os.path.isdir(tiff_dir))

    @mock.patch('tiff.tiffconverter.os.path.isfile')
    def test_remove_folder_if_conversion_fails(self, mock):
        tiff_dir = os.path.join(self.temp_dir, 'folder')
        tiff_file = os.path.join(tiff_dir, 'temp.tif')

        def remove_tiff_file(x):
            os.remove(tiff_file)
            return False

        mock.side_effect = remove_tiff_file

        self.assertFalse(
            self.converter.image_magick_convert(
                'test/resources/sample.tiff', tiff_file))
        self.assertFalse(os.path.isdir(tiff_dir))

    @mock.patch('tiff.tiffconverter.os.path.isfile')
    def test_only_remove_folder_if_empty(self, mock):
        tiff_dir = os.path.join(self.temp_dir, 'folder')
        tiff_file = os.path.join(tiff_dir, 'temp.tif')

        os.mkdir(tiff_dir)
        shutil.copy(os.path.abspath('test/resources/sample.pdf'),
                    os.path.join(tiff_dir, 'sample.pdf'))

        def remove_tiff_file(x):
            os.remove(tiff_file)
            return False

        mock.side_effect = remove_tiff_file

        self.assertFalse(
            self.converter.image_magick_convert(
                'test/resources/sample.tiff', tiff_file))
        self.assertTrue(os.path.isdir(tiff_dir))
