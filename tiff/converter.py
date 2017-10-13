import siarddk.docmanager
import siarddk.docindex
import tiff.filehandler
from tiff.pdfconverter import MSOfficeToPdfConverter
import tiff.tiffconverter
from ff.folder import *

from util.logger import logger


class ComplexConverter(object):
    def __init__(self, conversion_dir: os.path.abspath):
        self.word_converter = MSOfficeToPdfConverter(
            conversion_dir, MSOfficeToPdfConverter.WORD)
        self.excel_converter = MSOfficeToPdfConverter(
            conversion_dir, MSOfficeToPdfConverter.EXCEL)
        self.powerpoint_converter = MSOfficeToPdfConverter(
            conversion_dir, MSOfficeToPdfConverter.POWERPOINT)
        self.tiff_converter = tiff.tiffconverter.TiffConverter(conversion_dir)

    def convert(self, source: os.path.abspath, target: os.path.abspath) -> bool:
        ext = os.path.splitext(source)[1][1:].lower()

        pdf = None
        if ext in ['doc', 'docx']:
            pdf = self.word_converter.convert(source)
        elif ext in ['xls', 'xlsx']:
            pdf = self.excel_converter.convert(source)
        elif ext in ['ppt', 'pptx']:
            pdf = self.powerpoint_converter.convert(source)
        elif ext == 'pdf':
            pdf = source
        elif ext == 'jpg':
            return self.tiff_converter.image_magick_convert(source, target)

        if pdf:
            return self.tiff_converter.pdf_convert(pdf, target)
        else:
            return False

    def close(self):
        self.word_converter.close()
        self.excel_converter.close()
        self.powerpoint_converter.close()


class Converter(object):
    def __init__(
            self,
            source: os.path.abspath,
            target: os.path.abspath,
            conversion_dir: os.path.abspath,
            name: str,
            docmanager: siarddk.docmanager.DocumentManager,
            settings: dict,
            old_docindex=None
    ):
        self.source = source
        self.target = target
        self.conversion_dir = conversion_dir
        self.name = name
        self.docmanager = docmanager
        self.settings = settings

        self.docindex_builder = siarddk.docindex.DocIndexBuilder(old_docindex)
        self.complex_converter = ComplexConverter(conversion_dir)

        create_target_folder(target)
        if not settings['append']:
            rename_old_av_folders(target, name)
        create_conversion_folder(conversion_dir)
        clean_conversion_folder(conversion_dir)

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

            folder = create_doc_folder(self.target, self.name, mID, dCf, dID)

            # Convert file to TIFF
            success = self.complex_converter.convert(
                next_file, os.path.join(folder, '1.tif'))
            if success:
                oFn = os.path.basename(next_file)
                self.docindex_builder.add_doc(str(mID), 'docCollection%s' % dCf,
                                              str(dID), oFn, 'tif')

            clean_conversion_folder(self.conversion_dir)
            next_file = filehandler.get_next_file()

        # TODO: move this elsewhere... (responsibility erosion)
        # Write docIndex to file
        logger.info('Writing docIndex.xml to disk...')
        indices_path = os.path.join(self.target, '%s.1' % self.name, 'Indices')
        if not self.settings['append']:
            os.mkdir(indices_path)
        docindex_path = os.path.join(indices_path, 'docIndex.xml')
        with open(docindex_path, 'w') as docindex:
            docindex.write(self.docindex_builder.to_string())
        logger.info('docIndex.xml written to disk')

        self.close()
        logger.info('Conversion done!')
