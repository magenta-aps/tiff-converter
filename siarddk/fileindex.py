import hashlib

from lxml import etree

from siarddk.xml import *


class FileIndex(SIARDDK, IndexReader):
    NS = 'http://www.sa.dk/xmlns/diark/1.0'

    def __init__(self, target: os.path.abspath, path: os.path.abspath):
        """
        :param target: the target folder where the archival version is located
        :param path: the full path to fileIndex.xml
        """
        super().__init__(path)
        self.target = target

    def add(self, path: os.path.abspath):
        tag = etree.QName(self.NS, 'f')
        f = etree.SubElement(self.get_index(), tag)

        foN, fiN = os.path.split(path)
        foN = os.path.relpath(foN, self.target).replace('/', '\\')

        self.add_element_child(f, 'foN', foN)
        self.add_element_child(f, 'fiN', fiN)
        self.add_element_child(f, 'md5', self._get_md5sum(path))

        # log stuff

    def calculate_md5sums(self):
        pass

    def remove_all(self):
        """
        Remove all files except for those in the Tables folder
        """
        for f in self.get_index():
            foN = f[0].text
            if not foN.split('\\')[1] == 'Tables':
                f.getparent().remove(f)

    @staticmethod
    def _get_md5sum(path: os.path.abspath) -> str:
        hash_md5 = hashlib.md5()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest().upper()
