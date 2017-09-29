import os
import platform
import subprocess

from util.logger import logger


class TiffConverter(object):
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

    def __init__(self, tempdir: os.path.abspath):
        self.tempdir = tempdir

    def convert(self, pdf: os.path.abspath, tiff: os.path.abspath) -> bool:
        temp_tiff = os.path.join(self.tempdir, os.path.basename(tiff))
        shell_command = self.COMMAND + ' -sOutputFile=' + temp_tiff + ' -f ' + pdf
        logger.debug('Converting %s to tiff...' % pdf)
        subprocess.call(shell_command, shell=True, stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE)
        if os.path.isfile(temp_tiff):
            logger.debug('Compressing %s ...' % tiff)
            subprocess.call('convert ' + temp_tiff + ' -compress lzw ' + tiff,
                            shell=True)
            if os.path.isfile(tiff):
                logger.info('Successfully converted %s to TIFF' % pdf)
                return True
        logger.error('Could not convert %s to TIFF' % pdf)
        return False
