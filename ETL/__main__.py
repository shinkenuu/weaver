#!/usr/bin/env python

import sys
import argparse
from ETL import etl

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser(description='Extract, Transform or Load data')
    arg_parser.add_argument('command', nargs=1, type=str, choices=['extract', 'transform', 'load'],
                            help='extract|transform|load')
    arg_parser.add_argument('--input', nargs='+', type=argparse.FileType('r'), help='file(s) to act on')
    arg_parser.add_argument('--target', nargs=1, type=str, help='<database>.<table>')
    parsed_args = arg_parser.parse_args(sys.argv[1:])
    etl.etl(command=parsed_args.command[0], input=parsed_args.input, target=parsed_args.target)
