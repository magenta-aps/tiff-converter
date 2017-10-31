import os
import shutil
import tempfile
import unittest
import freezegun

from ff.folder import create_doc_folder, rename_old_av_folders


class TestFolder(unittest.TestCase):
    def setUp(self):
        self.target = os.path.join(tempfile.gettempdir(), 'tiff-converter')
        if os.path.isdir(self.target):
            shutil.rmtree(self.target)

    def tearDown(self):
        if os.path.isdir(self.target):
            shutil.rmtree(self.target)

    def test_should_create_AVID_MAG_1000_1_1_1(self):
        self.assertEqual(
            os.path.join(self.target, 'AVID.MAG.1000.1', 'Documents',
                         'docCollection1', '1', '1.tif'),
            create_doc_folder(self.target, 'AVID.MAG.1000', 1, 1, 1))

    def test_should_create_AVID_MAG_1000_3_2_5(self):
        folder = create_doc_folder(self.target, 'AVID.MAG.1000', 3, 2, 5)
        self.assertEqual(
            os.path.join(self.target, 'AVID.MAG.1000.3', 'Documents',
                         'docCollection2', '5', '1.tif'), folder)

    @freezegun.freeze_time('2017-01-01 12:00:00')
    def test_should_rename_AVID_MAG_1000_1(self):
        os.makedirs(os.path.join(self.target, 'AVID.MAG.1000.1'))
        rename_old_av_folders(self.target, 'AVID.MAG.1000')
        self.assertTrue(os.path.isdir(
            os.path.join(self.target, 'AVID.MAG.1000.1_2017-01-01_120000')))

    @freezegun.freeze_time('2017-01-01 12:00:00')
    def test_should_rename_AVID_MAG_2000_2(self):
        os.makedirs(os.path.join(self.target, 'AVID.MAG.2000.2'))
        rename_old_av_folders(self.target, 'AVID.MAG.2000')
        self.assertTrue(os.path.isdir(
            os.path.join(self.target, 'AVID.MAG.2000.2_2017-01-01_120000')))

    @freezegun.freeze_time('2017-01-01 12:00:00')
    def test_should_rename_AVID_MAG_1000_1_and_AVID_MAG_1000_3(self):
        os.makedirs(os.path.join(self.target, 'AVID.MAG.1000.1'))
        os.makedirs(os.path.join(self.target, 'AVID.MAG.1000.3'))
        rename_old_av_folders(self.target, 'AVID.MAG.1000')
        self.assertTrue(os.path.isdir(
            os.path.join(self.target, 'AVID.MAG.1000.1_2017-01-01_120000')))
        self.assertTrue(os.path.isdir(
            os.path.join(self.target, 'AVID.MAG.1000.3_2017-01-01_120000')))
        self.assertFalse(
            os.path.isdir(os.path.join(self.target, 'AVID.MAG.1000.1')))
        self.assertFalse(os.path.isdir(
            os.path.join(self.target, 'AVID.MAG.1000.1')))
