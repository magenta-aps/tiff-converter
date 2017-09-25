from lxml import etree


class DocIndexBuilder(object):
    NSMAP = {
        None: "http://www.sa.dk/xmlns/diark/1.0",
        'xsi': "http://www.w3.org/2001/XMLSchema-instance"
    }

    def build(self):
        tag = etree.QName(self.NSMAP[None], 'docIndex')
        docIndex = etree.Element(tag, nsmap=self.NSMAP)
        schemaLocation = etree.QName(self.NSMAP['xsi'], 'schemaLocation')
        docIndex.set(schemaLocation, 'http://www.sa.dk/xmlns/diark/1.0 '
                                     '../Schemas/standard/docIndex.xsd')
        return docIndex
