
import warder
from ETL.Extract import extractor
from ETL.Transform import transformer
from ETL.Load import loader

_warder = warder.Warder()


def etl(command: str, target: str, chain_until: str):
    """
    Receives command and delegates it to the right ETL module
    :param command: extract | transform | load
    :param target: the immediate destination of the referred data
    :param chain_until: pipe results since command until ...
    :return: 
    """
    try:
        result = None
        if command not in ('extract', 'transform', 'load'):
            raise NotImplementedError('Invalid command: {}'.format(command))
        if command == 'extract':
            result = extractor.extract(target=target)
            _warder.ward_progress('etl', 'OK', '{} completed for {}'.format(command, target))
            if chain_until == 'transform' or chain_until == 'load':
                command = 'transform'
        if command == 'transform':
            result = transformer.transform(input_data=result, into=target)
            _warder.ward_progress('etl', 'OK', '{} completed for {}'.format(command, target))
            if chain_until == 'load':
                command = 'load'
        if command == 'load':
            loader.load(input_data=result, into=target)
            _warder.ward_progress('etl', 'OK', '{} completed for {}'.format(command, target))
    except Exception as err:
        _warder.ward_error('etl', err)
