import os
import platform

from util.logger import logger

if platform.system() == 'Windows':
    import comtypes.client


class MSOfficeToPdfConverter(object):
    WORD = 'Word.Application'
    EXCEL = 'Excel.Application'
    WD_FORMAT_PDF = 17

    def __init__(self, temp_dir: os.path.abspath, application: str):
        self.temp_dir = temp_dir
        self.application = application
        logger.info('Opening %s...' % application)
        self.app = comtypes.client.CreateObject(application)
        self.app.Visible = False
        logger.info('Opened %s' % application)

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
            if self.application == self.WORD:
                doc = self.app.Documents.Open(file)
                doc.SaveAs(pdf_path,
                           FileFormat=MSOfficeToPdfConverter.WD_FORMAT_PDF)
            elif self.application == self.EXCEL:
                doc = self.app.Workbooks.Open(file)
                doc.ExportAsFixedFormat(0, pdf_path, 1, 0)
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
        logger.info('Closing %s...' % self.application)
        self.app.Quit()
        logger.info('Closed %s' % self.application)


class PdfConverter(object):
    def convert(self, file):
        pass

    def close(self):
        pass
