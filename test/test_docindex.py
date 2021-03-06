import mock
import os
import shutil
import tempfile
import unittest

from lxml import etree

from siarddk.docindex import DocIndexHandler


class TestDocIndexReader(unittest.TestCase):
    def setUp(self):
        self.target = os.path.join(tempfile.gettempdir(), '_docIndex')
        if os.path.isdir(self.target):
            shutil.rmtree(self.target)
        os.makedirs(os.path.join(self.target, 'AVID.MAG.1000.1', 'Indices'))
        self.docindex_path = os.path.join(self.target, 'AVID.MAG.1000.1',
                                          'Indices', 'docIndex.xml')
        self.builder = DocIndexHandler(self.target, 'AVID.MAG.1000')
        self.builder.add_doc('1', 'docCollection1', '1', 'file1.tif', 'tif')

    def tearDown(self):
        if os.path.isdir(self.target):
            shutil.rmtree(self.target)

    def test_should_return_mID_1_dCf_1_dID_1(self):
        self.write_to_file_and_read_docindex()
        self.assertEqual((1, 1, 1), self.d.get_ids())

    def test_should_return_mID_1_dCf_1_dID_2(self):
        self.builder.add_doc('1', 'docCollection1', '2', 'file2.tif', 'tif')
        self.write_to_file_and_read_docindex()
        self.assertEqual((1, 1, 2), self.d.get_ids())

    def test_should_return_mID_1_dCf_2_dID_3(self):
        self.builder.add_doc('1', 'docCollection1', '2', 'file2.tif', 'tif')
        self.builder.add_doc('1', 'docCollection2', '3', 'file3.tif', 'tif')
        self.write_to_file_and_read_docindex()
        self.assertEqual((1, 2, 3), self.d.get_ids())

    def test_should_return_mID_2_dCf_3_dID_4(self):
        self.builder.add_doc('1', 'docCollection1', '2', 'file2.tif', 'tif')
        self.builder.add_doc('1', 'docCollection2', '3', 'file3.tif', 'tif')
        self.builder.add_doc('2', 'docCollection3', '4', 'file4.tif', 'tif')
        self.write_to_file_and_read_docindex()
        self.assertEqual((2, 3, 4), self.d.get_ids())

    def test_should_raise_exception_if_docindex_invalid(self):
        self.builder.add_doc('1', 'docCollection1', '2', 'file2.bin', 'bin')
        with open(self.docindex_path, 'w') as f:
            f.write(str(etree.tostring(self.builder.index), 'utf-8'))
        with self.assertRaises(etree.DocumentInvalid):
            DocIndexHandler(self.target, 'AVID.MAG.1000')

    def test_should_return_docindex(self):
        self.write_to_file_and_read_docindex()
        docindex = self.d.build()
        self.assertEqual(1, len(docindex))
        doc1 = docindex[0]
        self.assertEqual('1', doc1[0].text)
        self.assertEqual('1', doc1[1].text)
        self.assertEqual('docCollection1', doc1[2].text)
        self.assertEqual('file1.tif', doc1[3].text)
        self.assertEqual('tif', doc1[4].text)

    def write_to_file_and_read_docindex(self):
        with open(self.docindex_path, 'w') as f:
            f.write(self.builder.to_string())
        self.d = DocIndexHandler(self.target, 'AVID.MAG.1000')


class TestHelper(unittest.TestCase):
    def setUp(self):
        self.target = os.path.join(tempfile.gettempdir(), '_docindex')
        self.name = 'AVID.MAG.1000'


class TestDocIndexBuilder(TestHelper):
    def setUp(self):
        super().setUp()
        self.builder = DocIndexHandler(self.target, self.name)
        self.builder.add_doc('1', 'docCollection1', '1', 'name.tif', 'tif')
        self.doc1 = self.builder.build()[0]
        self.builder.add_doc('2', 'docCollection2', '2', 'name2.jpg', 'wav')
        self.doc2 = self.builder.build()[1]
        self.docIndex_tag = etree.QName(self.builder.build())

        self.builder.write()

    def tearDown(self):
        shutil.rmtree(self.target)

    def test_should_store_type_docindex(self):
        self.assertEqual('docIndex', self.builder.NAME)

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

    def test_should_store_existing_docindex(self):
        builder_new = DocIndexHandler(self.target, self.name)
        docindex_new = builder_new.build()
        self.assertEqual(2, len(docindex_new))

    def test_should_append_document_to_existing_docindex(self):
        builder_new = DocIndexHandler(self.target, self.name)
        builder_new.add_doc('3', 'docCollection3', '3', 'name3.tif', 'tif')
        docindex_new = builder_new.build()
        self.assertEqual(3, len(docindex_new))
        doc1 = docindex_new[0]
        self.assertEqual('1', doc1[0].text)
        self.assertEqual('1', doc1[1].text)
        self.assertEqual('docCollection1', doc1[2].text)
        self.assertEqual('name.tif', doc1[3].text)
        self.assertEqual('tif', doc1[4].text)
        doc3 = docindex_new[2]
        self.assertEqual('3', doc3[0].text)
        self.assertEqual('3', doc3[1].text)
        self.assertEqual('docCollection3', doc3[2].text)
        self.assertEqual('name3.tif', doc3[3].text)
        self.assertEqual('tif', doc3[4].text)

    def test_should_get_location_223(self):
        builder_new = DocIndexHandler(self.target, self.name)
        self.assertEqual((2, 2, 3), builder_new.get_location())

    # Testing add_doc

    def test_docIndex_should_have_child_doc(self):
        tag = etree.QName(self.doc1)
        self.assertEqual('doc', tag.localname)
        self.assertEqual('http://www.sa.dk/xmlns/diark/1.0', tag.namespace)

    def test_1st_doc_should_have_child_dID(self):
        tag = etree.QName(self.doc1[0])
        self.assertEqual('dID', tag.localname)
        self.assertEqual('http://www.sa.dk/xmlns/diark/1.0', tag.namespace)

    def test_1st_dID_should_contain_1(self):
        dID = self.doc1[0]
        self.assertEqual('1', dID.text)

    def test_1st_doc_should_have_child_mID(self):
        tag = etree.QName(self.doc1[1])
        self.assertEqual('mID', tag.localname)
        self.assertEqual('http://www.sa.dk/xmlns/diark/1.0', tag.namespace)

    def test_1st_mID_should_contain_1(self):
        mID = self.doc1[1]
        self.assertEqual('1', mID.text)

    def test_1st_doc_should_have_child_dCf(self):
        tag = etree.QName(self.doc1[2])
        self.assertEqual('dCf', tag.localname)
        self.assertEqual('http://www.sa.dk/xmlns/diark/1.0', tag.namespace)

    def test_1st_dCf_should_contain_1(self):
        dCf = self.doc1[2]
        self.assertEqual('docCollection1', dCf.text)

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

    def test_2nd_doc_should_have_child_dID(self):
        tag = etree.QName(self.doc2[0])
        self.assertEqual('dID', tag.localname)
        self.assertEqual('http://www.sa.dk/xmlns/diark/1.0', tag.namespace)

    def test_2nd_dID_should_contain_2(self):
        dID = self.doc2[0]
        self.assertEqual('2', dID.text)

    def test_2nd_doc_should_have_child_mID(self):
        tag = etree.QName(self.doc2[1])
        self.assertEqual('mID', tag.localname)
        self.assertEqual('http://www.sa.dk/xmlns/diark/1.0', tag.namespace)

    def test_2nd_mID_should_contain_2(self):
        mID = self.doc2[1]
        self.assertEqual('2', mID.text)

    def test_2nd_doc_should_have_child_dCf(self):
        tag = etree.QName(self.doc2[2])
        self.assertEqual('dCf', tag.localname)
        self.assertEqual('http://www.sa.dk/xmlns/diark/1.0', tag.namespace)

    def test_2nd_dCf_should_contain_2(self):
        dCf = self.doc2[2]
        self.assertEqual('docCollection2', dCf.text)

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

    def test_2nd_aFt_should_contain_name(self):
        oFn = self.doc2[4]
        self.assertEqual('wav', oFn.text)

    def test_should_return_string_representation(self):
        expected = '<docIndex xmlns:xsi="http://www.w3.org/2001/XMLSchema-' \
                   'instance" xmlns="http://www.sa.dk/xmlns/diark/1.0" ' \
                   'xsi:schemaLocation="http://www.sa.dk/xmlns/diark/1.0 ' \
                   '../Schemas/standard/docIndex.xsd"><doc><dID>1</dID>' \
                   '<mID>1</mID><dCf>docCollection1</dCf><oFn>name.tif</oFn>' \
                   '<aFt>tif</aFt></doc><doc><dID>2</dID><mID>2</mID>' \
                   '<dCf>docCollection2</dCf><oFn>name2.jpg</oFn>' \
                   '<aFt>wav</aFt></doc></docIndex>'
        self.assertEqual(expected, self.builder.to_string())

    def test_docindex_should_be_valid(self):
        self.assertTrue(self.builder.is_valid())

    def test_should_write_docindex_to_disk(self):
        docindex_path = os.path.join(self.target, 'AVID.MAG.1000.1', 'Indices',
                                     'docIndex.xml')
        self.assertTrue(os.path.isfile(docindex_path))
        docindex = DocIndexHandler(self.target, 'AVID.MAG.1000')
        self.assertTrue(docindex.is_valid())

    @mock.patch('siarddk.xml.IndexHandler.build')
    def test_to_string_should_return_none_when_index_invalid(self, mock):
        mock.return_value = None
        self.assertIsNone(self.builder.to_string())

    @mock.patch('siarddk.xml.IndexHandler.to_string')
    def test_to_string_should_return_none_when_index_invalid(self, mock):
        mock.return_value = None
        docindex_path = os.path.join(self.target, 'AVID.MAG.1000.1', 'Indices',
                                     'docIndex.xml')
        handler = DocIndexHandler(self.target, self.name)
        os.remove(docindex_path)
        handler.write()
        self.assertFalse(os.path.isfile(docindex_path))


@unittest.skip('Skipped in order to save time...')
class TestStressDocIndexHandler(TestHelper):
    def tearDown(self):
        shutil.rmtree(self.target)

    def test_should_handle_10million_docs(self):
        handler = DocIndexHandler(self.target, self.name)
        for i in range(1, 1000000):
            handler.add_doc('1', 'docCollection1', str(i), 'name.tif', 'tif')
        handler.write()
        self.assertTrue(
            os.path.isfile(
                os.path.join(self.target, 'AVID.MAG.1000.1', 'Indices',
                             'docIndex.xml')))


class TestAddFilepath(TestHelper):
    def setUp(self):
        super().setUp()
        self.handler = DocIndexHandler(self.target, self.name)

    def tearDown(self):
        if os.path.isdir(self.target):
            shutil.rmtree(self.target)

    def test_should_add_doc1_correctly(self):
        doc_path = os.path.join(tempfile.gettempdir(), 'sample.docx')
        tiff_path = os.path.join(self.target, '%s.1' % self.name, 'Documents',
                                'docCollection2', '3', '1.tif')
        self.handler.add_file(doc_path, tiff_path)
        doc = self.handler.index[0]
        self.assertEqual('3', doc[0].text)
        self.assertEqual('1', doc[1].text)
        self.assertEqual('docCollection2', doc[2].text)
        self.assertEqual('sample.docx', doc[3].text)
        self.assertEqual('tif', doc[4].text)

    def test_should_add_doc2_correctly(self):
        doc_path = os.path.join(tempfile.gettempdir(), 'sample.wav')
        tiff_path = os.path.join(self.target, '%s.2' % self.name, 'Documents',
                                'docCollection3', '4', '1.wav')
        self.handler.add_file(doc_path, tiff_path)
        doc = self.handler.index[0]
        self.assertEqual('4', doc[0].text)
        self.assertEqual('2', doc[1].text)
        self.assertEqual('docCollection3', doc[2].text)
        self.assertEqual('sample.wav', doc[3].text)
        self.assertEqual('wav', doc[4].text)
