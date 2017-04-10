#!/usr/bin/env python

import os
from ETL import etl


def transform(into_ent_type : type, raw_data_file_names : str):
    """
    Transforms raw entities from files into final ents in the file read to bulk insert
    :param into: The final entity in which the transform must lead raw entities in 'input_files' to. 
    Usage: database.table
    :param raw_data_file_names: The file names with raw entities to be transformed
    :param transformed_data_file_name: The file name to store the transformed entities (read to bulk insert)
    :return: 
    """
    transformed_ents = []
    for raw_file in raw_data_file_names:
        raw_ent_type = type(etl.raw_ent_types_dict[os.path.basename(raw_file).lower()])
        with open(raw_file, 'r+') as file:
            all_lines = file.read().split('\n')
        all_lines.sort()
        raw_ents = []
        for line in all_lines:
            raw_ent = raw_ent_type(line)
            # if there is no raw_ent to compare yet OR if this raw_ent belongs with the current list of raw_ents
            if len(raw_ents) == 0 or raw_ents[0].belongs_with(raw_ent):
                raw_ents.append(raw_ent)
            else:
                transformed_ent = into_ent_type(raw_ents)
                transformed_ents.append(transformed_ent)
                raw_ents.clear()
                raw_ents.append(raw_ent)
        _write_ents_to_disc(transformed_ents, etl.dirs_dict['into'])


def _write_ents_to_disc(ents, output_path):
    output = open(output_path, 'w')
    output.truncate()
    doc = ''
    for ent in ents:
        doc += str(ent) + '\n'
    output.write(doc)
