import os


FOLDERS = 100
FILES = 10000
BASEDIR = '/tmp/folders'


def touch(fname, times=None):
    with open(fname, 'a'):
        os.utime(fname, times)


for i in range(FOLDERS):
    folder = os.path.join(BASEDIR, str(i))
    if not os.path.isdir(folder):
        os.mkdir(folder)
    for j in range(FILES):
        f = os.path.join(folder, str(j) + '.tif')
        touch(f)