#!/usr/bin/env python3

import sys
import argparse
from etl import main

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser(description='Extract, Transform or Load data')
    arg_parser.add_argument('command', nargs=1, type=str, choices=['extract', 'transform', 'load'],
                            help='extract|transform|load')
    if sys.argv[1] == 'extract':
        arg_parser.add_argument('--source', nargs=1, type=str, help='source name: [ftp|mssql|msaccess|v5]')
        arg_parser.add_argument('--target', nargs=1, type=str, help='target name: [database.table|server.database]')
        arg_parser.add_argument('--chain', nargs='?', type=str, help='chain until [transform|load]', default='',
                                choices=['transform', 'load'])
    elif sys.argv[1] == 'transform':
        arg_parser.add_argument('--source', nargs=1, type=str, help='source name: [ftp|mssql|msaccess|v5]')
        arg_parser.add_argument('--target', nargs=1, type=str, help='[<database>.<table>]')
        arg_parser.add_argument('--chain', nargs='?', type=str, help='chain until [load]', default='',
                                choices=['load'])
    elif sys.argv[1] == 'load':
        arg_parser.add_argument('--source', nargs=1, type=argparse.FileType('r'), help='source name: blk file path')
        arg_parser.add_argument('--target', nargs=1, type=str, help='[<database>.<table>]')
    parsed_args = arg_parser.parse_args(sys.argv[1:])
    main.etl(command=parsed_args.command[0], target=parsed_args.target[0],
             source=parsed_args.source[0], chain_until=parsed_args.chain)
