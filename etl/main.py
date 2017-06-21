#!/usr/bin/env python3

import argparse
import sys
import warder
from etl import extractor, loader, transformer

_warder = warder.Warder()


def etl(command: str, source: str, target: str, chain_until: str):
    """
    Receives command and delegates it to the right etl module
    :param command: extract | transform | load
    :param source: the data source [ftp|mssql|msaccess|v5]
    :param target: the immediate destination of the referred data [server.database|database.table]
    :param chain_until: pipe results since command until ...
    :return: 
    """
    try:
        result = None
        if command not in ('extract', 'transform', 'load'):
            raise ValueError('Invalid command: {}'.format(command))
        if command == 'extract':
            print('Extracting data for {} from {}'.format(target, source))
            _warder.ward_progress('etl', 'INIT', 'Extracting data for {} from {}'.format(target, source))
            result = extractor.extract(source=source, target=target)
            print('Extraction completed')
            _warder.ward_progress('etl', 'OK', '{} completed for {} from {}'.format(command, target, source))
            if chain_until == 'transform' or chain_until == 'load':
                command = 'transform'
        if command == 'transform':
            print('Transforming data for {} from {}'.format(target, source))
            _warder.ward_progress('etl', 'INIT', 'Transforming data for {} from {}'.format(target, source))
            result = transformer.transform(into=target, source=source, input_data=result)
            print('Transformation completed')
            _warder.ward_progress('etl', 'OK', '{} completed for {} from {}'.format(command, target, source))
            if chain_until == 'load':
                command = 'load'
                source = result
        if command == 'load':
            print('Loading data for {} from {}'.format(target, source))
            _warder.ward_progress('etl', 'INIT', 'Loading data for {} from {}'.format(target, source))
            loader.load(into=target, source=source)
            print('Load completed')
            _warder.ward_progress('etl', 'OK', '{} completed for {} with {}'.format(command, target, source))
        return 0
    except Exception as err:
        print(err)
        _warder.ward_error('etl', err)
        return -1

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
    etl(command=parsed_args.command[0], target=parsed_args.target[0],
        source=parsed_args.source[0], chain_until=parsed_args.chain)
