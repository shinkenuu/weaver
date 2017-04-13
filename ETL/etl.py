import os
import warder
from ETL.Extract import extractor
from ETL.Transform import transformer

_warder = warder.Warder()

dirs_dict = {
    'root': '{}/weaver/etl/'.format(os.path.expanduser('~')),
    'raw': '{}/weaver/etl/raw/'.format(os.path.expanduser('~')),
    'transformed': '{}/weaver/etl/transformed/'.format(os.path.expanduser('~')),
}


def etl(command: str, target):
    """
    Receives command and delegates it to the right ETL module
    :param command: 
    :param target: the immediate destination of the refered data
    :return: 
    """
    try:
        target = target[0]
        if command == 'extract':
            extractor.extract(target=target, output_dir='{0}{1}/'.format(dirs_dict['raw'], target))
        elif command == 'transform':
            transformer.transform(into=target, output_dir='{0}{1}/'.format(dirs_dict['transformed'], target))
        elif command == 'load':
            raise NotImplementedError('Load module of ETL')
        else:
            raise NotImplementedError('Invalid command: {}'.format(command))
    except Exception as err:
        _warder.ward_error('etl', err)
