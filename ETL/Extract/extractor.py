#!/usr/bin/env python

import abc
import ftplib
import pymssql
import os
import access as acc

raw_dir_path = '{}/weaver/etl/raw/'.format(os.path.expanduser('~'))


class Extractor:
    __metaclass__ = abc.ABCMeta

    def __init__(self, access: acc.Access):
        self.access = access

    @abc.abstractmethod
    def extract(self, to_file: bool):
        pass


class FtpExtractor(Extractor):
    def __init__(self, access: acc.Access, url: str, output_dir: str):
        super().__init__(access)
        self.url = url
        if not os.path.isdir(output_dir):
            os.makedirs(output_dir)
        self.output_dir = output_dir

    def extract(self, to_file: bool=False):
        """
        Extracts (downloads) file from ftp
        :return: the path to the downloaded file
        """
        try:
            with ftplib.FTP(self.access.address) as ftp:
                ftp.login(self.access.username, self.access.pwd)
                local_file_path = '{0}{1}'.format(self.output_dir, self.url.split('/')[-1])
                with open(local_file_path, 'wb') as downloading_file:
                    ftp.retrbinary('RETR {}'.format(self._get_file_path_since_root()), downloading_file.write)
                return local_file_path
        except Exception as ex:
            raise ex

    def _get_file_path_since_root(self):
        url = self.url
        if url.startswith('ftp://'):
            url = url.strip('ftp://')
        return url.replace(url.split('/')[0], '')

# TODO test
class SqlDataExtractor(Extractor):
    def __init__(self, access: acc.Access, db: str, query: str):
        super().__init__(access)
        self.db = db
        self.query = query

    def extract(self, to_file: bool):
        try:
            with pymssql.connect(self.access.address, self.access.username, self.access.pwd, self.db,
                                 charset='utf-8') as conn:
                with conn.cursor() as cursor:
                    cursor.execute(self.query)
                    if to_file:
                        self._write_to_file(cursor.fetchall())
                    else:
                        return cursor.fetchall()
        except Exception as ex:
            raise ex

    def _write_to_file(self, data: tuple):
        with open(self.sql_file_name, 'w') as result_file:
            for row in data:
                result_file.write('{}\n'.format('|'.join(row)))


def _create_extractor(target: str):
    if target == 'sscbr_cs2002':
        return FtpExtractor(acc.access_dict['jatoftp2'],
                            'ftp://ftp2.carspecs.jato.com/CURRENT/DATABASES/SQLSERVER/SSCBR/SSCBR_CS2002_SQL.EXE',
                            '{}sscbr_cs2002/'.format(raw_dir_path))
    elif target == 'nscbr_cs2002':
        return FtpExtractor(acc.access_dict['jatoftp2'],
                            'ftp://ftp2.carspecs.jato.com/CURRENT/DATABASES/SQLSERVER/NSCBR/NSCBR_CS2002_SQL.EXE',
                            '{}nscbr_cs2002/'.format(raw_dir_path))
    elif target == 'escbr_cs2002':
        return FtpExtractor(acc.access_dict['jatoftp2'],
                            'ftp://ftp2.carspecs.jato.com/CUSTOMEREMBARGO/Current/Databases/SQLSERVER/SSCBR/'
                            'Incentive_Public_BR/SSCBR_CS2002_SQL.EXE',
                            '{}escbr_cs2002/'.format(raw_dir_path))
    elif target == 'rt.vehicles':
        return SqlDataExtractor(acc.access_dict['ukvsqlbdrep01'], db='rt', query_sql_file_path='sscbr_cs2002')
    elif target == 'rt.incentives':
        return SqlDataExtractor(acc.access_dict['ukvsqlbdrep01'], db='rt', query_sql_file_path='sscbr_cs2002')
    elif target == 'rt.tp':
        return SqlDataExtractor(acc.access_dict['ukvsqlbdrep01'], db='rt', query_sql_file_path='sscbr_cs2002')


# TODO code mssql query
def extract(target: str, chain: bool):
    """
    Extract data from sources based on the target declared
    :param target: the immediate destination of this data
    :return: 
    """
    extractor = _create_extractor(target)
    return extractor.extract(to_file=not chain)
