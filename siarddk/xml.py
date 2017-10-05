import os

from lxml import etree


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
