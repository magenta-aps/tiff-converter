import unittest

from siarddk.fileindex import FileIndexReader


class TestFileIndexReader(unittest.TestCase):
    def test_should_read_1st_file(self):
        reader = FileIndexReader('test/resources/siarddk/fileIndex.xml')
        fileindex = reader.get_index()
        self.assertEqual(3, len(fileindex))
        f = fileindex[0]
        self.assertEqual('AVID.MAG.1000.1\Indices', f[0].text)
        self.assertEqual('archiveIndex.xml', f[1].text)
        self.assertEqual('16EFBE43D5F278162428A625FF0CA18C', f[2].text)
