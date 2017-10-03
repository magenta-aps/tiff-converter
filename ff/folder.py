import datetime
import os
import shutil


def clean_conversion_folder(folder: os.path.abspath):
    for f in os.listdir(folder):
        f = os.path.join(folder, f)
        if os.path.isfile(f):
            os.remove(f)


def create_conversion_folder(folder: os.path.abspath):
    try:
        shutil.rmtree(folder)
    except OSError:
        pass
    os.makedirs(folder)


def create_doc_folder(target: os.path.abspath, name: str, mID: int, dCf: int,
                      dID: int):
    folder = os.path.join(target, '%s.%s' % (name, mID),
                          'Documents', 'docCollection%s' % dCf, str(dID)
                          )
    if not os.path.isdir(folder):
        os.makedirs(folder)

    return folder


def create_target_folder(target: os.path.abspath):
    if not os.path.isdir(target):
        os.makedirs(target)


def rename_old_av_folders(target: os.path.abspath, name: str):
    contents = os.listdir(target)
    for f in contents:
        if name in f:
            new_name = os.path.join(
                target, '%s_%s' % (
                f, datetime.datetime.now().strftime('%Y-%m-%d_%H%M%S')))
            os.rename(os.path.join(target, f), new_name)
