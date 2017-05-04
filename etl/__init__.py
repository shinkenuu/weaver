#!/usr/env python

import os
from . import extractor, loader, transformer


def init_env(dir_path: str):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path, exist_ok=True)


if __name__ in ('__init__', 'etl'):
    init_env(dir_path=extractor.EXTRACTED_DIR_PATH)
    init_env(dir_path=transformer.READY_DIR_PATH)
