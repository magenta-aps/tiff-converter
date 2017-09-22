import unittest

from lxml import etree

from siarddk.docindex import DocIndexBuilder


class TestDocIndexBuilder(unittest.TestCase):

    def setUp(self):
        self.builder = DocIndexBuilder()
        self.tag = etree.QName(self.builder.build())

    def test_root_element_should_be_docindex(self):
        self.assertEqual('docIndex', self.tag.localname)

    def test_root_element_should_have_correct_namespace(self):
        self.assertEqual('http://www.sa.dk/xmlns/diark/1.0', self.tag.namespace)

    @unittest.skip('later')
    def test_should_have_correct_schema_location(self):
        builder = DocIndexBuilder()
        self.assertEqual('http://www.sa.dk/xmlns/diark/1.0 ../Schemas/standard/docIndex.xsd', builder.build().get('xsi'))
