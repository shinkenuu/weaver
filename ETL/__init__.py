#!/usr/env python

import os
from . import etl


def init_env():
    for key, dir in etl.dirs_dict.items():
        if not os.path.exists(dir):
            os.makedirs(dir)


if __name__ in ('__init__', 'ETL'):
    init_env()
