#!/usr/bin/env python3


import re
from ETL.Extract.CS_2002 import ents as cs_2002_ents


class VehicleEntity(cs_2002_ents.AssembledEntity):
    vehicle_id = 0
    uid = 0
    data_date = 0
    version_state = ''
    outgoing = False
    make = ''
    model = ''
    version = ''
    production_year = 0
    model_year = 0
    trim_level = ''
    number_of_doors = 0
    body_type = ''
    fuel_type = ''
    other_fuel_type = ''
    transmission_description = ''
    driven_wheels = ''
    liters = 0.0
    msrp = 0.0

    version_regex = re.compile(r'^([(])(O|!|\+|0)([)])')

    def __init__(self):
        super(cs_2002_ents.AssembledEntity, self).__init__()

    def __str__(self):
        return '|'.join([str(self.vehicle_id), str(self.uid), str(self.data_date), str(self.version_state),
                         str(self.make), str(self.model), str(self.version), '1' if self.outgoing else '0',
                         str(self.production_year), str(self.model_year), str(self.trim_level),
                         str(self.number_of_doors), str(self.body_type), str(self.fuel_type), str(self.other_fuel_type),
                         str(self.transmission_description), str(self.driven_wheels), str(self.liters), str(self.msrp)])

    def assembly(self, raw_ents):
        super().assembly(raw_ents)

    def _compose(self, current, new):
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

    def _decode_raw_ent(self, raw):
        """
        Decodes schema_id from rawEntity and assigns its data_value to the right SpecsEntity attribute
        Raises NotImplementedError with schema_id is not coded
        :param raw: raw from extraction of SCBR
        :return: 
        """
        self.vehicle_id = raw.vehicle_id
        if raw.schema_id == '101':
            self.uid = raw.data_value
        elif raw.schema_id == '104':
            self.data_date = raw.data_value
        elif raw.schema_id == '105':
            self.version_state = self._compose(current=self.version_state,
                                               new=cs_2002_ents.dict_version_state[raw.data_value])
            if raw.data_value == 'G':  # outgoing flag
                self.outgoing = True
        elif raw.schema_id == '111':
            self.make = raw.data_value
        elif raw.schema_id == '112':
            self.model = raw.data_value
        elif raw.schema_id == '302':
            self.version = self.version_regex.sub('', raw.data_value)
        elif raw.schema_id == '57108':
            self.production_year = raw.data_value
        elif raw.schema_id == '108':
            self.model_year = raw.data_value
        elif raw.schema_id == '402':
            self.trim_level = raw.data_value
        elif raw.schema_id == '602':
            self.number_of_doors = raw.data_value
        elif raw.schema_id == '603':
            self.body_type = cs_2002_ents.dict_body_type[raw.data_value]
        elif raw.schema_id == '8702':
            self.fuel_type = cs_2002_ents.dict_fuel_type[raw.data_value]
        elif raw.schema_id == '8703':
            self.other_fuel_type = cs_2002_ents.dict_fuel_type[raw.data_value]
        elif raw.schema_id == '20624':
            self.transmission_description = self._compose(current=self.transmission_description,
                                                          new=cs_2002_ents.dict_transmission_type[raw.data_value])
        elif raw.schema_id == '6502':
            self.driven_wheels = cs_2002_ents.dict_driven_wheels[raw.data_value]
        elif raw.schema_id == '7403':
            self.liters = raw.data_value
        elif raw.schema_id == '902':
            self.msrp = raw.data_value
        else:
            raise NotImplementedError('schema_id ' + raw.schema_id + ' is not implemented')
