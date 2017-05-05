#!/usr/env python

import os
from . import extractor, loader, transformer


def init_env(dir_path: str):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path, exist_ok=True)


if __name__ in ('__init__', 'etl'):
    init_env(dir_path=extractor.EXTRACTED_DIR_PATH)
    #  init_env(dir_path=transformer.READY_FILES_ROOT_DIR_PATH)
    for key, file_path in transformer.READY_FILES_PATH_DICT.items():
        init_env(dir_path=file_path.replace(os.path.basename(file_path), ''))
