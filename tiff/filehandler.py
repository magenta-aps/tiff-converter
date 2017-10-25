import os


class FilePathStrategy(object):

    def get_next(self):
        pass


class LocalFilePathStrategy(FilePathStrategy):

    def __init__(self, basedir):
        self.walk = os.walk(basedir)
        self.root, self.dirs, self.files = next(self.walk)

    def get_next(self) -> os.path:
        if self.files:
            filename = self.files.pop(0)
            return os.path.join(self.root, filename)
        else:
            try:
                self.root, self.dirs, self.files = next(self.walk)
                return self.get_next()
            except StopIteration:
                return None

