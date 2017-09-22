import logging
import logging.config
import os
import platform


logging.config.fileConfig('logging.conf')
logger = logging.getLogger('root')

if platform.system() == 'Windows':
    import comtypes.client


class PdfConverter(object):
    def convert(self, file):
        pass

    def close(self):
        pass


class DocToPdfConverter(PdfConverter):
    WD_FORMAT_PDF = 17

    def __init__(self, temp_dir: os.path.abspath):
        self.temp_dir = temp_dir
        self.word = comtypes.client.CreateObject('Word.Application')

    def convert(self, file: os.path.abspath) -> os.path.abspath:
        # TODO: maybe use contextmanager instead

        if not os.path.isfile(file):
            logger.critical(file + ' not found!')
            raise FileNotFoundError(file + ' not found!')

        pdf_path = os.path.join(os.path.abspath(self.temp_dir),
                                os.path.splitext(os.path.basename(file))[
                                    0] + '.pdf')

        doc = None
        try:
            doc = self.word.Documents.Open(file)
            doc.SaveAs(pdf_path, FileFormat=DocToPdfConverter.WD_FORMAT_PDF)
            logger.info('Successfully converted %s to PDF' % file)
            return pdf_path
        except Exception as e:
            logger.error('Could not convert %s to PDF' % file)
            return None
        finally:
            if doc:
                doc.Close()

    def close(self):
        logger.info('Closed Word application')
        self.word.Quit()
