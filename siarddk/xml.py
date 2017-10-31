import os

from lxml import etree

from util.logger import logger


def print_element(element):
    print(str(etree.tostring(element, pretty_print=True), 'utf-8'))


class IndexHandler(object):
    """
    This class should not be instantiated directly - use subclasses instead
    """
    NAME = ''
    NS = 'http://www.sa.dk/xmlns/diark/1.0'
    NSMAP = {
        None: NS,
        'xsi': 'http://www.w3.org/2001/XMLSchema-instance'
    }

    def __init__(self, target: os.path.abspath, name: str):
        """
        :param target: the target folder where the archival version is located
        :param name: the name of the archival version, e.g. AVID.MAG.1000
        """

        self.target = target
        self.name = name
        path = os.path.join(target, '%s.1' % name, 'Indices',
                            '%s.xml' % self.NAME)

        if os.path.isfile(path):
            with open(path, 'r') as f:
                self.index = etree.parse(f).getroot()
            # index_type = os.path.splitext(os.path.basename(path))[0]
            with open('siarddk/%s.xsd' % self.NAME, 'r') as f:
                xsd = etree.XMLSchema(etree.parse(f))
                xsd.assertValid(self.index)
        else:
            tag = etree.QName(self.NS, self.NAME)
            self.index = etree.Element(tag, nsmap=self.NSMAP)
            schema_location = etree.QName(self.NSMAP['xsi'], 'schemaLocation')
            self.index.set(schema_location,
                           'http://www.sa.dk/xmlns/diark/1.0 '
                           '../Schemas/standard/%s.xsd' % self.NAME)
        logger.info('Initialized %s handler' % self.NAME)

    def add_element_child(self, element: etree.Element, name: str, value: str):
        tag = etree.QName(self.NS, name)
        element = etree.SubElement(element, tag)
        element.text = value

    def build(self) -> etree.Element:
        if self.is_valid():
            return self.index
        return None

    def get_index(self):
        return self.index

    def to_string(self):
        index = self.build()
        return str(etree.tostring(index), 'utf-8') \
            if index is not None else None

    def write(self):
        """
        Validate the index file and write it to disk
        """

        logger.info('Writing %s.xml to disk...' % self.NAME)

        index_str = self.to_string()
        if index_str:
            indices_path = os.path.join(self.target, '%s.1' % self.name,
                                      'Indices')
            if not os.path.isdir(indices_path):
                os.makedirs(indices_path)
            index_path = os.path.join(indices_path, '%s.xml' % self.NAME)
            with open(index_path, 'w') as index:
                index.write(self.to_string())
                logger.info('%s.xml written to disk' % self.NAME)
        else:
            logger.error('%s.xml NOT written to disk' % self.NAME)

    def is_valid(self) -> bool:
        logger.info('Validating %s.xml...' % self.NAME)
        with open('siarddk/%s.xsd' % self.NAME, 'r') as f:
            xsd = etree.XMLSchema(etree.parse(f))
            is_valid = xsd.validate(self.index)
            if is_valid:
                logger.info('%s.xml valid' % self.NAME)
                return True
            else:
                logger.error(
                    '%s.xml NOT valid! Error: %s' % (self.NAME, xsd.error_log))
                return False
