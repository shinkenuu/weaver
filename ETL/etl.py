#!/usr/bin/env python

import argparse
import sys
import warder
from ETL.Transform import transformer

etl_warder = warder.Warder()


def main():
    """
        NAME
            ETL

        SYNOPSIS
            etl.py [COMMAND] [OPTIONS]

        COMMAND
            <b>extract</b>
            <b>transform</b>
            <b>load</b>

        OPTIONS
            --<b>input</b> [path/to/filex1[ path/to/filexN]]
            --<b>target</b> [<database>.<table>]
    """
    arg_parser = argparse.ArgumentParser(description='Extract, Transform or Load data')
    arg_parser.add_argument('command', nargs=1, type=str, choices=['extract', 'transform', 'load'],
                            help='extract|transform|load')
    arg_parser.add_argument('--input', nargs='+', type=argparse.FileType('r'), help='file(s) to act on')
    arg_parser.add_argument('--target', nargs=1, type=str, help='<database>.<table>')
    parsed_args = arg_parser.parse_args(sys.argv[1:])

    try:
        if parsed_args.command[0] == 'extract':
            raise NotImplementedError('Extraction module of ETL')
        elif parsed_args.command[0] == 'transform':
            transformer.transform(
                into=parsed_args.target,
                raw_data_file_names=parsed_args.input)
        elif parsed_args.command[0] == 'load':
            raise NotImplementedError('Loading module of ETL')
        else:
            raise NotImplementedError('Invalid command: {}'.format(parsed_args.command))
    except Exception as err:
        etl_warder.ward_error('etl', err)


if __name__ == '__main__':
    main()
