#!/usr/bin/env python

import sys
import argparse
from ETL import etl

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser(description='Extract, Transform or Load data')
    arg_parser.add_argument('command', nargs=1, type=str, choices=['extract', 'transform', 'load'],
                            help='extract|transform|load')
    if sys.argv[1] == 'extract':
        arg_parser.add_argument('--target', nargs=1, type=str, help='[<database>.<table>] or [<database>]')
    elif sys.argv[1] == 'transform':
        # arg_parser.add_argument('--input', nargs='+', type=argparse.FileType('r'), help='file(s) to act on')
        arg_parser.add_argument('--target', nargs=1, type=str, help='[<database>.<table>]')
    elif sys.argv[1] == 'load':
        pass
    parsed_args = arg_parser.parse_args(sys.argv[1:])
    etl.etl(command=parsed_args.command[0][0], target=parsed_args.target)
