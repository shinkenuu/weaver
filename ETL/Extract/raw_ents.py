#!/usr/bin/env python

import abc

dict_version_state = {
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

dict_body_type = {
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

dict_driven_wheels = {
    '-': '',
    '?': '?',
    '4': '4x4',
    'D': 'direta',
    'F': 'dianteira',
    'R': 'traseira'
}

dict_fuel_type = {
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

dict_transmission_type = {
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
    def __init__(self, line=''):
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
    def __init__(self, line=''):
        self.vehicle_id = 0
        self.schema_id = None
        self.data_value = None
        super().__init__(line)

    def from_line(self, line):
        """
        Set this entity from a line of text (vehicle_id|schema_id|data_value)
        :param line: the line of text to set from
        :return: 
        """
        self.vehicle_id = line.split('|')[0]
        self.schema_id = line.split('|')[1]
        self.data_value = line.split('|')[2].strip('\n')

    def belongs_with(self, other):
        return self.vehicle_id == other.vehicle_id


class MsAccessTpEntity(RawEntity):
    """
        Microsoft Access Rt entity
    """
    def __init__(self, line=''):
        self.uid = 0
        self.data_date = 19000101  # yyyymmdd
        self.sample_date = 19000101  # yyyymmdd
        self.transaction_price = 0.0
        super().__init__(line)

    def from_line(self, line):
        """
        Set this entity from a line of text (uid|data_date|delivery_date|transaction_price)
        :param line: the line of text to set from
        :return: 
        """
        self.uid = line.split('|')[0]
        self.data_date = line.split('|')[1]
        self.sample_date = line.split('|')[2]
        self.transaction_price = line.split('|')[3].strip('\n')

    def belongs_with(self, other):
        return self.uid == other.uid and self.data_date == other.data_date
