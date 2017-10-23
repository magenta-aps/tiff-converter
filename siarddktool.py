import os
import tempfile
import re
import sys
import click

import tiff.converter
from siarddk.fileindex import FileIndex
from config import settings


@click.group()
@click.option('--target', type=click.Path(writable=True),
              help='Path to target folder')
@click.option('--name',
              help='The name of the archival version e.g. AVID.MAG.1000')
@click.pass_context
def cli(ctx, target, name):
    regex_str = 'AVID\.[A-ZÆØÅ]{2,4}\.[1-9][0-9]*'
    regex = re.compile(regex_str)
    name_ok = regex.match(name)
    if not name_ok:
        click.echo(
            'The name of the archival version must match '
            'the regular expression %s' % regex_str)
        sys.exit()

    ctx.obj['target'] = os.path.abspath(target)
    ctx.obj['name'] = name


@click.command()
@click.option('--source', type=click.Path(exists=True),
              help='Absolute path to root dir of files to convert')
@click.option('--tempdir',
              type=click.Path(exists=True, writable=True),
              default=os.path.join(tempfile.gettempdir(), 'tiff-conversion'),
              help='The temporary folder to use for tiff conversion')
@click.option('--append', is_flag=True, default=False,
              help='Use this option if you want to append data to an '
                   'already existing archival version')
@click.pass_context
def convert(ctx, source, tempdir, append):
    settings['append'] = append
    converter = tiff.converter.Converter(
        os.path.abspath(source), ctx.obj['target'], tempdir, ctx.obj['name'],
        settings)
    converter.run()


@click.command()
@click.option('--add', multiple=True,
              help='Add file or folder to fileIndex.xml '
                   '(multiple occurences of the --add option is allowed)')
@click.option('--remove', is_flag=True, default=False,
              help='Remove all files from fileIndex.xml except for those '
                   'in the Tables folder')
@click.pass_context
def fileindex(ctx, add, remove):
    fileindex_handler = FileIndex(ctx.obj['target'], ctx.obj['name'])

    if add:
        for f in [os.path.abspath(f) for f in add]:
            if os.path.isfile(f):
                fileindex_handler.add_file(f)
            elif os.path.isdir(f):
                fileindex_handler.add_folders([f])
    if remove:
        fileindex_handler.remove_all()

    fileindex_handler.write(
        os.path.join(ctx.obj['target'], '%s.1' % ctx.obj['name'],
                     'Indices'))


cli.add_command(convert)
cli.add_command(fileindex)

if __name__ == '__main__':
    cli(obj={})
