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


def etl(command: str, input, target):
    try:
        if command == 'extract':
            extractor.extract()
        elif command == 'transform':
            transformer.transform(
                into=target,
                raw_data_file_names=input,
                output_dir=dirs_dict['transformed'])
        elif command == 'load':
            raise NotImplementedError('Loading module of ETL')
        else:
            raise NotImplementedError('Invalid command: {}'.format(command))
    except Exception as err:
        _warder.ward_error('etl', err)
