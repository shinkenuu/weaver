#!/usr/bin/env python3

import warder
from . import extractor, loader, transformer

_warder = warder.Warder()


def etl(command: str, source: str, target: str, chain_until: str):
    """
    Receives command and delegates it to the right etl module
    :param command: extract | transform | load
    :param source: the data source [ftp|mssql|msaccess]
    :param target: the immediate destination of the referred data [server.database|database.table]
    :param chain_until: pipe results since command until ...
    :return: 
    """
    try:
        result = None
        if command not in ('extract', 'transform', 'load'):
            raise ValueError('Invalid command: {}'.format(command))
        if command == 'extract':
            result = extractor.extract(source=source, target=target)
            _warder.ward_progress('etl', 'OK', '{} completed for {} from {}'.format(command, target, source))
            if chain_until == 'transform' or chain_until == 'load':
                command = 'transform'
        if command == 'transform':
            result = transformer.transform(into=target, source=source, input_data=result)
            _warder.ward_progress('etl', 'OK', '{} completed for {} from {}'.format(command, target, source))
            if chain_until == 'load':
                command = 'load'
                source = result
        if command == 'load':
            loader.load(into=target, source=source)
            _warder.ward_progress('etl', 'OK', '{} completed for {} with {}'.format(command, target, source))
    except Exception as err:
        _warder.ward_error('etl', err)
