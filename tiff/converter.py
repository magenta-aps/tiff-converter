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
            docindex_handler,
            success_strategy
    ):
        self.source = source
        self.target = target
        self.conversion_dir = conversion_dir
        self.name = name
        self.settings = settings
        self.file_path_strategy = file_path_strategy
        self.initialization_strategy = initialization_strategy
        self.docindex_handler = docindex_handler
        self.success_strategy = success_strategy

        self.complex_converter = ComplexConverter(conversion_dir)

        create_conversion_folder(conversion_dir)
        clean_conversion_folder(conversion_dir)

        logger.info('Initialized Converter')

    def close(self):
        self.complex_converter.close()

    def run(self):
        logger.info('Starting conversion...')

        self.initialization_strategy.prepare(self)

        self.next_file, self.tiff_path = self.file_path_strategy.get_next(self)
        while self.next_file:
            success = self.complex_converter.convert(self.next_file,
                                                     self.tiff_path)
            self.success_strategy.post_convert(success, self)
            clean_conversion_folder(self.conversion_dir)
            self.next_file, self.tiff_path = self.file_path_strategy.get_next(
                self)

        self.docindex_handler.write()
        self.close()

        logger.info('Conversion done!')
