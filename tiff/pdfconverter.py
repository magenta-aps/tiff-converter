import os

import comtypes.client


class PdfConverter(object):
    def convert(self, file):
        pass


class DocToPdfConverter(PdfConverter):
    WD_FORMAT_PDF = 17

    def __init__(self, temp_dir: os.path.abspath):
        self.temp_dir = temp_dir
        self.word = comtypes.client.CreateObject('Word.Application')

    def convert(self, file: os.path.abspath) -> os.path.abspath:
        # TODO: maybe use contextmanager instead

        pdf_path = os.path.join(os.path.abspath(self.temp_dir),
                                os.path.splitext(file)[0] + '.pdf')

        try:
            doc = self.word.Documents.Open(file)
            doc.SaveAs(pdf_path, FileFormat=DocToPdfConverter.WD_FORMAT_PDF)
            return pdf_path
        except:
            pass
        finally:
            doc.Close()


