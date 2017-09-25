import unittest

from lxml import etree

from siarddk.docindex import DocIndexBuilder


class TestDocIndexBuilder(unittest.TestCase):
    def setUp(self):
        self.builder = DocIndexBuilder()
        self.docIndex_tag = etree.QName(self.builder.build())
        self.builder.add_doc('1', '1', '1', 'name.tif', 'tif')
        self.doc1 = self.builder.build()[0]
        self.builder.add_doc('2', '2', '2', 'name2.jpg', 'jpg')
        self.doc2 = self.builder.build()[1]

    # Testing that the docIndex element is constructed correctly

    def test_root_element_should_be_docindex(self):
        self.assertEqual('docIndex', self.docIndex_tag.localname)

    def test_root_element_should_have_correct_namespace(self):
        self.assertEqual('http://www.sa.dk/xmlns/diark/1.0',
                         self.docIndex_tag.namespace)

    def test_should_have_correct_schema_location(self):
        name_space = 'http://www.w3.org/2001/XMLSchema-instance'
        self.assertEqual(
            'http://www.sa.dk/xmlns/diark/1.0 ../Schemas/standard/docIndex.xsd',
            self.builder.build().get('{%s}' % name_space + 'schemaLocation'))

    # Testing add_doc

    def test_docIndex_should_have_child_doc(self):
        tag = etree.QName(self.doc1)
        self.assertEqual('doc', tag.localname)
        self.assertEqual('http://www.sa.dk/xmlns/diark/1.0', tag.namespace)

    def test_1st_doc_should_have_child_mID(self):
        tag = etree.QName(self.doc1[0])
        self.assertEqual('mID', tag.localname)
        self.assertEqual('http://www.sa.dk/xmlns/diark/1.0', tag.namespace)

    def test_1st_mID_should_contain_1(self):
        mID = self.doc1[0]
        self.assertEqual('1', mID.text)

    def test_1st_doc_should_have_child_dCf(self):
        tag = etree.QName(self.doc1[1])
        self.assertEqual('dCf', tag.localname)
        self.assertEqual('http://www.sa.dk/xmlns/diark/1.0', tag.namespace)

    def test_1st_dCf_should_contain_1(self):
        dCf = self.doc1[1]
        self.assertEqual('1', dCf.text)

    def test_1st_doc_should_have_child_dID(self):
        tag = etree.QName(self.doc1[2])
        self.assertEqual('dID', tag.localname)
        self.assertEqual('http://www.sa.dk/xmlns/diark/1.0', tag.namespace)

    def test_1st_dID_should_contain_1(self):
        dID = self.doc1[2]
        self.assertEqual('1', dID.text)

    def test_1st_doc_should_have_child_oFn(self):
        tag = etree.QName(self.doc1[3])
        self.assertEqual('oFn', tag.localname)
        self.assertEqual('http://www.sa.dk/xmlns/diark/1.0', tag.namespace)

    def test_1st_oFn_should_contain_name(self):
        oFn = self.doc1[3]
        self.assertEqual('name.tif', oFn.text)

    def test_1st_doc_should_have_child_aFt(self):
        tag = etree.QName(self.doc1[4])
        self.assertEqual('aFt', tag.localname)
        self.assertEqual('http://www.sa.dk/xmlns/diark/1.0', tag.namespace)

    def test_1st_aFt_should_contain_name(self):
        oFn = self.doc1[4]
        self.assertEqual('tif', oFn.text)

    def test_docIndex_should_doc_as_2nd_child(self):
        tag = etree.QName(self.doc2)
        self.assertEqual('doc', tag.localname)
        self.assertEqual('http://www.sa.dk/xmlns/diark/1.0', tag.namespace)

    def test_2nd_doc_should_have_child_mID(self):
        tag = etree.QName(self.doc2[0])
        self.assertEqual('mID', tag.localname)
        self.assertEqual('http://www.sa.dk/xmlns/diark/1.0', tag.namespace)

    def test_2nd_mID_should_contain_2(self):
        mID = self.doc2[0]
        self.assertEqual('2', mID.text)

    def test_2nd_doc_should_have_child_dCf(self):
        tag = etree.QName(self.doc2[1])
        self.assertEqual('dCf', tag.localname)
        self.assertEqual('http://www.sa.dk/xmlns/diark/1.0', tag.namespace)

    def test_2nd_dCf_should_contain_2(self):
        dCf = self.doc2[1]
        self.assertEqual('2', dCf.text)

    def test_2nd_doc_should_have_child_dID(self):
        tag = etree.QName(self.doc2[2])
        self.assertEqual('dID', tag.localname)
        self.assertEqual('http://www.sa.dk/xmlns/diark/1.0', tag.namespace)

    def test_2nd_dID_should_contain_2(self):
        dID = self.doc2[2]
        self.assertEqual('2', dID.text)

    def test_2nd_doc_should_have_child_oFn(self):
        tag = etree.QName(self.doc2[3])
        self.assertEqual('oFn', tag.localname)
        self.assertEqual('http://www.sa.dk/xmlns/diark/1.0', tag.namespace)

    def test_2nd_oFn_should_contain_name(self):
        oFn = self.doc2[3]
        self.assertEqual('name2.jpg', oFn.text)

    def test_2nd_doc_should_have_child_aFt(self):
        tag = etree.QName(self.doc2[4])
        self.assertEqual('aFt', tag.localname)
        self.assertEqual('http://www.sa.dk/xmlns/diark/1.0', tag.namespace)

    def test_1st_aFt_should_contain_name(self):
        oFn = self.doc2[4]
        self.assertEqual('jpg', oFn.text)
