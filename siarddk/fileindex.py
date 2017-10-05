import os

from siarddk.xml import IndexReader


class FileIndexReader(IndexReader):
    def __init__(self, path: os.path.abspath):
        super().__init__(path)

