#!/usr/bin/env python3

from ETL.Extract.CS_2002 import ents as cs_2002_ents
from ETL.Extract.MsAccess import ents as ms_access_ents
from ETL.Transform.Vehicles import ent as vehicles_ent
from ETL.Transform.PublicIncentives import ent as incentives_ent
from ETL.Transform.TP import ent as tp_ent
import copy


class Transformer:
    _transformed_ents = []

    def __init__(self):
        pass

    def transform(self, into, raw_data_files, transformed_data_file):
        """
        Transforms raw entities from files into final ents in the file read to bulk insert
        :param into: The final entity in which the transform must lead raw entities in 'input_files' to 
        :param raw_data_files: The files with raw entities to be transformed
        :param transformed_data_file: The file to store the transformed entities (read to bulk insert)
        :return: 
        """
        if into == 'rt.vehicles' or into == 'rt.incentives':
            self._transform_from_cs_2002(str.replace(into, 'rt.', ''), raw_data_files)
        elif into == 'rt.tp':
            self._transform_rt_tp(raw_data_files)
        else:
            raise NotImplementedError(into + ' is not implemented. Use format [database].[table]')
        self._write_transformed_data_to_disc(transformed_data_file)

    def _write_transformed_data_to_disc(self, output_path):
        output = open(output_path, 'w')
        output.truncate()
        doc = ''
        for entity in self._transformed_ents:
            doc += str(entity) + '\n'
        output.write(doc)

    def _transform_from_cs_2002(self, into, input_files):
        """
        Transforms data from 'input_files' into the format ready for bulk insert
        :param into: Which database and table to format to
        :param input_files: the file containing the raw entities
        :return: 
        """
        into_ent = None
        if into == 'vehicles':
            into_ent = vehicles_ent.VehicleEntity()
        elif into == 'incentives':
            into_ent = incentives_ent.IncentiveEntity()
        else:
            raise NotImplementedError(into)
        raw_ents = []
        for input_file in input_files:
            with open(input_file, 'r+') as file:
                for line in file:
                    raw_ent = cs_2002_ents.RawEntity()
                    raw_ent.from_line(line)
                    # if raw_ent is the first one of this file OR if this raw_ent has belongs to the
                    if len(raw_ents) == 0 or raw_ents[0].vehicle_id == raw_ent.vehicle_id:
                        raw_ents.append(raw_ent)
                    else:
                        transformed_ent = copy.copy(into_ent)
                        transformed_ent.assembly(raw_ents)
                        self._transformed_ents.append(transformed_ent)
                        raw_ents.clear()
                        raw_ents.append(raw_ent)

    def _transform_rt_tp(self, input_files):
        into_ent = tp_ent.TpEntity()
        raw_ents = []
        for input_file in input_files:
            with open(input_file, 'r+') as file:
                for line in file:
                    raw_ent = ms_access_ents.RawEntity()
                    raw_ent.from_line(line)
                    # if raw_ent is the first one of this file OR if this raw_ent has belongs to the
                    if len(raw_ents) == 0 or \
                            (raw_ents[0].uid == raw_ent.uid and raw_ents[0].data_date == raw_ent.data_date):
                        raw_ents.append(raw_ent)
                    else:
                        transformed_ent = copy.copy(into_ent)
                        transformed_ent.assembly(raw_ents)
                        self._transformed_ents.append(transformed_ent)
                        raw_ents.clear()
                        raw_ents.append(raw_ent)
