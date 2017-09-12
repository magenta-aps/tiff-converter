import os
import shutil
import sys

TEMPLATE_DOC = 'demo.docx'
TARGET_DIR = 'C:/Users/IEUser/Documents/jscript/docs2'
NUMBER_OF_COPIES = 100

if len(sys.argv) > 1:
    offset = int(sys.argv[1])
else:
    offset = 0

target_dir = os.path.abspath(TARGET_DIR)
if not os.path.isdir(target_dir):
    os.mkdir(target_dir)

name, ext = os.path.splitext(TEMPLATE_DOC)
basedir = os.path.abspath(os.path.dirname(__file__))
for i in range(NUMBER_OF_COPIES):
    filename = name + str(i + offset) + ext
    src = os.path.join(basedir, TEMPLATE_DOC)
    dst = os.path.join(TARGET_DIR, filename)
    shutil.copyfile(src, dst)
