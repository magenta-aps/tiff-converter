import json
import os


def message(next_file: os.path.abspath, tiff_path: os.path.abspath):
    return json.dumps({
        'next': next_file,
        'tiff': tiff_path
    })
