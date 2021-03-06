import credential
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
    sql_access = credential.get_credential(subject='ukvsqlbdrep01', owner='etl')
    with pymssql.connect(sql_access['address'], sql_access['username'], sql_access['password'], db) as conn:
        with conn.cursor() as cursor:
            cursor.callproc('blkInsert{}'.format(table),
                            (_convert_to_srv_path(remote_file_path), ))
        conn.commit()


def load(into: str, source: str):
    db, table = into.split('.')
    bulk_insert(db=db, table=table, local_file_path=source)
