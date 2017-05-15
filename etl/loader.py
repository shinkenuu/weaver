
import access
import os
import pymssql
import shutil

BLKINS_PATHS = {
    'rt': '/mnt/ukvsqlbdrep01/RT/'
}

def _convert_to_srv_path(path: str):
    return path.replace('/mnt/ukvsqlbdrep01', 'D:').replace('/', '\\')

def bulk_insert(db: str, table: str, local_file_path: str):
    file_name = os.path.basename(local_file_path)
    remote_file_path = '{}data/{}'.format(BLKINS_PATHS[db], file_name)
    shutil.copy(local_file_path, remote_file_path)
    sql_access = access.access_dict['ukvsqlbdrep01']
    with pymssql.connect(sql_access.address, sql_access.username, sql_access.pwd, db) as conn:
        with conn.cursor() as cursor:
            return cursor.callproc('blkInsert{}'.format(str.upper(table)),
                                   (_convert_to_srv_path(remote_file_path), ))

def load(into: str, source: str):
    db, table = into.split('.')
    result = bulk_insert(db=db, table=table, local_file_path=source)
    return result
