import datetime
import os


def create_doc_folder(target: os.path.abspath, name: str, mID: int, dCf: int,
                      dID: int):
    folder = os.path.join(target, '%s.%s' % (name, mID),
                          'Documents', 'docCollection%s' % dCf, str(dID)
                          )
    if not os.path.isdir(folder):
        os.makedirs(folder)

    return folder


def rename_old_av_folders(target: os.path.abspath, name: str):
    contents = os.listdir(target)
    for f in contents:
        if name in f:
            new_name = os.path.join(
                target, '%s_%s' % (
                f, datetime.datetime.now().strftime('%Y-%m-%d_%H%M%S')))
            os.rename(os.path.join(target, f), new_name)
