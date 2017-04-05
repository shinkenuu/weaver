#!/usr/bin/python3

import os
import sys
from ETL.Transform import transformer


def etl(action, raw_data_file_names, transformed_data_file_name, target=None):
    """
        Extracts, Transforms or Loads data from a source to a destiny
    :param action: [x|t|l] eXtract, Transform, Load
    :param raw_data_file_names: iterable with raw data file names
    :param transformed_data_file_name:
    :param transform_into: destiny in the [database.table] format
    :return: 
    """
    raw_data_file_names = raw_data_file_names.split(',')

    #Verify input files existence
    for file_name in raw_data_file_names:
        if not os.path.isfile(file_name):
            raise FileNotFoundError(file_name)

    if (action == 'x'):
        raise NotImplementedError('Extraction')
    elif (action == '-t'):
        transformer.transform(
            into=target,
            raw_data_file_names=raw_data_file_names,
            transformed_data_file_name=transformed_data_file_name)
    elif (action == '-l'):
        raise NotImplementedError('Load')


def main():
    """
        NAME
            ETL

        SYNOPSIS
            etl.py [OPTIONS] [INPUT FILE NAME[,INPUT FILE NAME]] [OUTPUT FILE NAME] [TARGET]

        OPTIONS
            <b>-x</b> eXtract
            <b>-t</b> Transform
            <b>-l</b> Load

        TARGET
            [<b>database</b>.<b>table</b>]
        """
    etl(sys.argv[2], sys.argv[3], sys.argv[4], target=sys.argv[5])



if __name__ == '__main__':
    main()
