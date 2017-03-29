#!/usr/bin/env python3

import os
import sys
from SCBR import scbr
from SCBR import sscbr
from SCBR import escbr
from SCBR import nscbr


def _write_to_disc(output_path, entities):
    output = open(output_path, 'w')
    output.truncate()
    doc = ''
    for entity in entities:
        doc += str(entity) + '\n'
    output.write(doc)


def transform_scbr(scbr_type, input_file, output_file):
    if scbr_type == 'sscbr':
        entity_type = sscbr.SscbrEntity()
    elif scbr_type == 'nscbr':
        entity_type = nscbr.NscbrEntity()
    elif scbr_type == 'escbr':
        entity_type = escbr.EscbrEntity()
    else:
        raise ValueError("Invalid scbr_type" + scbr_type + ". Please refer to help()")

    entities = []
    results = []

    with open(input_file, 'r+') as file:
        for line in file:
            result = scbr.ExtractedResult()
            result.from_line(line)
            if len(results) == 0 or results[0].vehicle_id == result.vehicle_id:
                results.append(result)
            else:
                entities.append(entity_type.assembly(results))
                results.clear()
                results.append(result)

    _write_to_disc(output_file, entities)


def main():
    """
    NAME
        SCBR etl

    SYNOPSIS
        etl [OPTIONS] [INPUT FILE NAME] [OUTPUT FILE NAME]

    OPTIONS
        <b>sscbr</b> stands for Cars
        <b>nscbr</b> stands for Light Commercials
        <b>escbr</b> stand for Public Incentives

    :return:
    """
    if len(sys.argv) != 4:
        raise ValueError("Insufficient parameters. Please refer to help()")
    elif not os.path.isfile(sys.argv[2]):
        raise FileExistsError(sys.argv[2])
    # elif not os.path.isfile(sys.argv[3]):
    #     raise FileExistsError(sys.argv[3])

    transform_scbr(input_file=sys.argv[2], output_file=sys.argv[3])


if __name__ == '__main__':
    main()
