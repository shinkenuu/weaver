
import abc
import ftplib
import pymssql
import os
import access as acc

EXTRACTED_DIR_PATH = '/mnt/jatobrfiles/Weaver/etl/extracted/'


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
    def extract(self):
        pass


class FtpExtractor(Extractor):
    def __init__(self, access: acc.Access, output_path: str, url: str):
        if not os.path.isdir(output_path):
            os.makedirs(output_path)
        super().__init__(access, output_path)
        self.url = url

    def extract(self):
        """
        Extracts (downloads) file from ftp
        :return: the path to the downloaded file
        """
        with ftplib.FTP(self.access.address) as ftp:
            ftp.login(self.access.username, self.access.pwd)
            local_file_path = '{0}{1}'.format(self.output_path, self.url.split('/')[-1])
            if os.path.exists(local_file_path):
                os.remove(local_file_path)
            with open(local_file_path, 'wb') as downloading_file:
                ftp.retrbinary('RETR {}'.format(self._get_file_path_since_root()), downloading_file.write)
            return local_file_path

    def _get_file_path_since_root(self):
        url = self.url
        if url.startswith('ftp://'):
            url = url.strip('ftp://')
        return url.replace(url.split('/')[0], '')


class SqlDataExtractor(Extractor):
    def __init__(self, access: acc.Access, output_path: str, db: str, query: str):
        if os.path.exists(output_path) and os.path.isfile(output_path):
            os.remove(output_path)
        else:
            os.makedirs(output_path.replace(os.path.basename(output_path), ''), exist_ok=True)
        super().__init__(access, output_path)
        self.db = db
        self.query = query

    def extract(self):
        """
        Query database extracting results
        :return: the extracted results
        """
        # specifying charset param in pymssql.connect() raises an unknown error
        with pymssql.connect(self.access.address, self.access.username, self.access.pwd, self.db) as conn:
            with conn.cursor() as cursor:
                cursor.execute(self.query)
                results = cursor.fetchall()
        self._write_to_file(results)
        return results

    def _write_to_file(self, query_results: tuple):
        with open(self.output_path, 'w') as result_file:
            for row in query_results:
                result_file.write('{}{}'.format('|'.join(str(col) for col in row), '\n'))
        return self.output_path


class MultiSourceExtractor(Extractor):
    def __init__(self, single_extractor_list: tuple):
        super().__init__(access=acc.Access('', '', '', '', ''), output_path='')
        self.extractors_list = single_extractor_list

    def extract(self):
        """
        Loop through each source, extracting 
        :return: the extracted results
        """
        if len(self.extractors_list) < 1:
            raise IndexError('MultiSourceExtractor\'s extractor list is empty')
        results = []
        for extractor in self.extractors_list:
                results.append(extractor.extract())
        return results


def extract(target: str, source: str):
    """
    Extract data from source
    :param target: the immediate data destination
    :param source: the source from which to extract data from
    :return: 
    """
    def create_extractor():
        if target == 'rt.vehicles':
            if source == 'mssql':
                extractors = (SqlDataExtractor(acc.access_dict['ukvsqlbdrep01'],
                                               db='rt',
                                               query='select * from vw_rt_vehicles_from_sscbr_cs2002'
                                                     ' order by vehicle_id',
                                               output_path='{}mssql/sscbr_cs2002.txt'.format(EXTRACTED_DIR_PATH)),
                              SqlDataExtractor(acc.access_dict['ukvsqlbdrep01'],
                                               db='rt',
                                               query='select * from vw_rt_vehicles_from_nscbr_cs2002'
                                                     ' order by vehicle_id',
                                               output_path='{}mssql/nscbr_cs2002.txt'.format(EXTRACTED_DIR_PATH)))
            elif source == 'msaccess':
                raise NotImplementedError('extraction of specs from msaccess')
            else:
                raise ValueError('{} is not a valid rt.vehicles source'.format(source))
            return MultiSourceExtractor(single_extractor_list=extractors)
        elif target == 'rt.incentives':
            if source == 'mssql':
                return SqlDataExtractor(acc.access_dict['ukvsqlbdrep01'],
                                        db='rt',
                                        query='select * from vw_rt_incentives_from_escbr_cs2002_br_public_incentive'
                                              ' order by vehicle_id, option_id',
                                        output_path='{}mssql/escbr_cs2002_br_public_incentive.txt'.format(
                                            EXTRACTED_DIR_PATH))
            elif source == 'msaccess':
                raise NotImplementedError('extraction of incentives from msaccess')
            else:
                raise ValueError('{} is not a valid rt.incentives source'.format(source))
        elif source == 'ftp':
            if target == 'ukvsqlbdrep01.sscbr_cs2002':
                return FtpExtractor(acc.access_dict['jatoftp2'],
                                    'ftp://ftp2.carspecs.jato.com/CURRENT/DATABASES/SQLSERVER/SSCBR/'
                                    'SSCBR_CS2002_SQL.EXE',
                                    '{}ftp/'.format(EXTRACTED_DIR_PATH))
            elif target == 'ukvsqlbdrep01.nscbr_cs2002':
                return FtpExtractor(acc.access_dict['jatoftp2'],
                                    'ftp://ftp2.carspecs.jato.com/CURRENT/DATABASES/SQLSERVER/NSCBR/'
                                    'NSCBR_CS2002_SQL.EXE',
                                    '{}ftp/'.format(EXTRACTED_DIR_PATH))
            elif target == 'ukvsqlbdrep01.escbr_cs2002_br_public_incentive':
                return FtpExtractor(acc.access_dict['jatoftp2'],
                                    'ftp://ftp2.carspecs.jato.com/CUSTOMEREMBARGO/Current/Databases/SQLSERVER/SSCBR/'
                                    'Incentive_Public_BR/SSCBR_CS2002_SQL.EXE',
                                    '{}ftp/'.format(EXTRACTED_DIR_PATH))
        else:
            raise ValueError('{0} is not a valid source for {1} target'.format(source, target))

    extractor = create_extractor()
    return extractor.extract()
