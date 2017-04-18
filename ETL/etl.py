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


# TODO finish the chain logic
def etl(command: str, target, chain: bool=False):
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
            result = extractor.extract(target=target, chain=chain)
            if chain:
                command = 'transform'

        if command == 'transform':
            if chain:
                result = transformer.transform(into=target, result)
                command = 'load'
            else:
                transformer.transform(into=target)
                return

        if command == 'load':
            raise NotImplementedError('Load module of ETL')

        raise NotImplementedError('Invalid command: {}'.format(command))
    except Exception as err:
        _warder.ward_error('etl', err)
