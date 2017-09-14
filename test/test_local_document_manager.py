import unittest

from siarddk import docmanager


class TestLocalDocumentManager(unittest.TestCase):

    def setUp(self):
        self.d = docmanager.LocalDocumentManager()

    def test_should_return_111_for_first_doc(self):
        self.assertEqual((1, 1, 1), self.d.get_location())

    def test_should_return_112_for_second_doc(self):
        self.add(1)
        self.assertEqual((1, 1, 2), self.d.get_location())

    def test_should_return_121_for_10001st_doc(self):
        self.add(10000)
        self.assertEqual((1, 2, 1), self.d.get_location())

    def test_should_return_132_for_20002nd_doc(self):
        self.add(20001)
        self.assertEqual((1, 3, 2), self.d.get_location())

    def test_should_return_211_for_next_doc_when_dCf_is_10000(self):
        self.d.dID = 10000
        self.d.dCf = 10000
        self.assertEqual((2, 1, 1), self.d.get_location())

    def add(self, n):
        """
        Add n docs to Documents
        """
        for i in range(n):
            self.d.get_location()