import os
from typing import Tuple

from ff.folder import create_doc_folder


class LocalFilePathStrategy(object):
    def __init__(self, basedir):
        self.walk = os.walk(basedir)
        self.root, self.dirs, self.files = next(self.walk)

    def get_next(self, converter) -> Tuple[os.path.abspath, os.path.abspath]:
        return self._get_source_path(), self._get_target_path(converter)

    # TODO: rename this method (or something) as it is used by fileindex.py
    def _get_source_path(self) -> os.path.abspath:
        if self.files:
            filename = self.files.pop(0)
            return os.path.join(self.root, filename)
        else:
            try:
                self.root, self.dirs, self.files = next(self.walk)
                return self._get_source_path()
            except StopIteration:
                return None

    def _get_target_path(self, converter):
        mID, dCf, dID = converter.docindex_handler.get_location()
        return create_doc_folder(converter.target, converter.name, mID,
                                 dCf, dID)
