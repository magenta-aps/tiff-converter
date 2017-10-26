import os
from typing import Tuple


class LocalFilePathStrategy(object):

    def __init__(self, basedir):
        self.walk = os.walk(basedir)
        self.root, self.dirs, self.files = next(self.walk)

    def get_next(self) -> Tuple[os.path.abspath, os.path.abspath]:
        return self._get_source_path(), None

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

    def _get_target_path(self):
        pass