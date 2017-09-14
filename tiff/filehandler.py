import os


class FileHandler(object):

    def get_next_file(self):
        pass


class LocalFileHandler(FileHandler):

    def __init__(self, basedir):
        self.walk = os.walk(basedir)
        self.root, self.dirs, self.files = next(self.walk)

    def get_next_file(self):
        if self.files:
            filename = self.files.pop(0)
            return os.path.join(self.root, filename)
        else:
            try:
                self.root, self.dirs, self.files = next(self.walk)
                return self.get_next_file()
            except StopIteration:
                return None

