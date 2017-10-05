import os
import unittest

from siarddk.fileindex import FileIndex


class TestFileIndexReader(unittest.TestCase):
    def setUp(self):
        self.fileindex = FileIndex(os.path.abspath('test/resources/siarddk'),
            os.path.abspath('test/resources/siarddk/AVID.MAG.1000.1/'
                            'Indices/fileIndex.xml'))

    def test_should_read_1st_file(self):
        index = self.fileindex.get_index()
        self.assertEqual(3, len(index))
        f = index[0]
        self.assertEqual('AVID.MAG.1000.1\Indices', f[0].text)
        self.assertEqual('archiveIndex.xml', f[1].text)
        self.assertEqual('16EFBE43D5F278162428A625FF0CA18C', f[2].text)

    def test_m5dsum_for_sample_jpg_is_f82e6de57911361c8aec8badbad37327(self):
        self.assertEqual(
            'f82e6de57911361c8aec8badbad37327'.upper(),
            self.fileindex._get_md5sum('test/resources/sample.jpg'))

    def test_m5dsum_for_sample_pdf_is_45221934539f968539b6f4b69ae05357(self):
        self.assertEqual(
            '45221934539f968539b6f4b69ae05357'.upper(),
            self.fileindex._get_md5sum('test/resources/sample.pdf'))

    def test_should_add_sample_tif_to_index(self):
        self.fileindex.add(os.path.abspath(
            'test/resources/siarddk/AVID.MAG.1000.1/'
            'Documents/docCollection1/1/1.tif'))
        index = self.fileindex.get_index()
        self.assertEqual(4, len(index))
        f = index[-1]
        self.assertEqual('AVID.MAG.1000.1\\Documents\\docCollection1\\1',
                         f[0].text)
        self.assertEqual('1.tif', f[1].text)
        self.assertEqual('6e95958e99aea72260f8036276d35ad9'.upper(), f[2].text)

    def test_should_add_sample2_tif_to_index(self):
        self.fileindex.add(os.path.abspath(
            'test/resources/siarddk/AVID.MAG.1000.1/'
            'Documents/docCollection1/2/1.tif'))
        index = self.fileindex.get_index()
        self.assertEqual(4, len(index))
        f = index[-1]
        self.assertEqual('AVID.MAG.1000.1\\Documents\\docCollection1\\2',
                         f[0].text)
        self.assertEqual('1.tif', f[1].text)
        self.assertEqual('8bdf61994c761ab179ebc936a356da6e'.upper(), f[2].text)


        # should add root documents to fileIndex correctly
        # new fileIndex.xml should be valid
