#!/usr/env python3

import os

from reporttool.xl import base


def check_dirs():
    if not os.path.isdir(base.REPORT_ROOT_PATH):
        os.mkdir(base.REPORT_ROOT_PATH)
    if not os.path.isdir(os.path.join(base.REPORT_ROOT_PATH, 'evolution')):
        os.mkdir(os.path.join(base.REPORT_ROOT_PATH, 'evolution'))

if __name__ == 'reporttool':
    check_dirs()
