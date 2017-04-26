#!/usr/bin/env python

import abc

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


class RawEntity(object, metaclass=abc.ABCMeta):
    def __init__(self, line: str=''):
        if line != '':
            self.from_line(line)

    @abc.abstractmethod
    def from_line(self, line):
        """
            Populates this Entity with raw data from a file's line
        :return:
        """
        pass

    @abc.abstractmethod
    def belongs_with(self, other):
        """
            Compares two instances of raw_ent and check if they belong to the same transformed_ent
        :param other: another instance of raw_ent to be compared to this one
        :return: True if this and other raw_ent belongs to the same transformed_ent
        """
        pass


class Cs2002Entity(RawEntity):
    """
        CS_2002 entity
    """
    def __init__(self, line: str=''):
        self.vehicle_id = 0
        self.schema_id = 0
        self.data_value = ''
        super().__init__(line)

    def from_line(self, line: str):
        """
        Set this entity from a line of text [vehicle_id|schema_id|data_value]
        :param line: the line of text to set from
        :return: 
        """
        self.vehicle_id, self.schema_id, self.data_value = line.strip('\n').split('|')

    def belongs_with(self, other):
        return self.vehicle_id == other.vehicle_id


class EscbrBrPublicIncentiveEntity(Cs2002Entity):
    """
        Escbr_BR_Public_Incentive entity
    """
    def __init__(self, line: str=''):
        self.vehicle_id = 0
        self.schema_id = 0
        self.data_value = ''
        self.option_id = 0
        self.option_code = ''
        self.rule_type = 0
        self.option_rule = ''
        if line == '':
            super().__init__()
        else:
            self.from_line(line)

    def from_line(self, line: str):
        self.vehicle_id, self.schema_id, self.data_value, self.option_id, self.option_code, self.rule_type,\
            self.option_rule = line.strip('\n').split('|')

    def belongs_with(self, other):
        return super().belongs_with(other) and self.option_id == other.option_id


class MsAccessTpEntity(RawEntity):
    """
        Microsoft Access Rt entity
    """
    def __init__(self, line=''):
        self.uid = 0
        self.data_date = 0  # yyyymmdd
        self._sample_date = 20000101  # yyyymmdd
        self._transaction_price = 0.0
        super().__init__(line)

    @property
    def sample_date(self):
        return self._sample_date

    @sample_date.setter
    def sample_date(self, value: int):
        if value > 20000100:
            self._sample_date = value

    @property
    def transaction_price(self):
        return self._transaction_price

    @transaction_price.setter
    def transaction_price(self, value: float):
        if value > 0.0:
            self._transaction_price = value

    def from_line(self, line):
        """
        Set this entity from a line of text (uid|data_date|sample_date|transaction_price)
        :param line: the line of text to set from
        :return: 
        """
        self.uid, self.data_date, self.sample_date, self.transaction_price = line.strip('\n').split('|')

    def belongs_with(self, other):
        return self.uid == other.uid and self.data_date == other.data_date and self.sample_date == other.sample_date


types_dict = {
    'sscbr_cs_2002': Cs2002Entity,
    'nscbr_cs_2002': Cs2002Entity,
    'escbr_cs_2002_br_public_incentive': EscbrBrPublicIncentiveEntity,
    'cs_rt_tp_completa': MsAccessTpEntity,
    'cs_rt_tp_toyota': MsAccessTpEntity
}
