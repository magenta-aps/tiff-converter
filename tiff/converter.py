import os
import shutil

import siarddk.docmanager
import siarddk.docindex
import tiff.filehandler
from tiff.pdfconverter import MSOfficeToPdfConverter
import tiff.tiffconverter

from util.logger import logger


class Converter(object):
    def __init__(
            self,
            source: os.path.abspath,
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
        pdfconverter = MSOfficeToPdfConverter(self.conversion_dir,
                                              MSOfficeToPdfConverter.WORD)
        docindex_builder = siarddk.docindex.DocIndexBuilder()

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
                if success:
                    oFn = os.path.basename(next_file)
                    docindex_builder.add_doc(str(mID), 'docCollection%s' % dCf,
                                             str(dID), oFn, 'tif')
            else:
                success = False

            # Clean up conversion folder
            for f in os.listdir(self.conversion_dir):
                f = os.path.join(self.conversion_dir, f)
                if os.path.isfile(f):
                    os.remove(f)

            next_file = filehandler.get_next_file()

        # Write docIndex to file
        logger.info('Writing docIndex.xml to disk...')
        indices_path = os.path.join(self.target, '%s.1' % self.name, 'Indices')
        os.mkdir(indices_path)
        docindex_path = os.path.join(indices_path, 'docIndex.xml')
        with open(docindex_path, 'w') as docindex:
            docindex.write(docindex_builder.to_string())
        logger.info('docIndex.xml written to disk')

        pdfconverter.close()
        logger.info('Conversion done!')
