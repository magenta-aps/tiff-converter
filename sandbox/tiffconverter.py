import os
import subprocess

# NOTE: remember append Ghostscript to the PATH environment variable

# convert identify

gs_args = [
    'gswin32',
    '-q',
    '-dNOPAUSE',
    '-dBATCH',
    '-sDEVICE=tiff24nc',
    '-r150',
    '-sCompression=none',
    '-sOutputFile=out.tif',
    '-f', 'C:\\Users\\IEUser\\Documents\\jscript\\test\\resources\\sample.pdf'
]

gs_args2 = [
    'gswin32',
    '-q',
    '-dNOPAUSE',
    '-dBATCH',
    '-sDEVICE=tiff24nc',
    '-r150',
    '-sCompression=none',
    '-sOutputFile=out2.tif',
    '-f', 'C:\\Users\\IEUser\\Documents\\jscript\\test\\resources\\sample.pdf'
]


shell_command = ' '.join(gs_args)
shell_command2 = ' '.join(gs_args2)
subprocess.Popen(shell_command, shell=True)
subprocess.Popen(shell_command2, shell=True)


def convert(infile: os.path.abspath, outfile: os.path.abspath):
    pass


