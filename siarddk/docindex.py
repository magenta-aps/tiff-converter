from siarddk.xml import *
from util.logger import logger


class DocIndexHandler(IndexHandler):
    NAME = 'docIndex'

    def __init__(self, path=None):
        super().__init__(path)

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

    def get_ids(self):
        doc = self.index[-1]
        return int(doc[1].text), int(
            doc[2].text.split('docCollection')[1]), int(doc[0].text)
