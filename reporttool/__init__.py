#!/usr/env python3

import os
from . import _base


def check_dirs():
    if not os.path.isdir(_base.REPORT_ROOT_PATH):
        os.mkdir(_base.REPORT_ROOT_PATH)
    if not os.path.isdir(os.path.join(_base.REPORT_ROOT_PATH, 'evolution')):
        os.mkdir(os.path.join(_base.REPORT_ROOT_PATH, 'evolution'))

if __name__ == 'reporttool':
    check_dirs()
