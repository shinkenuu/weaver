import abc
import re
from . import base, cs2002 as cs2002_ents, msaccess as msaccess_ents

version_state_dict = {
    '-': '',
    '?': '',
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
    '?': '',
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
    'WT': 'chassis cabine com plataforma',
    'WV': 'furgão com janelas'
}

driven_wheels_dict = {
    '-': '',
    '?': '',
    '4': '4x4',
    'D': 'direta',
    'F': 'dianteira',
    'R': 'traseira'
}

fuel_type_dict = {
    '-': '',
    '?': '',
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
    '?': '',
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

version_regex = re.compile(r'^([(])(O|!|\+|0)([)])')


def compose(current: str, new: str):
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


class RtEntity(object, metaclass=abc.ABCMeta):
    """
        Base RT entity that RT entity child must inherit of
    """
    def __init__(self):
        self.vehicle_id = 0


class VehicleEntity(RtEntity, base.AssemblerEntity):
    def __init__(self, raw_ent_list: [cs2002_ents.Cs2002Entity]=None):
        super().__init__()
        self.uid = 0
        self.data_date = 0  # %Y%m%d
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
        if raw_ent_list:
            self.assembly(cs2002_ent_list=raw_ent_list)

    def __str__(self):
        return '|'.join([str(self.vehicle_id), str(self.uid), str(self.data_date), str(self.version_state),
                         str(self.make), str(self.model), str(self.version), '1' if self.outgoing else '0',
                         str(self.production_year), str(self.model_year), str(self.trim_level),
                         str(self.number_of_doors), str(self.body_type), str(self.fuel_type), str(self.other_fuel_type),
                         str(self.transmission_description), str(self.driven_wheels), str(self.liters), str(self.msrp)])

    def _decode_raw_ent(self, cs2002_ent: cs2002_ents.Cs2002Entity):
        """
        Decodes schema_id from raw_entEntity and assigns its data_value to the right SpecsEntity attribute
        Raises NotImplementedError with schema_id is not coded
        :param cs2002_ent: Cs2002 entity
        :return: 
        """
        if cs2002_ent.schema_id == 101:
            self.uid = int(cs2002_ent.data_value)
        elif cs2002_ent.schema_id == 104:
            self.data_date = int(cs2002_ent.data_value)
        elif cs2002_ent.schema_id == 105:
            self.version_state = compose(current=self.version_state,
                                         new=version_state_dict[cs2002_ent.data_value])
            if cs2002_ent.data_value == 'G':  # outgoing flag
                self.outgoing = True
        elif cs2002_ent.schema_id == 111:
            self.make = cs2002_ent.data_value
        elif cs2002_ent.schema_id == 112:
            self.model = cs2002_ent.data_value
        elif cs2002_ent.schema_id == 302:
            self.version = version_regex.sub('', cs2002_ent.data_value)
        elif cs2002_ent.schema_id == 57108:
            self.production_year = int(cs2002_ent.data_value)
        elif cs2002_ent.schema_id == 108:
            self.model_year = int(cs2002_ent.data_value)
        elif cs2002_ent.schema_id == 402:
            self.trim_level = cs2002_ent.data_value
        elif cs2002_ent.schema_id == 602:
            self.number_of_doors = int(cs2002_ent.data_value)
        elif cs2002_ent.schema_id == 603:
            self.body_type = body_type_dict[cs2002_ent.data_value]
        elif cs2002_ent.schema_id == 8702:
            self.fuel_type = fuel_type_dict[cs2002_ent.data_value]
        elif cs2002_ent.schema_id == 8703:
            self.other_fuel_type = fuel_type_dict[cs2002_ent.data_value]
        elif cs2002_ent.schema_id == 20624:
            self.transmission_description = compose(current=self.transmission_description,
                                                    new=transmission_type_dict[cs2002_ent.data_value])
        elif cs2002_ent.schema_id == 6502:
            self.driven_wheels = driven_wheels_dict[cs2002_ent.data_value]
        elif cs2002_ent.schema_id == 7403:
            self.liters = float(cs2002_ent.data_value)
        elif cs2002_ent.schema_id == 902:
            self.msrp = float(cs2002_ent.data_value)
        else:
            raise NotImplementedError('schema_id {0} is not implemented'.format(str(cs2002_ent.schema_id)))

    def scavenge_common_data(self, raw_ent: cs2002_ents.Cs2002Entity):
        self.vehicle_id = raw_ent.vehicle_id

    def assembly(self, cs2002_ent_list: [cs2002_ents.Cs2002Entity]):
        if len(cs2002_ent_list) < 1:
            raise IndexError("VehicleEntity's cs2002_ent_list cannot be empty")
        self.scavenge_common_data(cs2002_ent_list[0])
        for ent in cs2002_ent_list:
            self._decode_raw_ent(ent)


class IncentiveEntity(RtEntity, base.AssemblerEntity):
    def __init__(self, raw_ent_list: [base.RawEntity]=None, raw_ent: base.RawEntity=None):
        super().__init__()
        self.data_date = 0  # %Y%m%d
        self.jato_value = 0.0
        self.take_rate = 0.0
        self.code = ''
        self.dealer_contrib_msrp = 0.0
        self.manuf_contrib_msrp = 0.0
        self.gov_contrib_msrp = 0.0
        self.deposit_perc = 0.0
        self.max_term = 0
        self.interest_perc = 0.0
        self.start_date = 0  # %Y%m%d
        self.end_date = 0  # %Y%m%d
        self.public_notes = ''
        self.internal_comms = ''
        self.opt_id = 0
        self.rule_type = 0
        self.opt_rule = ''
        if raw_ent_list:
            self.assembly(raw_ent_list)
        elif raw_ent:
                if isinstance(raw_ent, msaccess_ents.CsRtIncentivesEntity):
                    self.from_msaccess_cs_rt_incentives(raw_ent)

    def __str__(self):
        return '|'.join([str(self.vehicle_id), str(self.data_date), str(self.jato_value), str(self.take_rate),
                         str(self.code), str(self.dealer_contrib_msrp), str(self.gov_contrib_msrp),
                         str(self.manuf_contrib_msrp), str(self.interest_perc), str(self.deposit_perc),
                         str(self.max_term), str(self.start_date), str(self.end_date), str(self.public_notes),
                         str(self.internal_comms), str(self.opt_id), str(self.rule_type), str(self.opt_rule)])

    def _decode_raw_ent(self, escbr_ent: cs2002_ents.EscbrBrPublicIncentiveEntity):
        if escbr_ent.schema_id == 45112:
            self.data_date = int(escbr_ent.data_value)
        if escbr_ent.schema_id == 47002:
            self.jato_value = float(escbr_ent.data_value)
        elif escbr_ent.schema_id == 47102:
            self.take_rate = float(escbr_ent.data_value)
        elif escbr_ent.schema_id == 51208:
            self.dealer_contrib_msrp = float(escbr_ent.data_value)
        elif escbr_ent.schema_id == 51210:
            self.gov_contrib_msrp = float(escbr_ent.data_value)
        elif escbr_ent.schema_id == 51209:
            self.manuf_contrib_msrp = float(escbr_ent.data_value)
        elif escbr_ent.schema_id == 47505:
            self.interest_perc = float(escbr_ent.data_value)
        elif escbr_ent.schema_id == 47508:
            self.deposit_perc = float(escbr_ent.data_value)
        elif escbr_ent.schema_id == 47504:
            self.max_term = int(escbr_ent.data_value)
        elif escbr_ent.schema_id == 45102:
            self.start_date = int(escbr_ent.data_value)
        elif escbr_ent.schema_id == 45103:
            self.end_date = int(escbr_ent.data_value)
        elif escbr_ent.schema_id == 45204:
            self.public_notes = escbr_ent.data_value
        elif escbr_ent.schema_id == 45209:
            self.internal_comms = escbr_ent.data_value
        else:
            raise NotImplementedError('schema_id {0} is not implemented'.format(str(escbr_ent.schema_id)))

    def from_msaccess_cs_rt_incentives(self, cs_rt_incentive_ent: msaccess_ents.CsRtIncentivesEntity):
        self.vehicle_id = '{0}{1}'.format(cs_rt_incentive_ent.uid, cs_rt_incentive_ent.data_date)
        self.jato_value = cs_rt_incentive_ent.jato_val
        self.take_rate = cs_rt_incentive_ent.take_rate
        self.code = cs_rt_incentive_ent.inc_aaaaa
        self.manuf_contrib_msrp = cs_rt_incentive_ent.manuf_cont
        self.dealer_contrib_msrp = cs_rt_incentive_ent.dealer_cont
        self.gov_contrib_msrp = 0.0
        self.start_date = cs_rt_incentive_ent.start  # %Y%m%d
        self.end_date = cs_rt_incentive_ent.end  # %Y%m%d
        self.deposit_perc = cs_rt_incentive_ent.perc_dep
        self.max_term = cs_rt_incentive_ent.months_pay
        self.interest_perc = cs_rt_incentive_ent.int_rate
        self.public_notes = cs_rt_incentive_ent.public_notes
        self.internal_comms = cs_rt_incentive_ent.internal_comments
        self.opt_id = 0
        self.rule_type = 0
        self.opt_rule = ''

    def scavenge_common_data(self, escbr_ent: cs2002_ents.EscbrBrPublicIncentiveEntity):
        self.vehicle_id = escbr_ent.vehicle_id
        self.code = escbr_ent.option_code
        self.opt_id = escbr_ent.option_id
        self.rule_type = escbr_ent.rule_type
        self.opt_rule = escbr_ent.option_rule

    def assembly(self, escbr_ent_list: [cs2002_ents.EscbrBrPublicIncentiveEntity]):
        if len(escbr_ent_list) < 1:
            raise IndexError("IncentiveEntity's escbr_ent_list cannot be empty")
        self.scavenge_common_data(escbr_ent=escbr_ent_list[0])
        for escbr_ent in escbr_ent_list:
            self._decode_raw_ent(escbr_ent=escbr_ent)


class TpEntity(RtEntity):
    def __init__(self, cs_rt_tp_ent: msaccess_ents.CsRtTpCompletaEntity=None):
        super().__init__()
        self.sample_date = 0  # %Y%m%d
        self.transaction_price = 0.0
        if cs_rt_tp_ent:
            self.from_cs_rt_tp_completa_ent(ent=cs_rt_tp_ent)

    def __str__(self):
        return '|'.join([str(self.vehicle_id), str(self.sample_date), str(self.transaction_price)])

    def from_cs_rt_tp_completa_ent(self, ent: msaccess_ents.CsRtTpCompletaEntity):
        self.vehicle_id = base.build_vehicle_id(ent.uid, ent.data_date)
        self.sample_date = ent.sample_date
        self.transaction_price = ent.transaction_price
