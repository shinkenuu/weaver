#!/usr/bin/env python

import os
from ETL.Extract.raw_ents import types_dict as raw_ent_types_dict
from .Rt import vehicle_ent, public_inc_ent, tp_ent

transformed_dir_path = '{}/weaver/etl/transformed/'.format(os.path.expanduser('~'))

transformed_ent_types_dict = {
    'rt.vehicles': vehicle_ent.VehicleEntity,
    'rt.incentives': public_inc_ent.IncentiveEntity,
    'rt.tp': tp_ent.TpEntity
}


# TODO recode the way the function find input files
def transform(into: str):
    """
    Transforms raw entities from files into final ents in the file read to bulk insert
    :param into: The final entity in which the transform must lead raw entities in 'input_files' to. 
    Usage: database.table
    :param raw_data_file_names: The file names with raw entities to be transformed
    :param transformed_data_file_name: The file name to store the transformed entities (read to bulk insert)
    :return: 
    """
    into_ent_type = transformed_ent_types_dict[into]
    transformed_ents = []
    for raw_file in raw_data_file_names:
        raw_ent_type = raw_ent_types_dict[os.path.basename(raw_file).lower()]
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
        _write_ents_to_disc(transformed_ents, '{0}{1}.txt'.format(output_dir, into.replace('.', '/')))


def _write_ents_to_disc(ents, output_path):
    output = open(output_path, 'w')
    output.truncate()
    doc = ''
    for ent in ents:
        doc += str(ent) + '\n'
    output.write(doc)
