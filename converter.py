import os
import sys
import comtypes.client

WD_FORMAT_PDF = 17
# SOURCE_DIR = 'C:/Users/IEUser/Documents/jscript/docs'
TARGET_DIR = 'C:/Users/IEUser/Documents/jscript/pdfs'

source_dir = sys.argv[1]

target_dir = os.path.abspath(TARGET_DIR)
if not os.path.isdir(target_dir):
    os.mkdir(target_dir)

docs = [
    os.path.join(os.path.abspath(source_dir), f)
    for f in os.listdir(source_dir)
]
pdfs = [
    os.path.join(os.path.abspath(TARGET_DIR), os.path.splitext(f)[0] + '.pdf')
    for f in os.listdir(source_dir)
]

word_app = comtypes.client.CreateObject('Word.Application')
word_app.Visible = False

for i in range(len(docs)):
    print(docs[i])
    doc = word_app.Documents.Open(docs[i])
    doc.SaveAs(pdfs[i], FileFormat=WD_FORMAT_PDF)
    doc.Close()

word_app.Quit()
