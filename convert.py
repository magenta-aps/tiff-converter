import os
import tempfile
import re
import sys
import click

import tiff.converter
from siarddk.docmanager import LocalDocumentManager
from config import settings


@click.command()
@click.option('--source', type=click.Path(exists=True),
              help='Absolute path to root dir of files to convert')
@click.option('--target', type=click.Path(writable=True),
              help='Absolute path to target folder')
@click.option('--name',
              help='The name of the archival version e.g. AVID.MAG.1000')
@click.option('--tempdir',
              type=click.Path(exists=True, writable=True),
              default=os.path.join(tempfile.gettempdir(), 'tiff-conversion'),
              help='The temporary folder to use for tiff conversion')
@click.option('--append', is_flag=True, default=False,
              help='Use this option if you want to append data to an '
                   'already existing archival version')
def start_conversion(source, target, tempdir, name, append):

    settings['append'] = append

    regex_str = 'AVID\.[a-zA-Z]{2,4}\.[1-9][0-9]*'
    regex = re.compile(regex_str)
    name_ok = regex.match(name)
    if not name_ok:
        click.echo(
            'The name of the archival version must match '
            'the regular expression %s' % regex_str)
        sys.exit()

    converter = tiff.converter.Converter(source, target, tempdir, name,
                                         LocalDocumentManager(), settings)
    converter.run()


if __name__ == '__main__':
    start_conversion()
