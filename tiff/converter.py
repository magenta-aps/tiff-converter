import os
import shutil

import siarddk.docmanager
import tiff.filehandler
import tiff.pdfconverter
import tiff.tiffconverter

from util.logger import logger


class Converter(object):
    def __init__(
            self, source: os.path.abspath,
            target: os.path.abspath,
            conversion_dir: os.path.abspath,
            name: str,
            docmanager: siarddk.docmanager.DocumentManager
    ):
        self.source = source
        self.target = target
        self.conversion_dir = conversion_dir
        self.name = name
        self.docmanager = docmanager

        # Set up conversion folder
        try:
            shutil.rmtree(self.conversion_dir)
        except OSError:
            pass
        os.makedirs(self.conversion_dir)

        logger.info('Initialized Converter')

    def convert(self):
        logger.info('Starting conversion...')
        filehandler = tiff.filehandler.LocalFileHandler(self.source)
        pdfconverter = tiff.pdfconverter.DocToPdfConverter(self.conversion_dir)

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
                success = tiff.tiffconverter.convert(
                    pdf, os.path.join(folder, '%s.tif' % dID))
            else:
                success = False

            # Clean up conversion folder
            for f in os.listdir(self.conversion_dir):
                f = os.path.join(self.conversion_dir, f)
                if os.path.isfile(f):
                    os.remove(f)

            next_file = filehandler.get_next_file()

        logger.info('Conversion done!')
        pdfconverter.close()
