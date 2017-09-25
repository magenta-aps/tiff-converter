from lxml import etree

from util.logger import logger


class DocIndexBuilder(object):
    NS = 'http://www.sa.dk/xmlns/diark/1.0'

    NSMAP = {
        None: NS,
        'xsi': 'http://www.w3.org/2001/XMLSchema-instance'
    }

    def __init__(self):
        tag = etree.QName(self.NS, 'docIndex')
        self.docIndex = etree.Element(tag, nsmap=self.NSMAP)
        schema_location = etree.QName(self.NSMAP['xsi'], 'schemaLocation')
        self.docIndex.set(schema_location, 'http://www.sa.dk/xmlns/diark/1.0 '
                                           '../Schemas/standard/docIndex.xsd')
        logger.info('Initialized docIndex builder')

    def add_doc(self, mID: str, dCf: str, dID: str, oFn: str, aFt: str):
        logger.debug('Adding document to docIndex XML...')

        tag = etree.QName(self.NS, 'doc')
        doc_element = etree.SubElement(self.docIndex, tag)

        # TODO: pID and gmlXsd still missing
        self._add_doc_child(doc_element, 'dID', dID)
        self._add_doc_child(doc_element, 'mID', mID)
        self._add_doc_child(doc_element, 'dCf', dCf)
        self._add_doc_child(doc_element, 'oFn', oFn)
        self._add_doc_child(doc_element, 'aFt', aFt)

        logger.debug('Added document to docIndex XML')

    def build(self):
        logger.info('Validating docIndex.xml...')
        with open('siarddk/docIndex.xsd', 'r') as f:
            xsd = etree.XMLSchema(etree.parse(f))
            is_valid = xsd.validate(self.docIndex)
            if is_valid:
                logger.info('docIndex.xml valid')
            else:
                logger.error(
                    'docIndex.xml NOT valid! Error: %s' % xsd.error_log)
        # print(str(etree.tostring(self.docIndex, pretty_print=True), 'utf-8'))
        return self.docIndex

    def to_string(self):
        pass

    def _add_doc_child(self, doc_element: etree.Element, name: str, value: str):
        tag = etree.QName(self.NS, name)
        element = etree.SubElement(doc_element, tag)
        element.text = value
