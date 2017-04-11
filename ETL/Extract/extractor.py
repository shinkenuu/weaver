#!/usr/bin/env python

import ftplib
import pymssql
import credentials as creds


class ExtractionSource:
    def __init__(self, protocol: str, credential: creds.Credential, full_path: str=None, db: str=None):
        self.protocol = protocol
        self.credential = credential
        if full_path:
            self.full_path = full_path
        if db:
            self.db = db


target_extration_sources_dict = {
    'sscbr_cs2002': ExtractionSource('ftp', creds.credentials_dict['jatoftp2'],
                                     'ftp2.carspecs.jato.com/CURRENT/DATABASES/SQLSERVER/SSCBR/SSCBR_CS2002_SQL.EXE'),
    'nscbr_cs2002': ExtractionSource('ftp', creds.credentials_dict['jatoftp2'],
                                     'ftp2.carspecs.jato.com/CURRENT/DATABASES/SQLSERVER/NSCBR/NSCBR_CS2002_SQL.EXE'),
    'escbr_cs2002': ExtractionSource('ftp', creds.credentials_dict['jatoftp2'],
                                     'ftp2.carspecs.jato.com/CUSTOMEREMBARGO/Current/Databases/SQLSERVER/SSCBR/'
                                     'Incentive_Public_BR/SSCBR_CS2002_SQL.EXE'),
    'rt.vehicles': ExtractionSource('mssql', creds.credentials_dict['ukvsqlbdrep01'], db='vehicles'),
    'rt.incentives': ExtractionSource('mssql', creds.credentials_dict['ukvsqlbdrep01'], db='incentives'),
    'rt.tp': ExtractionSource('mssql', creds.credentials_dict['ukvsqlbdrep01'], db='tp')
}


# TODO test
def download_from_ftp(address: str, port: int, username: str, pwd: str, file_path: str, output_path: str):
    with ftplib.FTP('{0}:{1}'.format(address, str(port))) as ftp:
        ftp.login(username, pwd)
        with open(output_path, 'wb') as downloading_file:
            ftp.retrbinary('RETR {}'.format(file_path), downloading_file.write)


# TODO test
def query_mssql(address: str, username: str, pwd: str, db: str, query: str):
    with pymssql.connect(address, username, pwd, db, charset='utf-8') as conn:
        with conn.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall()


# TODO code mssql query
def extract(target: str, output_path: str):
    ext_src = target_extration_sources_dict[target]
    if ext_src.protocol == 'ftp':
        with ext_src.credential as cred:
            download_from_ftp(cred.address, cred.port, cred.username, cred.pwd, ext_src.full_path, output_path)
    elif ext_src.protocol == 'mssql':
        with ext_src.credential as cred:
            query_mssql(cred.address, cred.username, cred.pwd, ext_src.db, 'code_me')
