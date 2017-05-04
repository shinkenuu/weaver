#!/usr/env python

import os
from .Extract import extractor
from .Transform import transformer
from .Load import loader


def init_env(dir: str):
    if not os.path.exists(dir):
        os.makedirs(dir, exist_ok=True)


if __name__ in ('__init__', 'ETL'):
    init_env(extractor.extracted_dir_path)
    init_env(transformer.transformed_dir_path)

