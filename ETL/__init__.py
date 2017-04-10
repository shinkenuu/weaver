#!/usr/env python

import os
from . import etl


def init_env():
    for dir in etl.dirs_dict:
        if not os.path.exists(dir):
            os.makedirs(dir)


if __name__ == '__init__':
    init_env()
