import os
import comtypes.client

FORMAT_PDF = 32
SOURCE_DIR = 'C:/Users/IEUser/Documents/jscript/test/resources'
TARGET_DIR = 'C:/Users/IEUser/Documents/jscript'

app = comtypes.client.CreateObject('Powerpoint.Application')
# app.Visible = False

infile = os.path.join(os.path.abspath(SOURCE_DIR), 'sample.pptx')
outfile = os.path.join(os.path.abspath(TARGET_DIR), 'powerpoint.pdf')

print(infile)
print(outfile)

doc = app.Presentations.Open(infile)
doc.SaveAs(outfile, FileFormat=FORMAT_PDF)
# doc.ExportAsFixedFormat(0, outfile, 1, 0)
doc.Close()

app.Quit()
