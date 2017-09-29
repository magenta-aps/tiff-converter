import os
import shutil
import tempfile

import siarddk.docmanager
import siarddk.docindex
import tiff.filehandler
from tiff.pdfconverter import MSOfficeToPdfConverter
import tiff.tiffconverter

from util.logger import logger


class ComplexConverter(object):
    def __init__(self, conversion_dir: os.path.abspath):
        self.word_converter = MSOfficeToPdfConverter(
            conversion_dir, MSOfficeToPdfConverter.WORD)
        self.excel_converter = MSOfficeToPdfConverter(
            conversion_dir, MSOfficeToPdfConverter.EXCEL)
        self.pdf_to_tiff_converter = tiff.tiffconverter.TiffConverter(
            conversion_dir)

    def convert(self, source: os.path.abspath, target: os.path.abspath):
        ext = os.path.splitext(source)[1][1:]

        pdf = None
        if ext == 'docx':  # or doc (add test for this)
            pdf = self.word_converter.convert(source)
        elif ext == 'xlsx':
            pdf = self.excel_converter.convert(source)
        elif ext == 'pdf':
            pdf = source

        if pdf:
            success = self.pdf_to_tiff_converter.convert(pdf, target)
            return success
        else:
            return False

    def close(self):
        self.word_converter.close()
        self.excel_converter.close()


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
        self.docindex_builder = siarddk.docindex.DocIndexBuilder()
        self.complex_converter = ComplexConverter(self.conversion_dir)

        # Set up conversion folder
        try:
            shutil.rmtree(self.conversion_dir)
        except OSError:
            pass
        os.makedirs(self.conversion_dir)

        logger.info('Initialized Converter')

    def close(self):
        self.complex_converter.close()

    def run(self):
        logger.info('Starting conversion...')
        filehandler = tiff.filehandler.LocalFileHandler(self.source)

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

            # Convert file to TIFF
            success = self.complex_converter.convert(
                next_file, os.path.join(folder, '%s.tif' % dID))
            if success:
                oFn = os.path.basename(next_file)
                self.docindex_builder.add_doc(str(mID), 'docCollection%s' % dCf,
                                         str(dID), oFn, 'tif')

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
            docindex.write(self.docindex_builder.to_string())
        logger.info('docIndex.xml written to disk')

        self.close()
        logger.info('Conversion done!')
