import os
import warder
from ETL.Extract import extractor
from ETL.Transform import transformer

_warder = warder.Warder()

dirs_dict = {
    'root': '{}/weaver/etl/'.format(os.path.expanduser('~')),
    'raw': extractor.raw_dir_path,
    'transformed': '{}/weaver/etl/transformed/'.format(os.path.expanduser('~')),
}


def etl(command: str, target: str):
    """
    Receives command and delegates it to the right ETL module
    :param command: 
    :param target: the immediate destination of the referred data
    :param chain: pipe result from command to the next process
    :return: 
    """
    try:
        result = None
        if command == 'extract':
            result = extractor.extract(target=target)
        elif command == 'transform':
            result = transformer.transform(into=target)
        elif command == 'load':
            raise NotImplementedError('Load module of ETL')
        else:
            raise NotImplementedError('Invalid command: {}'.format(command))
        _warder.ward_progress('etl', 'OK', '{} completed for {}'.format(command, target))
    except Exception as err:
        _warder.ward_error('etl', err)
