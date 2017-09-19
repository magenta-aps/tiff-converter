import os
import subprocess

GS_ARGS = [
    'gswin32',
    '-q',
    '-dNOPAUSE',
    '-dBATCH',
    '-sDEVICE=tiff24nc',
    '-r150',
    '-sCompression=none',
]

COMMAND = ' '.join(GS_ARGS)


def convert(pdf: os.path.abspath, tiff: os.path.abspath) -> int:
    shell_command = COMMAND + ' -sOutputFile=' + tiff + ' -f ' + pdf
    subprocess.Popen(shell_command, shell=True)
    return 0
