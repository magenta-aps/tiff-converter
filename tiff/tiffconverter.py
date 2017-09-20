import os
import platform
import subprocess

GS_ARGS = [
    'gswin32c' if platform.system() == 'Windows' else 'gs',
    '-q',
    '-dNOPAUSE',
    '-dBATCH',
    '-sDEVICE=tiff24nc',
    '-r150',
    '-sCompression=none',
]

COMMAND = ' '.join(GS_ARGS)


def convert(pdf: os.path.abspath, tiff: os.path.abspath) -> bool:
    shell_command = COMMAND + ' -sOutputFile=' + tiff + ' -f ' + pdf
    subprocess.call(shell_command, shell=True, stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE)
    if os.path.isfile(tiff):
        return True
    else:
        return False
