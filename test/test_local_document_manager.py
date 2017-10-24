import unittest

from siarddk import docmanager


class TestLocalDocumentManager(unittest.TestCase):

    def setUp(self):
        self.d = docmanager.LocalDocumentManager(False)
        self.d.MAX = 2   # To make it easier to test

    def test_should_return_111_for_1st_doc(self):
        self.assertEqual((1, 1, 1), self.d.get_location())

    def test_should_return_112_for_2nd_doc(self):
        self.add(1)
        self.assertEqual((1, 1, 2), self.d.get_location())

    def test_should_return_123_for_3rd_doc(self):
        self.add(2)
        self.assertEqual((1, 2, 3), self.d.get_location())

    def test_should_return_124_for_4th_doc(self):
        self.add(3)
        self.assertEqual((1, 2, 4), self.d.get_location())

    def test_should_return_235_for_5th_doc(self):
        self.add(4)
        self.assertEqual((2, 3, 5), self.d.get_location())

    def test_should_return_236_for_6th_doc(self):
        self.add(5)
        self.assertEqual((2, 3, 6), self.d.get_location())

    def test_should_return_247_for_7th_doc(self):
        self.add(6)
        self.assertEqual((2, 4, 7), self.d.get_location())

    def test_should_return_359_for_9th_doc(self):
        self.add(8)
        self.assertEqual((3, 5, 9), self.d.get_location())

    def test_should_instantiate_with_mID_3(self):
        d = docmanager.LocalDocumentManager(False, 3, 1, 1)
        self.assertEqual(3, d.mID)
        self.assertEqual(1, d.dCf)
        self.assertEqual(2, d.dID)

    def test_should_instantiate_with_dCf_3(self):
        d = docmanager.LocalDocumentManager(False, 1, 3, 1)
        self.assertEqual(1, d.mID)
        self.assertEqual(3, d.dCf)
        self.assertEqual(2, d.dID)

    def test_should_instantiate_with_dID_3(self):
        d = docmanager.LocalDocumentManager(False, 1, 1, 3)
        self.assertEqual(1, d.mID)
        self.assertEqual(1, d.dCf)
        self.assertEqual(4, d.dID)

    def test_should_increase_dCf_if_dID_greater_than_MAX(self):
        d = docmanager.LocalDocumentManager(False, 1, 1, 10000)
        self.assertEqual((1, 2, 10001), d.get_location())

    def test_should_increase_mID_if_dCf_greater_than_MAX(self):
        d = docmanager.LocalDocumentManager(False, 1, 10000, 100000000)
        self.assertEqual((2, 10001, 100000001), d.get_location())

    def test_should_set_mID_3(self):
        d = docmanager.LocalDocumentManager(False)
        d.set_location(3, 1, 1)
        self.assertEqual(3, d.mID)
        self.assertEqual(1, d.dCf)
        self.assertEqual(2, d.dID)

    def test_should_set_dCf_3(self):
        d = docmanager.LocalDocumentManager(False)
        d.set_location(1, 3, 1)
        self.assertEqual(1, d.mID)
        self.assertEqual(3, d.dCf)
        self.assertEqual(2, d.dID)

    def test_should_set_dID_3(self):
        d = docmanager.LocalDocumentManager(False)
        d.set_location(1, 1, 3)
        self.assertEqual(1, d.mID)
        self.assertEqual(1, d.dCf)
        self.assertEqual(4, d.dID)

    def test_should_store_append(self):
        d = docmanager.LocalDocumentManager(True)
        self.assertTrue(d.append)

    def test_append_should_be_false(self):
        d = docmanager.LocalDocumentManager(False)
        self.assertFalse(d.append)

    def test_should_increment_values_if_append_true(self):
        d = docmanager.LocalDocumentManager(True)
        self.assertEqual(1, d.mID)
        self.assertEqual(1, d.dCf)
        self.assertEqual(2, d.dID)

    def add(self, n):
        """
        Add n docs to Documents
        """
        for i in range(n):
            self.d.get_location()