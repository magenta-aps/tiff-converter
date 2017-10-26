import siarddk.docmanager
import siarddk.docindex
import tiff.filehandler
from tiff.pdfconverter import MSOfficeToPdfConverter
import tiff.tiffconverter
from ff.folder import *
from siarddk.docindex import DocIndexHandler

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
    ):
        self.source = source
        self.target = target
        self.conversion_dir = conversion_dir
        self.name = name
        self.settings = settings
        self.file_path_strategy = file_path_strategy
        self.initialization_strategy = initialization_strategy

        self.complex_converter = ComplexConverter(conversion_dir)
        self.docindex_handler = DocIndexHandler()
        self.docmanager = siarddk.docmanager.LocalDocumentManager(
            self.settings['append'])

        create_conversion_folder(conversion_dir)
        clean_conversion_folder(conversion_dir)

        logger.info('Initialized Converter')

    def close(self):
        self.complex_converter.close()

    def run(self):
        logger.info('Starting conversion...')

        if self.settings['in-place']:
            self._reuse_source_as_target_run()
        else:
            self._new_target_run()

        self.close()
        logger.info('Conversion done!')

    def _new_target_run(self):
        self.initialization_strategy.prepare(self)

        if self.settings['append']:
            self.docindex_handler = DocIndexHandler(
                os.path.join(self.target, '%s.1' % self.name, 'Indices',
                             'docIndex.xml'))
            mID, dCf, dID = self.docindex_handler.get_ids()
        else:
            mID, dCf, dID = (1, 1, 1)

        self.docmanager.set_location(mID, dCf, dID)

        success = True
        next_file = self.file_path_strategy.get_next()
        while next_file:
            if success:
                mID, dCf, dID = self.docmanager.get_location()

            folder = create_doc_folder(self.target, self.name, mID, dCf, dID)

            # Convert file to TIFF
            success = self.complex_converter.convert(
                next_file, os.path.join(folder, '1.tif'))
            if success:
                oFn = os.path.basename(next_file)
                self.docindex_handler.add_doc(str(mID), 'docCollection%s' % dCf,
                                              str(dID), oFn, 'tif')
            else:
                os.rmdir(folder)

            clean_conversion_folder(self.conversion_dir)
            next_file = self.file_path_strategy.get_next()

        # Write docIndex to file
        indices_path = os.path.join(self.target, '%s.1' % self.name, 'Indices')
        self.docindex_handler.write(indices_path)

    def _reuse_source_as_target_run(self):

        # The source must be the folder where the AVID.XYZ.nnnn.m's are located

        self.docindex_handler = DocIndexHandler(
            os.path.join(self.source, '%s.1' % self.name, 'Indices',
                         'docIndex.xml'))
        docindex = self.docindex_handler.get_index()

        for doc in docindex:
            dID = doc[0].text
            mID = doc[1].text
            dCf = doc[2].text
            path = os.path.join(self.source, '%s.%s' % (self.name, mID),
                                'Documents', dCf, dID)
            source_file = os.path.join(path, os.listdir(path)[0])

            success = self.complex_converter.convert(
                source_file, os.path.join(path, '1.tif'))
            if success:
                os.remove(source_file)

            clean_conversion_folder(self.conversion_dir)
