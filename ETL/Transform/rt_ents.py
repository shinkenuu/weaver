#!/usr/bin/env python

import abc
import re
from datetime import datetime

from ETL.Transform import raw_ents

version_state_dict = {
    '-': '',
    '?': '?',
    'A': 'estoque',
    'C': 'alteração de moeda',
    'D': 'Mudança de nome do modelo',
    'E': 'embargado',
    'F': 'novo visual',
    'G': 'descontinuada',
    'I': 'alteração de incentivo',
    'K': 'Mudança de nome de marca',
    'L': 'frota',
    'M': 'alteração ano modelo',
    'N': 'novo modelo',
    'O': 'alteração de opcionais',
    'P': 'alteração de preço',
    'R': 're-introdução',
    'S': 'alteração especificação',
    'T': 'alteração de impostos',
    'V': 'nova versão'
 }

body_type_dict = {
    '-': '',
    '?': '?',
    '3C': 'tricycle',
    '4C': 'quadricycle',
    'BH': 'chassis cabine',
    'BP': 'pick-up de cabine simples',
    'BT': 'plataforma com cabine',
    'BU': 'van de passageiros',
    'CA': 'conversível',
    'CC': 'veículo de uso misto',
    'CE': 'perua comercial',
    'CH': 'hatchback comercial',
    'CM': 'autocaravana',
    'CO': 'coupê',
    'CP': 'pick-up derivada de automóvel',
    'CR': 'Crossover',
    'CV': 'carro-furgão',
    'CX': 'somente chassis',
    'DH': 'chassis cabine dupla',
    'DP': 'pick-up de cabine dupla',
    'DS': 'abertura lateral',
    'ES': 'perua',
    'FW': 'MPV',
    'HA': 'hatchback',
    'MC': 'micro carro',
    'MM': 'Mini MPV',
    'MY': 'Motocicleta',
    'OC': 'fora de estrada comercial',
    'OD': 'SUV',
    'OM': 'ônibus',
    'PU': 'pick-up',
    'PV': 'furgão fechado',
    'RV': 'furgão montado em chassis cabine',
    'SA': 'sedan',
    'SH': 'sedan com teto reforçado - Japão',
    'TA': 'targa',
    'TI': 'basculante',
    'TR': 'comercial pesado',
    'VA': 'furgão',
    'WH': 'chassis',
    'WT': 'chassis cabine com plataforma'
}

driven_wheels_dict = {
    '-': '',
    '?': '?',
    '4': '4x4',
    'D': 'direta',
    'F': 'dianteira',
    'R': 'traseira'
}

fuel_type_dict = {
    '-': '',
    '?': '?',
    '1': 'mistura de etanol',
    '2': 'mistura de biodiesel',
    '3': 'mistura de metanol',
    'A': 'metanol',
    'B': 'biodiesel',
    'C': 'célula de combustível',
    'D': 'diesel',
    'E': 'elétrico',
    'F': 'E85',
    'G': 'GLP',
    'H': 'hidrogênio',
    'L': 'gasolina com chumbo',
    'M': 'M85',
    'N': 'gás natural comprimido',
    'P': 'gasolina premium',
    'R': 'ar comprimido',
    'T': 'álcool',
    'U': 'gasolina'
}

transmission_type_dict = {
    '-': '',
    '?': '?',
    'A': 'automática',
    'C': 'CVT',
    'D': 'dupla embreagem - somente automática',
    'I': 'automática com modo manual',
    'M': 'manual',
    'Q': 'manual sequencial com modo automático',
    'S': 'manual sequencial',
    'T': 'dupla embreagem man.sequ.com modo auto',
    'U': 'manual com embreagem automática',
    'V': 'CVT com modo manual'
}


class RtEntity(object, metaclass=abc.ABCMeta):
    """
        Base RT entity that satisfy the needs of any child RT entity
    """
    def __init__(self, raw_ents: [raw_ents.RawEntity] = None) -> None:
        self._vehicle_id = 0
        if raw_ents:
            self.assembly(raw_ents)

    @property
    def vehicle_id(self):
        return self._vehicle_id

    @vehicle_id.setter
    def vehicle_id(self, value):
        """
        Check vehicle_id length and date 
        :param value: 
        :return: 
        """
        if 13 < len(value) < 16 and value[-8:] > 19000100:
            self._vehicle_id = value
        else:
            raise ValueError('{} doesnt meet the vehicle_id criteria'.format(value))

    @abc.abstractmethod
    def _decode_raw_ent(self, raw_ent: raw_ents.RawEntity):
        """
            Populates this Entity with raw data from an raw entity
        :return:
        """
        pass

    def assembly(self, raw_ents: list):
        """
            Assemblies data from raw entities and store into the child Entity
        :param raw_ents: list of raw entities to compose the child entity 
        :return:
        """
        for raw_ent in raw_ents:
            self._decode_raw_ent(raw_ent)



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


class VehicleEntity(RtEntity):
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


class IncentiveEntity(RtEntity):
    def __init__(self, raw_ents=None):
        self.jato_value = ''
        self.take_rate = ''
        self.code = ''
        self.dealer_contrib_msrp = ''
        self.manuf_contrib_msrp = ''
        self.gov_contrib_msrp = ''
        self.deposit_perc = ''
        self.max_term = ''
        self.interest = ''
        self.start_date = ''
        self.end_date = ''
        self.public_notes = ''
        self.internal_comms = ''
        self.opt_id = ''
        self.rule_type = ''
        self.opt_rule = ''
        super().__init__(raw_ents)

    def __str__(self):
        return '|'.join([str(self.vehicle_id), str(self.jato_value), str(self.take_rate), str(self.code),
                         str(self.dealer_contrib_msrp), str(self.manuf_contrib_msrp), str(self.gov_contrib_msrp),
                         str(self.deposit_perc), str(self.max_term), str(self.interest), str(self.start_date),
                         str(self.end_date), str(self.public_notes), str(self.internal_comms), str(self.opt_id),
                         str(self.rule_type), str(self.opt_rule)])

    def _decode_raw_ent(self, raw_ent):
        self.vehicle_id = raw_ent.vehicle_id
        if raw_ent.schema_id == '47002':
            self.jato_value = raw_ent.data_value
        elif raw_ent.schema_id == '47102':
            self.take_rate = raw_ent.data_value
        elif raw_ent.schema_id == '47508':
            self.deposit_perc = raw_ent.data_value
        elif raw_ent.schema_id == '47504':
            self.max_term = raw_ent.data_value
        elif raw_ent.schema_id == '47505':
            self.interest = raw_ent.data_value
        elif raw_ent.schema_id == '45102':
            self.start_date = raw_ent.data_value
        elif raw_ent.schema_id == '45103':
            self.end_date = raw_ent.data_value
        elif raw_ent.schema_id == '51208':
            self.dealer_contrib_msrp = raw_ent.data_value
        elif raw_ent.schema_id == '51209':
            self.manuf_contrib_msrp = raw_ent.data_value
        elif raw_ent.schema_id == '51210':
            self.gov_contrib_msrp = raw_ent.data_value
        elif raw_ent.schema_id == '45204':
            self.public_notes = raw_ent.data_value
        elif raw_ent.schema_id == '45209':
            self.internal_comms = raw_ent.data_value
        else:
            raise NotImplementedError('schema_id ' + raw_ent.schema_id + ' is not implemented')


class TpEntity(RtEntity):
    def __init__(self, raw_ents=None):
        self._sample_date = 19000101  # yyyyMMdd
        self._transaction_price = 0.0
        super().__init__(raw_ents)

    @property
    def vehicle_id(self):
        return self._vehicle_id

    @vehicle_id.setter
    def vehicle_id(self, value):
        data_date = value[-8:]
        datetime.strptime(data_date, '%Y%m%d')  # check date format
        uid = value[:-9]
        if 4 < len(uid) < 8 and str.isnumeric(uid):  # check uid
            self._vehicle_id = value

    @property
    def sample_date(self):
        return self._sample_date

    @sample_date.setter
    def sample_date(self, value):
        datetime.strptime(str(value), '%Y%m%d')  # check date format
        self._sample_date = value

    @property
    def transaction_price(self):
        return self._transaction_price

    @transaction_price.setter
    def transaction_price(self, value):
        self._transaction_price = float(value)

    def __str__(self):
        return '|'.join([str(self.vehicle_id), str(self.sample_date), str(self.transaction_price)])

    def _decode_raw_ent(self, raw_ent):
        raw_ent.uid = str(int(float(raw_ent.uid)))  # get rid of the '.00' that comes from MS Access
        self.vehicle_id = '{0}{1}'.format(raw_ent.uid, raw_ent.data_date)
        self.sample_date = raw_ent.sample_date
        self.transaction_price = raw_ent.transaction_price
