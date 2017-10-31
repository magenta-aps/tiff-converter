from typing import Tuple

from siarddk.xml import *
from siarddk.docmanager import LocalDocumentManager
from util.logger import logger


# TODO: rename to Local...
class DocIndexHandler(IndexHandler):
    NAME = 'docIndex'

    def __init__(self, target: os.path.abspath, name: str):
        super().__init__(target, name)
        mid, dcf, did = self.get_ids()
        self.docmanager = LocalDocumentManager(mid, dcf, did)

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

    def add_file(self, next_file: os.path.abspath, tiff_path: os.path.abspath):
        oFn = os.path.basename(next_file)
        rel_tiff_path = os.path.relpath(tiff_path, self.target)
        path, file = os.path.split(rel_tiff_path)
        aFt = os.path.splitext(file)[1][1:]
        path, dID = os.path.split(path)
        path, dCf = os.path.split(path)
        mID = os.path.split(path)[0].split('.')[-1]
        self.add_doc(mID, dCf, dID, oFn, aFt)

    def get_location(self):
        return self.docmanager.get_location()

    def get_ids(self) -> Tuple[int, int, int]:
        if len(self.index) == 0:
            return 1, 1, 1
        else:
            doc = self.index[-1]
            return int(doc[1].text), int(
                doc[2].text.split('docCollection')[1]), int(doc[0].text)
