#!/usr/bin/env python

import abc
import ftplib
import pymssql
import os
import access as acc

raw_dir_path = '{}/weaver/etl/raw/'.format(os.path.expanduser('~'))


class Extractor(metaclass=abc.ABCMeta):
    def __init__(self, access: acc.Access, output_path: str):
        """
        Everything any extractor needs to know
        :param access: Any credential and address necessary to extract
        :param output_path: a output path to extract to. WARNING: each child should under their criteria this value
        """
        self.access = access
        self.output_path = output_path

    @abc.abstractmethod
    def extract(self, to_file: bool):
        pass


class FtpExtractor(Extractor):
    def __init__(self, access: acc.Access, output_path: str, url: str):
        if not os.path.isdir(output_path):
            os.makedirs(output_path)
        super().__init__(access, output_path)
        self.url = url

    def extract(self, to_file: bool=False):
        """
        Extracts (downloads) file from ftp
        :return: the path to the downloaded file
        """
        try:
            with ftplib.FTP(self.access.address) as ftp:
                ftp.login(self.access.username, self.access.pwd)
                local_file_path = '{0}{1}'.format(self.output_path, self.url.split('/')[-1])
                if os.path.exists(local_file_path):
                    os.remove(local_file_path)
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
    def __init__(self, access: acc.Access, output_path: str, db: str, query: str):
        if os.path.exists(output_path) and os.path.isfile(output_path):
            os.remove(output_path)
        super().__init__(access, output_path)
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
        with open('{}{}/{}'.format(raw_dir_path, self.db, self.output_path), 'w') as result_file:
            for row in data:
                result_file.write('{}\n'.format('|'.join(row)))


class MultiSourceExtractor(Extractor):
    def __init__(self, single_extractor_list: tuple):
        super().__init__(access=acc.Access('', '', '', '', ''), output_path='')
        self.extractors_list = single_extractor_list

    def extract(self, to_file: bool):
        if len(self.extractors_list) < 1:
            raise IndexError('MultiSourceExtractor\'s extractor list is empty')
        results = []
        for extractor in self.extractors_list:
                results.append(extractor.extract(to_file=to_file))
        return results


# TODO code mssql query
def extract(target: str):
    """
    Extract data from sources based on the target declared
    :param target: the immediate destination of this data
    :return: 
    """
    def create_extractor(target: str):
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
            extractors = (SqlDataExtractor(acc.access_dict['ukvsqlbdrep01'],
                                           db='rt',
                                           query='select * vw_rt_vehicles_from_sscbr_cs2002'
                                                 ' order by e.vehicle_id, e.schema_id',
                                           output_path='sscbr_cs2002.txt'),
                          SqlDataExtractor(acc.access_dict['ukvsqlbdrep01'],
                                           db='rt',
                                           query='select * vw_rt_vehicles_from_sscbr_cs2002 '
                                                 'order by e.vehicle_id, e.schema_id',
                                           output_path='nscbr_cs2002.txt'))
            return MultiSourceExtractor(single_extractor_list=extractors)
        elif target == 'rt.incentives':
            return SqlDataExtractor(acc.access_dict['ukvsqlbdrep01'],
                                    db='rt',
                                    query='select * vw_rt_vehicles_from_escbr_cs2002_br_public_incentive'
                                          ' order by e.vehicle_id, e.schema_id',
                                    output_path='escbr_cs2002.txt')

    extractor = create_extractor(target)
    return extractor.extract(to_file=True)
