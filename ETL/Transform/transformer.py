#!/usr/bin/python3

import os
import traceback
import pigeon
from ETL.Extract import raw_ents
from ETL.Transform.Rt import tp_ent, public_inc_ent, vehicle_ent


raw_ents_dict = {
    'sscbr_cs_2002': raw_ents.Cs2002Entity(),
    'nsscbr_cs_2002': raw_ents.Cs2002Entity,
    'escbr_cs_2002': raw_ents.Cs2002Entity(),
    'cs_rt_tp_completa': raw_ents.MsAccessTpEntity(),
    'cs_rt_tp_toyota': raw_ents.MsAccessTpEntity()
}

into_ents_dict = {
    'rt.vehicles': vehicle_ent.VehicleEntity(),
    'rt.incentives': public_inc_ent.IncentiveEntity(),
    'rt.tp': tp_ent.TpEntity()
}


def transform(into, raw_data_file_names, transformed_data_file_name):
    """
    Transforms raw entities from files into final ents in the file read to bulk insert
    :param into: The final entity in which the transform must lead raw entities in 'input_files' to. 
    Usage: database.table
    :param raw_data_file_name_list: The file name list with raw entities to be transformed
    :param transformed_data_file_name: The file name to store the transformed entities (read to bulk insert)
    :return: 
    """
    try:
        into_ent_type = type(into_ents_dict[into])
        transformed_ents = []
        for raw_file in raw_data_file_names:
            raw_ent_type = type(raw_ents_dict[os.path.basename(raw_file)])
            with open(raw_file, 'r+') as file:
                all_lines = file.read().split('\n')
            all_lines.sort()
            raw_ents = []
            for line in all_lines:
                raw_ent = raw_ent_type(line)
                # if there is no raw_ent to compare yet OR if this raw_ent belongs to the current list of raw_ents
                if len(raw_ents) == 0 or raw_ents[0].compare(raw_ent):
                    raw_ents.append(raw_ent)
                else:
                    transformed_ent = into_ent_type(raw_ents)
                    transformed_ents.append(transformed_ent)
                    raw_ents.clear()
                    raw_ents.append(raw_ent)
            _write_ents_to_disc(transformed_ents, transformed_data_file_name)
    except Exception as ex:
        pigeon.alert_tower('{}\n{}'.format(traceback.extract_stack(), traceback.extract_tb(ex.__traceback__)))


def _write_ents_to_disc(ents, output_path):
    output = open(output_path, 'w')
    output.truncate()
    doc = ''
    for ent in ents:
        doc += str(ent) + '\n'
    output.write(doc)
