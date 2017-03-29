#!/usr/bin/env python3


from . import scbr


class SscbrEntity(scbr.Entity):
    vehicle_id = 0
    uid = 0
    data_date = 0
    version_state = ''  # code, composed
    make = ''
    model = ''
    version = ''
    production_year = 0
    model_year = 0
    trim_level = ''
    number_of_doors = 0
    body_type = ''  # code
    fuel_type = ''  # code
    other_fuel_type = ''  # code
    transmission_description = ''  # code, composed
    driven_wheels = ''  # code
    liters = 0.0
    msrp = 0.0

    def __init__(self):
        pass

    def __str__(self):
        return '|'.join([str(self.vehicle_id), str(self.uid), str(self.data_date), str(self.version_state),
                         str(self.make), str(self.model), str(self.version), str(self.production_year),
                         str(self.model_year), str(self.trim_level), str(self.number_of_doors), str(self.body_type),
                         str(self.fuel_type), str(self.other_fuel_type), str(self.transmission_description),
                         str(self.driven_wheels), str(self.liters), str(self.msrp)])

    def _compose_version_state(self, result):
        if self.version_state == '':
            self.version_state = result.data_value
        else:
            self.version_state += ',' + result.data_value

    def _compose_transmission_description(self, result):
        if self.transmission_description == '':
            self.transmission_description = result.data_value
        else:
            self.transmission_description += ',' + result.data_value

    def _decode_result(self, result):
        self.vehicle_id = result.vehicle_id
        if result.schema_id == '101':
            self.uid = result.data_value
        elif result.schema_id == '104':
            self.data_date = result.data_value
        elif result.schema_id == '105':
            self._compose_version_state(result.data_value)
        elif result.schema_id == '111':
            self.make = result.data_value
        elif result.schema_id == '112':
            self.model = result.data_value
        elif result.schema_id == '302':
            self.version = result.data_value
        elif result.schema_id == '57108':
            self.production_year = result.data_value
        elif result.schema_id == '108':
            self.model_year = result.data_value
        elif result.schema_id == '402':
            self.trim_level = result.data_value
        elif result.schema_id == '602':
            self.number_of_doors = result.data_value
        elif result.schema_id == '603':
            self.body_type = result.data_value
        if result.schema_id == '8702':
            self.fuel_type = result.data_value
        if result.schema_id == '8703':
            self.other_fuel_type = result.data_value
        if result.schema_id == '20624':
            self._compose_transmission_description(result.data_value)
        if result.schema_id == '6502':
            self.driven_wheels = result.data_value
        if result.schema_id == '7403':
            self.liters = result.data_value
        if result.schema_id == '902':
            self.msrp = result.data_value
        else:
            raise NotImplementedError('schema_id ' + result.schema_id + ' is not implemented')

