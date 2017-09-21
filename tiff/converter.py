import os
import tempfile

import siarddk.docmanager
import tiff.filehandler
import tiff.pdfconverter
import tiff.tiffconverter


class Converter(object):
    def __init__(
            self, source: os.path.abspath,
            target: os.path.abspath,
            name: str,
            docmanager: siarddk.docmanager.DocumentManager
    ):
        self.source = source
        self.target = target
        self.name = name
        self.docmanager = docmanager
        # Field to store errors

    def convert(self):
        filehandler = tiff.filehandler.LocalFileHandler(self.source)
        pdfconverter = tiff.pdfconverter.DocToPdfConverter(
            tempfile.gettempdir())

        success = True
        next_file = filehandler.get_next_file()
        while next_file:
            if success:
                mID, dCf, dID = self.docmanager.get_location()

            # Create folder
            folder = os.path.join(self.target, '%s.%s' % (self.name, mID),
                                  'Documents', 'docCollection%s' % dCf, str(dID)
                                  )
            if not os.path.isdir(folder):
                os.makedirs(folder)

            # Convert file to PDF
            pdf = pdfconverter.convert(next_file)
            if pdf:
                # Check for errors
                tif = tiff.tiffconverter.convert(
                    pdf, os.path.join(folder, '%s.tif' % dID))
                success = True
            else:
                success = False
                # Do logging
                pass

            # print(next_file, tif)

            next_file = filehandler.get_next_file()

        pdfconverter.close()
