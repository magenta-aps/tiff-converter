import os
import comtypes.client

FORMAT_PDF = 17
SOURCE_DIR = 'C:/Users/IEUser/Documents/jscript/test/resources/root3'
TARGET_DIR = 'C:/Users/IEUser/Documents/jscript'

app = comtypes.client.CreateObject('Excel.Application')
app.Visible = False

infile = os.path.join(os.path.abspath(SOURCE_DIR), 'spreadsheet1.xlsx')
outfile = os.path.join(os.path.abspath(TARGET_DIR), 'spreadsheet1.pdf')

print(infile)
print(outfile)

doc = app.Workbooks.Open(infile)
# doc.SaveAs(outfile, FileFormat=FORMAT_PDF)
doc.ExportAsFixedFormat(0, outfile, 1, 0)
doc.Close()

app.Quit()
