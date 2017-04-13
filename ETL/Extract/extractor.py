#!/usr/bin/env python

import ftplib
import pymssql
import os
import access as acc


class ExtractionSource:
    def __init__(self, protocol: str, access: acc.Access, full_path: str=None, db: str=None, table: str=None):
        self.protocol = protocol
        self.access = access
        if full_path:
            self.full_path = full_path
        if db:
            self.db = db
        if table:
            self.table = table


target_extration_sources_dict = {
    'sscbr_cs2002': ExtractionSource('ftp', acc.access_dict['jatoftp2'],
                                     'ftp2.carspecs.jato.com/CURRENT/DATABASES/SQLSERVER/SSCBR/SSCBR_CS2002_SQL.EXE'),
    'nscbr_cs2002': ExtractionSource('ftp', acc.access_dict['jatoftp2'],
                                     'ftp2.carspecs.jato.com/CURRENT/DATABASES/SQLSERVER/NSCBR/NSCBR_CS2002_SQL.EXE'),
    'escbr_cs2002': ExtractionSource('ftp', acc.access_dict['jatoftp2'],
                                     'ftp2.carspecs.jato.com/CUSTOMEREMBARGO/Current/Databases/SQLSERVER/SSCBR/'
                                     'Incentive_Public_BR/SSCBR_CS2002_SQL.EXE'),
    'rt.vehicles': ExtractionSource('mssql', acc.access_dict['ukvsqlbdrep01'], db='vehicles'),
    'rt.incentives': ExtractionSource('mssql', acc.access_dict['ukvsqlbdrep01'], db='incentives'),
    'rt.tp': ExtractionSource('mssql', acc.access_dict['ukvsqlbdrep01'], db='tp')
}


def download_from_ftp(address: str, username: str, pwd: str, file_path: str, output_dir: str):
    """
    Download files from ftp
    :param address:
    :param username: 
    :param pwd: 
    :param file_path: 
    :param output_dir: 
    :return: 
    """
    try:
        with ftplib.FTP(address) as ftp:
            ftp.login(username, pwd)
            with open('{0}{1}'.format(output_dir, file_path.split('/')[-1]), 'wb') as downloading_file:
                ftp.retrbinary('RETR {}'.format(file_path).replace(address, ''), downloading_file.write)
    except Exception as ex:
        raise ex


# TODO test
def query_mssql(address: str, username: str, pwd: str, db: str, query: str):
    """
    Query SQL Server and return the results
    :param address: SQL Server host address
    :param username: login username 
    :param pwd: login password
    :param db: which database to run the query on
    :param query: the query that retrieves the data
    :return: the queried results
    """
    with pymssql.connect(address, username, pwd, db, charset='utf-8') as conn:
        with conn.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall()


# TODO code mssql query
def extract(target: str, output_dir: str):
    """
    Extract data from sources based on the target declared
    :param target: the immediate destination of this data
    :param output_dir: where should it be stored
    :return: 
    """
    ext_src = target_extration_sources_dict[target]
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
    if ext_src.protocol == 'ftp':
            download_from_ftp(address=ext_src.access.address,
                              username=ext_src.access.username,
                              pwd=ext_src.access.pwd,
                              file_path=ext_src.full_path,
                              output_dir=output_dir)
    elif ext_src.protocol == 'mssql':
            query_mssql(address=ext_src.access.address,
                        username=ext_src.access.username,
                        pwd=ext_src.access.pwd,
                        db=ext_src.db,
                        query='code_me')
