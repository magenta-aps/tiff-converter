import os
import re
from typing import Tuple

from ff.folder import create_doc_folder


class LocalFilePathStrategy(object):
    def __init__(self, basedir):
        self.walk = os.walk(basedir)
        try:
            self.root, self.dirs, self.files = next(self.walk)
        except StopIteration:
            pass

    def get_next(self, converter) -> Tuple[os.path.abspath, os.path.abspath]:
        return self.get_source_path(), self._get_target_path(converter)

    def get_source_path(self) -> os.path.abspath:
        if self.files:
            filename = self.files.pop(0)
            return os.path.join(self.root, filename)
        else:
            try:
                self.root, self.dirs, self.files = next(self.walk)
                return self.get_source_path()
            except StopIteration:
                return None

    def _get_target_path(self, converter):
        mID, dCf, dID = converter.docindex_handler.get_location()
        return create_doc_folder(converter.target, converter.name, mID,
                                 dCf, dID)


class InPlaceFilePathStrategy(object):
    def __init__(self, target, name):
        self.target = target
        self.name = name
        self.next_file = None
        self.folders = os.listdir(target)
        self.folders.sort()
        self.i = 0
        self._set_walker()

    def get_next(self, converter) -> Tuple[os.path.abspath, os.path.abspath]:
        return self._get_source_path(), self._get_target_path()

    def _get_source_path(self) -> os.path.abspath:
        self.next_file = self.local_file_path_strategy.get_source_path()
        if not self.next_file:
            self.i += 1
            self._set_walker()
            self.next_file = self.local_file_path_strategy.get_source_path()
        return self.next_file

    def _set_walker(self) -> os.path.abspath:
        if self.i < len(self.folders):
            folder = self.folders[self.i]
            regex = re.compile(self.name + '\.[1-9][0-9]*$')
            if regex.match(folder):
                walk_path = os.path.join(self.target, folder, 'Documents')
                self.local_file_path_strategy = LocalFilePathStrategy(walk_path)
                return walk_path
        return None

    def _get_target_path(self):
        return os.path.join(os.path.split(self.next_file)[0],
                            '1.tif') if self.next_file else None
