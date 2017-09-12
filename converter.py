import os
import comtypes.client

WD_FORMAT_PDF = 17
SOURCE_DIR = 'C:/Users/IEUser/Documents/jscript/docs'
TARGET_DIR = 'C:/Users/IEUser/Documents/jscript/pdfs'

# Create target dir...

docs = [
    os.path.join(os.path.abspath(SOURCE_DIR), f)
    for f in os.listdir(SOURCE_DIR)
]
pdfs = [
    os.path.join(os.path.abspath(TARGET_DIR), os.path.splitext(f)[0] + '.pdf')
    for f in os.listdir(SOURCE_DIR)
]

word_app = comtypes.client.CreateObject('Word.Application')
word_app.Visible = False

for i in range(len(docs)):
    print(docs[i])
    doc = word_app.Documents.Open(docs[i])
    doc.SaveAs(pdfs[i], FileFormat=WD_FORMAT_PDF)
    doc.Close()

word_app.Quit()
