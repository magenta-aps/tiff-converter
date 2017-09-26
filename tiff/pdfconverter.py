import os
import platform

from util.logger import logger


if platform.system() == 'Windows':
    import comtypes.client


class MSOfficeToPdfConverter(object):
    WD_FORMAT_PDF = 17

    def __init__(self, temp_dir: os.path.abspath, application: str):
        self.temp_dir = temp_dir
        logger.info('Opening Word application...')
        self.app = comtypes.client.CreateObject(application)
        logger.info('Opened Word application')

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
            logger.debug('Opening %s ...' % file)
            doc = self.app.Documents.Open(file)
            doc.SaveAs(pdf_path, FileFormat=MSOfficeToPdfConverter.WD_FORMAT_PDF)
            logger.info('Successfully converted %s to PDF' % file)
            return pdf_path
        except Exception as e:
            logger.error('Could not convert %s to PDF' % file)
            return None
        finally:
            if doc:
                doc.Close()
                logger.debug('Closed %s' % file)

    def close(self):
        logger.info('Closing Word application...')
        self.app.Quit()
        logger.info('Closed Word application')


class PdfConverter(object):
    def convert(self, file):
        pass

    def close(self):
        pass
