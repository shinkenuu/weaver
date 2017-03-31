#!/usr/bin/env python3

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


class RawEntity:
    """
    CS_2002 raw entity
    """
    vehicle_id = 0
    schema_id = None
    data_value = None


    def __init__(self):
        pass

    def from_line(self, line):
        """
        Constructor from a line of text (vehicle_id|schema_id|data_value)
        :param line: 
        :return: 
        """
        self.vehicle_id = line.split('|')[0]
        self.schema_id = line.split('|')[1]
        self.data_value = line.split('|')[2].strip('\n')


class AssembledEntity:
    """
    Super class for assembled CS_2002 entities
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        pass

    @abc.abstractmethod
    def _decode_raw_ent(self, raw_ent):
        """
            Populates this Entity with raw data from an raw entity
        :return:
        """
        pass

    def assembly(self, raw_ents):
        """
            Assemblies data from raw entities and store into the child Entity
        :param raw_ents: list of raw entities to compose the child entity 
        :return:
        """
        for raw_ent in raw_ents:
            self._decode_raw_ent(raw_ent)
