import ftplib

# TODO test
def download_from_ftp(ipAddress : str, port : int, username :str, pwd : str, file_path : str, output_path : str):
    ftp = ftplib.FTP('{0}:{1}'.format(ipAddress, str(port)))
    ftp.login(username, pwd)
    try:
        with open(output_path, 'wb') as downloading_file:
            ftp.retrbinary('RETR {}'.format(file_path), downloading_file.write)
    except:
        pass
    finally:
        ftp.close()
        ftp.quit()
# TODO code
def extract(source, target):
    pass

