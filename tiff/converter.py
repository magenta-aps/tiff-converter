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
        elif ext in ['bmp', 'gif', 'jpg', 'png', 'tif', 'tiff']:
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
    # TODO: use abstract factory to provide all the strategies
    def __init__(
            self,
            source: os.path.abspath,
            target: os.path.abspath,
            conversion_dir: os.path.abspath,
            name: str,
            settings: dict,
            file_path_strategy,
            initialization_strategy,
            docindex_handler
    ):
        self.source = source
        self.target = target
        self.conversion_dir = conversion_dir
        self.name = name
        self.settings = settings
        self.file_path_strategy = file_path_strategy
        self.initialization_strategy = initialization_strategy
        self.docindex_handler = docindex_handler

        self.complex_converter = ComplexConverter(conversion_dir)

        create_conversion_folder(conversion_dir)
        clean_conversion_folder(conversion_dir)

        logger.info('Initialized Converter')

    def close(self):
        self.complex_converter.close()

    def run(self):
        logger.info('Starting conversion...')

        self.initialization_strategy.prepare(self)

        next_file, tiff_path = self.file_path_strategy.get_next(self)
        while next_file:
            # Convert file to TIFF
            success = self.complex_converter.convert(next_file, tiff_path)
            if success:
                self.docindex_handler.add_file(next_file, tiff_path)

            clean_conversion_folder(self.conversion_dir)
            next_file, tiff_path = self.file_path_strategy.get_next(self)

        self.docindex_handler.write()
        self.close()

        logger.info('Conversion done!')

    # def _reuse_source_as_target_run(self):
    #
    #     # The source must be the folder where the AVID.XYZ.nnnn.m's are located
    #
    #     self.docindex_handler = DocIndexHandler(
    #         os.path.join(self.source, '%s.1' % self.name, 'Indices',
    #                      'docIndex.xml'))
    #     docindex = self.docindex_handler.get_index()
    #
    #     for doc in docindex:
    #         dID = doc[0].text
    #         mID = doc[1].text
    #         dCf = doc[2].text
    #         path = os.path.join(self.source, '%s.%s' % (self.name, mID),
    #                             'Documents', dCf, dID)
    #         source_file = os.path.join(path, os.listdir(path)[0])
    #
    #         success = self.complex_converter.convert(
    #             source_file, os.path.join(path, '1.tif'))
    #         if success:
    #             os.remove(source_file)
    #
    #         clean_conversion_folder(self.conversion_dir)
