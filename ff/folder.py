import os


def create_doc_folder(target: os.path.abspath, name: str, mID: int, dCf: int,
                      dID: int):
    folder = os.path.join(target, '%s.%s' % (name, mID),
                          'Documents', 'docCollection%s' % dCf, str(dID)
                          )
    if not os.path.isdir(folder):
        os.makedirs(folder)

    return folder

