#!/usr/bin/env python3

import sys
from ETL.Transform import transformer


def main():
    """
    NAME
        ETL

    SYNOPSIS
        etl.py [OPTIONS] [DATABASE] [INPUT FILE NAME] [OUTPUT FILE NAME]

    OPTIONS
        <b>-x</b> eXtract
        <b>-t</b> Transform
        <b>-l</b> Load
    
    DATABASE
        <b>--sscbr</b> stands for Cars
        <b>--nscbr</b> stands for Light Commercials
        <b>--escbr</b> stand for Public Incentives

    """

    if(sys.argv.__len__() < 6):
        print("Insufficient parameters")
        return -1

    if (sys.argv[2] == '-x'):
        raise NotImplementedError()
    elif (sys.argv[2] == '-t'):
        septimus = transformer.Transformer()
        septimus.transform(
            into=str(sys.argv[3]), raw_data_files=str.split(sys.argv[4], ','), transformed_data_file=sys.argv[5])
    elif (sys.argv[2] == '-l'):
        raise NotImplementedError()


if __name__ == '__main__':
    main()
