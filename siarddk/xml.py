import os

from lxml import etree

from util.logger import logger


def print_element(element):
    print(str(etree.tostring(element, pretty_print=True), 'utf-8'))


class IndexBuilder(object):
    """
    This class should not be instantiated directly - use subclasses instead
    """
    NAME = ''
    NS = 'http://www.sa.dk/xmlns/diark/1.0'

    def __init__(self):
        self.index = None

    def add_element_child(self, element: etree.Element, name: str, value: str):
        tag = etree.QName(self.NS, name)
        element = etree.SubElement(element, tag)
        element.text = value

    def build(self) -> etree.Element:
        logger.info('Validating %s.xml...' % self.NAME)
        with open('siarddk/%s.xsd' % self.NAME, 'r') as f:
            xsd = etree.XMLSchema(etree.parse(f))
            is_valid = xsd.validate(self.index)
            if is_valid:
                logger.info('%s.xml valid' % self.NAME)
            else:
                logger.error(
                    '%s.xml NOT valid! Error: %s' % (self.NAME, xsd.error_log))
        return self.index

    def to_string(self):
        return str(etree.tostring(self.build()), 'utf-8')

            # def write(self, target: os.path.abspath):
    #     """
    #     Validate the index file and write it to disk
    #     :return: None
    #     """
    #
    #     logger.info('Writing %s.xml to disk...' % self.NAME)
    #
    #     indices_path = os.path.join(target, '%s.1' % self.NAME, 'Indices')
    #     if not os.path.isdir(indices_path):
    #         os.mkdir(indices_path)
    #     index_path = os.path.join(indices_path, '%s.xml' % self.NAME)
    #     with open(index_path, 'w') as docindex:
    #         docindex.write(self.docindex_builder.to_string())
    #
    #     logger.info('%s.xml written to disk' % self.NAME)


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
