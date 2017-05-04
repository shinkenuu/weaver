#!/usr/bin/env python

from etl import extractor
from . import raw_ents
from . import rt_ents

transformed_dir_path = '/mnt/jatobrfiles/Weaver/etl/transformed/'

transformed_ent_types_dict = {
    'rt.vehicles': rt_ents.VehicleEntity,
    'rt.incentives': rt_ents.IncentiveEntity,
    'rt.tp': rt_ents.TpEntity
}

raw_ent_types_dict = {
    'mssql|rt.vehicles': raw_ents.Cs2002Entity,
    'mssql|rt.incentives': raw_ents.EscbrBrPublicIncentiveEntity,
    'msaccess|rt.incentives': raw_ents.CsRtIncentivesEntity,
    'msaccess|rt.tp': raw_ents.CsRtTpCompletaEntity
}

necessary_files_dict = {
    'mssql|rt.vehicles': ('sscbr_cs2002.txt', 'nscbr_cs2002.txt'),
    'mssql|rt.incentives': ('escbr_cs2002_br_public_incentive.txt', ),
    'msaccess|rt.incentives': ('CS_RT_INCENTIVES.txt', ),
    'msaccess|rt.tp': ('CS_RT_TP_COMPLETA.txt', )
}


def _transform_from_file(file_path: str, into_raw_type: type):
    ents = []
    with open(file_path, 'r') as file:
        for line in file:
            raw_ent = into_raw_type(raw_data=line)
            ents.append(raw_ent)
    return ents


def _transform_from_iterable(extracted_data: list, into_raw_type: type):
    ents = []
    for data in extracted_data:
        raw_ent = into_raw_type(raw_data=data)
        ents.append(raw_ent)
    return ents


def _transform_from_raw(raw_ent_array: list, into_type: type):
    transformed_ents = []
    ents_to_assemble = []
    for raw_ent in raw_ent_array:
        # if there is no raw_ent to compare yet OR if this raw_ent belongs with the current list of raw_ents
        if len(ents_to_assemble) == 0 or ents_to_assemble[0].belongs_with(raw_ent):
            ents_to_assemble.append(raw_ent)
        else:
            transformed_ent = into_type(ents_to_assemble)
            transformed_ents.append(transformed_ent)
            ents_to_assemble.clear()
            ents_to_assemble.append(raw_ent)
    return transformed_ents


def transform(into: str, source: str, input_data: list):
    """
    Transforms raw entities from files into final ents in the file read to bulk insert
    :param into: The final entity. Usage: database.table
    :param source: The data source
    :param input_data: file path or tuple with extracted data
    :return: 
    """
    key = '{0}|{1}'.format(source, into)
    if input_data:
        input_data = _transform_from_iterable(extracted_data=input_data, into_raw_type=raw_ent_types_dict[into])
    else:
        input_data = []
        for necessary_file in necessary_files_dict[key]:
                input_data.extend(_transform_from_file(
                    file_path='{0}{1}/{2}'.format(extractor.extracted_dir_path, source, necessary_file),
                    into_raw_type=raw_ent_types_dict[key]))
    input_data = _transform_from_raw(input_data, into_type=transformed_ent_types_dict[into])
    _write_ents_to_disc(input_data, '{0}{1}.txt'.format(transformed_dir_path, into))


def _write_ents_to_disc(ents, output_path: str):
    output = open(output_path, 'w')
    output.truncate()
    doc = ''
    for ent in ents:
        doc += str(ent) + '\n'
    output.write(doc)
