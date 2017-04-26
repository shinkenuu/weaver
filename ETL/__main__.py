#!/usr/bin/env python

import sys
import argparse
from ETL import etl

#  TODO fix target to accept just one value
if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser(description='Extract, Transform or Load data')
    arg_parser.add_argument('command', nargs=1, type=str, choices=['extract', 'transform', 'load'],
                            help='extract|transform|load')
    if sys.argv[1] == 'extract':
        arg_parser.add_argument('--target', nargs=1, type=str, help='[database.table] or [database]')
        arg_parser.add_argument('--chain', nargs='?', type=str, help='chain until [transform|load]', default='',
                                choices=['transform', 'load'])
    elif sys.argv[1] == 'transform':
        arg_parser.add_argument('--target', nargs=1, type=str, help='[<database>.<table>]')
        arg_parser.add_argument('--chain', nargs='?', type=str, help='chain until [load]', default='',
                                choices=['load'])
    elif sys.argv[1] == 'load':
        arg_parser.add_argument('--target', nargs=1, type=str, help='[<database>.<table>]')
    parsed_args = arg_parser.parse_args(sys.argv[1:])
    etl.etl(command=parsed_args.command[0], target=parsed_args.target[0], chain_until=parsed_args.chain)
