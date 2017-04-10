#!/usr/bin/env python

import re

from ETL.Extract import raw_ents as cs_2002_ent
from . import rt_ent

version_regex = re.compile(r'^([(])(O|!|\+|0)([)])')


def compose(current, new):
    """
    Compose multiple data_values into the same attribute(field) joining everything with ','
    :param current: the attribute(field) to be composed
    :param new: the new data_value part of it
    :return: the composed field
    """
    if current == '':
        return new
    else:
        return current + ',' + new


class VehicleEntity(rt_ent.RtEntity):
    def __init__(self, raw_ents=None):
        self.uid = 0
        self.data_date = 0  # yyyyMMdd
        self.version_state = ''
        self.outgoing = False
        self.make = ''
        self.model = ''
        self.version = ''
        self.production_year = 0
        self.model_year = 0
        self.trim_level = ''
        self.number_of_doors = 0
        self.body_type = ''
        self.fuel_type = ''
        self.other_fuel_type = ''
        self.transmission_description = ''
        self.driven_wheels = ''
        self.liters = 0.0
        self.msrp = 0.0
        super().__init__(raw_ents)

    def __str__(self):
        return '|'.join([str(self.vehicle_id), str(self.uid), str(self.data_date), str(self.version_state),
                         str(self.make), str(self.model), str(self.version), '1' if self.outgoing else '0',
                         str(self.production_year), str(self.model_year), str(self.trim_level),
                         str(self.number_of_doors), str(self.body_type), str(self.fuel_type), str(self.other_fuel_type),
                         str(self.transmission_description), str(self.driven_wheels), str(self.liters), str(self.msrp)])

    def _decode_raw_ent(self, raw_ent):
        """
        Decodes schema_id from raw_entEntity and assigns its data_value to the right SpecsEntity attribute
        Raises NotImplementedError with schema_id is not coded
        :param raw_ent: raw_ent from extraction of SCBR
        :return: 
        """
        self.vehicle_id = raw_ent.vehicle_id
        if raw_ent.schema_id == '101':
            self.uid = raw_ent.data_value
        elif raw_ent.schema_id == '104':
            self.data_date = raw_ent.data_value
        elif raw_ent.schema_id == '105':
            self.version_state = compose(current=self.version_state,
                                         new=cs_2002_ent.dict_version_state[raw_ent.data_value])
            if raw_ent.data_value == 'G':  # outgoing flag
                self.outgoing = True
        elif raw_ent.schema_id == '111':
            self.make = raw_ent.data_value
        elif raw_ent.schema_id == '112':
            self.model = raw_ent.data_value
        elif raw_ent.schema_id == '302':
            self.version = version_regex.sub('', raw_ent.data_value)
        elif raw_ent.schema_id == '57108':
            self.production_year = raw_ent.data_value
        elif raw_ent.schema_id == '108':
            self.model_year = raw_ent.data_value
        elif raw_ent.schema_id == '402':
            self.trim_level = raw_ent.data_value
        elif raw_ent.schema_id == '602':
            self.number_of_doors = raw_ent.data_value
        elif raw_ent.schema_id == '603':
            self.body_type = cs_2002_ent.dict_body_type[raw_ent.data_value]
        elif raw_ent.schema_id == '8702':
            self.fuel_type = cs_2002_ent.dict_fuel_type[raw_ent.data_value]
        elif raw_ent.schema_id == '8703':
            self.other_fuel_type = cs_2002_ent.dict_fuel_type[raw_ent.data_value]
        elif raw_ent.schema_id == '20624':
            self.transmission_description = compose(current=self.transmission_description,
                                                    new=cs_2002_ent.dict_transmission_type[raw_ent.data_value])
        elif raw_ent.schema_id == '6502':
            self.driven_wheels = cs_2002_ent.dict_driven_wheels[raw_ent.data_value]
        elif raw_ent.schema_id == '7403':
            self.liters = raw_ent.data_value
        elif raw_ent.schema_id == '902':
            self.msrp = raw_ent.data_value
        else:
            raise NotImplementedError('schema_id ' + raw_ent.schema_id + ' is not implemented')
