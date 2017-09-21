import os
import platform
import subprocess
import tempfile

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
TEMP_DIR = tempfile.gettempdir()


def convert(pdf: os.path.abspath, tiff: os.path.abspath) -> bool:
    temp_tiff = os.path.join(TEMP_DIR, os.path.basename(tiff))
    shell_command = COMMAND + ' -sOutputFile=' + temp_tiff + ' -f ' + pdf
    subprocess.call(shell_command, shell=True, stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE)
    if os.path.isfile(temp_tiff):
        # Conversion succeeded
        subprocess.call('convert ' + temp_tiff + ' -compress lzw ' + tiff,
                        shell=True)
        if os.path.isfile(tiff):
            return True
    return False
