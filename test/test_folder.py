import os
import shutil
import tempfile
import unittest

from ff.folder import create_doc_folder


class TestFolder(unittest.TestCase):
    def setUp(self):
        self.target = os.path.join(tempfile.gettempdir(), 'tiff-converter')
        if os.path.isdir(self.target):
            shutil.rmtree(self.target)

    def tearDown(self):
        if os.path.isdir(self.target):
            shutil.rmtree(self.target)

    def test_should_create_AVID_MAG_1000_1_1_1(self):
        create_doc_folder(self.target, 'AVID.MAG.1000', 1, 1, 1)
        self.assertTrue(
            os.path.isdir(
                os.path.join(self.target, 'AVID.MAG.1000.1', 'Documents',
                             'docCollection1', '1')))

    def test_should_create_AVID_MAG_1000_3_2_5(self):
        folder = create_doc_folder(self.target, 'AVID.MAG.1000', 3, 2, 5)
        self.assertTrue(
            os.path.isdir(
                os.path.join(self.target, 'AVID.MAG.1000.3', 'Documents',
                             'docCollection2', '5')))
        self.assertEqual(
            os.path.join(self.target, 'AVID.MAG.1000.3', 'Documents',
                         'docCollection2', '5'), folder)
