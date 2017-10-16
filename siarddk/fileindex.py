import hashlib

from lxml import etree

from siarddk.xml import *
from tiff.filehandler import LocalFileHandler


class FileIndex(IndexBuilder, IndexReader):
    NS = 'http://www.sa.dk/xmlns/diark/1.0'
    NAME = 'fileIndex'

    def __init__(self, target: os.path.abspath, name: str):
        """
        :param target: the target folder where the archival version is located
        :param name: the name of the archival version, e.g. AVID.MAG.1000
        """

        # TODO: this is getting ugly... use compositional design instead

        path = os.path.join(target, '%s.1' % name, 'Indices', 'fileIndex.xml')

        IndexBuilder.__init__(self)
        IndexReader.__init__(self, path if os.path.isfile(path) else None)
        self.target = target

    def add_file(self, path: os.path.abspath):
        foN, fiN = os.path.split(path)
        foN = os.path.relpath(foN, self.target).replace('/', '\\')

        exclude_conditions = [
            foN.split('\\')[1] == 'Indices' and fiN == 'fileIndex.xml',
            foN.split('\\')[1] == 'Tables'
        ]

        if True not in exclude_conditions:
            tag = etree.QName(self.NS, 'f')
            f = etree.SubElement(self.get_index(), tag)
            self.add_element_child(f, 'foN', foN)
            self.add_element_child(f, 'fiN', fiN)
            self.add_element_child(f, 'md5', self._get_md5sum(path))

        # log stuff

    def add_folders(self, folders: list):
        for folder in folders:
            filehandler = LocalFileHandler(folder)
            next_file = filehandler.get_next_file()
            while next_file:
                self.add_file(next_file)
                next_file = filehandler.get_next_file()

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
