import os
from lxml import etree

from siarddk.xml import *
from util.logger import logger


class DocIndexBuilder(IndexBuilder):
    NAME = 'docIndex'
    NSMAP = {
        None: IndexBuilder.NS,
        'xsi': 'http://www.w3.org/2001/XMLSchema-instance'
    }

    def __init__(self, docindex=None):
        super().__init__()
        if docindex is not None:
            self.index = docindex
        else:
            tag = etree.QName(self.NS, 'docIndex')
            self.index = etree.Element(tag, nsmap=self.NSMAP)
            schema_location = etree.QName(self.NSMAP['xsi'], 'schemaLocation')
            self.index.set(schema_location,
                           'http://www.sa.dk/xmlns/diark/1.0 '
                           '../Schemas/standard/docIndex.xsd')
        logger.info('Initialized docIndex builder')

    def add_doc(self, mID: str, dCf: str, dID: str, oFn: str, aFt: str):
        logger.debug('Adding document to docIndex XML...')

        tag = etree.QName(self.NS, 'doc')
        doc_element = etree.SubElement(self.index, tag)

        # TODO: pID and gmlXsd still missing
        self.add_element_child(doc_element, 'dID', dID)
        self.add_element_child(doc_element, 'mID', mID)
        self.add_element_child(doc_element, 'dCf', dCf)
        self.add_element_child(doc_element, 'oFn', oFn)
        self.add_element_child(doc_element, 'aFt', aFt)

        logger.debug('Added document to docIndex XML')


class DocIndexReader(IndexReader):
    def __init__(self, path: os.path.abspath):
        super().__init__(path)

    def get_ids(self):
        doc = self.index[-1]
        return int(doc[1].text), int(
            doc[2].text.split('docCollection')[1]), int(doc[0].text)
