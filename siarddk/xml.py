import os

from lxml import etree


def print_element(element):
    print(str(etree.tostring(element, pretty_print=True), 'utf-8'))


class IndexBuilder(object):
    NS = 'http://www.sa.dk/xmlns/diark/1.0'

    def add_element_child(self, element: etree.Element, name: str, value: str):
        tag = etree.QName(self.NS, name)
        element = etree.SubElement(element, tag)
        element.text = value


class IndexReader(object):
    def __init__(self, path: os.path.abspath):
        with open(path, 'r') as f:
            self.index = etree.parse(f).getroot()
        index_type = os.path.splitext(os.path.basename(path))[0]
        with open('siarddk/%s.xsd' % index_type, 'r') as f:
            xsd = etree.XMLSchema(etree.parse(f))
            xsd.assertValid(self.index)

    def get_index(self):
        return self.index
