import os

import siarddk.docmanager
import tiff.filehandler


class Converter(object):
    def __init__(self, source: os.path.abspath,
                 target: os.path.abspath,
                 name: str,
                 docmanager: siarddk.docmanager.DocumentManager):
        self.source = source
        self.target = target
        self.name = name
        self.docmanager = docmanager
        # Field to store errors

    def convert(self):
        filehandler = tiff.filehandler.LocalFileHandler(self.source)

        next_file = filehandler.get_next_file()
        while next_file:
            # Chech permissions
            mID, dCf, dID = self.docmanager.get_location()
            folder = os.path.join(self.target, '%s.%s' % (self.name, mID),
                                  'Documents', 'docCollection%s' % dCf,
                                  str(dID))
            if not os.path.isdir(folder):
                os.makedirs(folder)
            next_file = filehandler.get_next_file()
