import abc
from datetime import datetime
import math
import re

from . import base, cs2002 as cs2002_ents, v5 as v5_ents, msaccess as msaccess_ents

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


def calc_interest_rate_per_month(yearly_interest: float) -> float:
    return (math.pow(yearly_interest / 100 + 1, 1/12) - 1) * 100


class RtEntity(object, metaclass=abc.ABCMeta):
    """
        Base RT entity that RT entity child must inherit of
    """
    def __init__(self):
        self.vehicle_id = 0


class VehicleEntity(RtEntity, base.AssemblerEntity):
    coded_v5_specs_version_state_dict = {
        'especificações': version_state_dict['S'],
        'opcionais': version_state_dict['O'],
        'alt.preço': version_state_dict['P'],
        'ano modelo': version_state_dict['M'],
        'impostos': version_state_dict['T'],
        'frota': version_state_dict['L'],
        'novo modelo': version_state_dict['N'],
        'moeda': version_state_dict['C'],
        'novo visual': version_state_dict['F'],
        'nova versão': version_state_dict['V'],
        're-introdução': version_state_dict['R'],
        'Mud.nome modelo': version_state_dict['D'],
        'Mud.nome marca': version_state_dict['K'],
        'descontinuada': version_state_dict['G'],
    }

    def __init__(self, raw_ent_list: [cs2002_ents.Cs2002Entity]=None, raw_ent: base.RawEntity=None):
        super().__init__()
        self.uid = None
        self.data_date = None  # %Y%m%d
        self.version_state = None
        self.outgoing = None
        self.make = None
        self.model = None
        self.version = None
        self.production_year = None
        self.model_year = None
        self.trim_level = None
        self.number_of_doors = None
        self.body_type = None
        self.fuel_type = None
        self.other_fuel_type = None
        self.transmission_description = None
        self.driven_wheels = None
        self.liters = None
        self.msrp = None
        if raw_ent_list:
            self.assembly(cs2002_ent_list=raw_ent_list)
        elif raw_ent:
                if isinstance(raw_ent, v5_ents.SpecsEntity):
                    self.from_v5_specs(v5_spec_ent=raw_ent)

    def __str__(self):
        return '|'.join([str(self.vehicle_id), str(self.uid), str(self.data_date),
                         '' if not self.version_state else str(self.version_state),
                         '' if not self.make else str(self.make), '' if not self.model else str(self.model),
                         '' if not self.version else str(self.version), '1' if self.outgoing else '0',
                         '' if not self.production_year else str(self.production_year),
                         '' if not self.model_year else str(self.model_year),
                         '' if not self.trim_level else str(self.trim_level),
                         '' if not self.number_of_doors else str(self.number_of_doors),
                         '' if not self.body_type else str(self.body_type),
                         '' if not self.fuel_type else str(self.fuel_type),
                         '' if not self.other_fuel_type else str(self.other_fuel_type),
                         '' if not self.transmission_description else str(self.transmission_description),
                         '' if not self.driven_wheels else str(self.driven_wheels),
                         '' if not self.liters else str(self.liters), '' if not self.msrp else str(self.msrp)])

    def from_v5_specs(self, v5_spec_ent: v5_ents.SpecsEntity):
        def format_date(date_str: str):
            date = datetime.strptime(date_str, '%d/%m/%Y')
            return int(date.strftime('%Y%m%d'))

        def decode_version_state():
            if not v5_spec_ent.version_state:
                return None
            decoded_version_states = []
            try:
                for coded_version_state in v5_spec_ent.version_state.split(':'):
                    decoded_version_states.append(VehicleEntity.coded_v5_specs_version_state_dict[coded_version_state])
            except KeyError:
                raise IndexError(
                    'Couldnt find the key to decode a version state within "{}"'.format(v5_spec_ent.version_state))
            return ', '.join(decoded_version_states)

        self.vehicle_id = '{}{}'.format(v5_spec_ent.uid, v5_spec_ent.data_date)
        self.uid = v5_spec_ent.uid
        self.data_date = v5_spec_ent.data_date
        self.version_state = decode_version_state()
        self.outgoing = True if 'descontinuada' in v5_spec_ent.version_state else False
        self.make = v5_spec_ent.make
        self.model = v5_spec_ent.model
        self.version = v5_spec_ent.version
        self.production_year = v5_spec_ent.production_year
        self.model_year = v5_spec_ent.model_year
        self.trim_level = v5_spec_ent.trim_level
        self.number_of_doors = v5_spec_ent.number_of_doors
        self.body_type = v5_spec_ent.body_type
        self.fuel_type = v5_spec_ent.fuel_type
        self.other_fuel_type = v5_spec_ent.other_fuel_type
        self.transmission_description = v5_spec_ent.transmission_description
        self.driven_wheels = v5_spec_ent.driven_wheels
        self.liters = v5_spec_ent.liters
        self.msrp = v5_spec_ent.price

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
        self.interest_perc = 0.0
        self.deposit_perc = 0.0
        self.max_term = 0
        self.final_balance_perc = 0.0
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
                if isinstance(raw_ent, v5_ents.IncentiveEntity):
                    self.from_v5_incentives(v5_inc_ent=raw_ent)
                elif isinstance(raw_ent, msaccess_ents.CsRtIncentivesEntity):
                    self.from_msaccess_cs_rt_incentives(cs_rt_incentive_ent=raw_ent)

    def __str__(self):
        return '|'.join([str(self.vehicle_id), str(self.data_date),
                         str(self.jato_value) if self.jato_value is not None else '',
                         str(self.take_rate) if self.take_rate is not None else '',
                         str(self.code), str(self.dealer_contrib_msrp) if self.dealer_contrib_msrp is not None else '',
                         str(self.gov_contrib_msrp) if self.gov_contrib_msrp is not None else '',
                         str(self.manuf_contrib_msrp) if self.manuf_contrib_msrp is not None else '',
                         str(self.interest_perc) if self.interest_perc is not None else '',
                         str(self.deposit_perc) if self.deposit_perc is not None else '',
                         str(self.max_term) if self.max_term is not None else '',
                         str(self.final_balance_perc) if self.final_balance_perc is not None else '',
                         str(self.start_date), str(self.end_date), str(self.public_notes), str(self.internal_comms),
                         str(self.opt_id), str(self.rule_type), str(self.opt_rule)])

    def from_msaccess_cs_rt_incentives(self, cs_rt_incentive_ent: msaccess_ents.CsRtIncentivesEntity):
        self.vehicle_id = '{0}{1}'.format(cs_rt_incentive_ent.uid, cs_rt_incentive_ent.data_date)
        self.jato_value = cs_rt_incentive_ent.jato_val
        self.take_rate = cs_rt_incentive_ent.take_rate
        self.code = cs_rt_incentive_ent.inc_aaaaa
        self.dealer_contrib_msrp = cs_rt_incentive_ent.dealer_cont
        self.gov_contrib_msrp = 0.0
        self.manuf_contrib_msrp = cs_rt_incentive_ent.manuf_cont
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

    def from_v5_incentives(self, v5_inc_ent: v5_ents.IncentiveEntity):
        def format_date(date_str: str):
            date = datetime.strptime(date_str, '%d/%m/%Y')
            return int(date.strftime('%Y%m%d'))

        def find_incentive_code():
            def slice_through_code(header: str):
                return header[header.index('[')+1:header.index(']')]

            if v5_inc_ent.contribution_header:
                return slice_through_code(v5_inc_ent.contribution_header)
            elif v5_inc_ent.take_rate_header:
                return slice_through_code(v5_inc_ent.take_rate_header)
            elif v5_inc_ent.finance_header:
                return slice_through_code(v5_inc_ent.finance_header)
            elif v5_inc_ent.incentive_comments_header:
                return slice_through_code(v5_inc_ent.incentive_comments_header)
            elif v5_inc_ent.incentive_header:
                return slice_through_code(v5_inc_ent.incentive_header)
            elif v5_inc_ent.incentive_value_header:
                return slice_through_code(v5_inc_ent.incentive_value_header)
            else:
                raise IndexError('No incentive code found')

        def slice_through_br_comment(comm: str):
            try:
                return comm[comm.index(':') + 1:]
            except ValueError:  # If ':' wasn't found in comm
                return ''

        self.vehicle_id = '{}{}'.format(str(v5_inc_ent.uid), format_date(v5_inc_ent.data_date))
        self.data_date = format_date(v5_inc_ent.inc_data_date)
        self.jato_value = v5_inc_ent.jato_value
        self.take_rate = v5_inc_ent.take_rate
        self.code = find_incentive_code()
        self.dealer_contrib_msrp = v5_inc_ent.dealer_contrib_price
        self.gov_contrib_msrp = v5_inc_ent.government_contrib_price
        self.manuf_contrib_msrp = v5_inc_ent.manufacturer_contrib_price
        self.start_date = format_date(v5_inc_ent.inc_start_date)
        self.end_date = format_date(v5_inc_ent.inc_end_date)
        self.deposit_perc = v5_inc_ent.deposit_percent
        self.max_term = v5_inc_ent.first_max_term
        self.interest_perc = calc_interest_rate_per_month(v5_inc_ent.first_max_interest) \
            if isinstance(v5_inc_ent.first_max_interest, float) else None
        self.public_notes = slice_through_br_comment(v5_inc_ent.public_notes)
        self.internal_comms = slice_through_br_comment(v5_inc_ent.internal_comments)
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
        def decode_raw_ent(escbr_assemblable_ent: cs2002_ents.EscbrBrPublicIncentiveEntity):
            if escbr_assemblable_ent.schema_id == 45112:
                self.data_date = int(escbr_assemblable_ent.data_value)
            if escbr_assemblable_ent.schema_id == 47002:
                self.jato_value = float(escbr_assemblable_ent.data_value)
            elif escbr_assemblable_ent.schema_id == 47102:
                self.take_rate = calc_interest_rate_per_month(float(escbr_assemblable_ent.data_value))
            elif escbr_assemblable_ent.schema_id == 51208:
                self.dealer_contrib_msrp = float(escbr_assemblable_ent.data_value)
            elif escbr_assemblable_ent.schema_id == 51210:
                self.gov_contrib_msrp = float(escbr_assemblable_ent.data_value)
            elif escbr_assemblable_ent.schema_id == 51209:
                self.manuf_contrib_msrp = float(escbr_assemblable_ent.data_value)
            elif escbr_assemblable_ent.schema_id == 47505:
                self.interest_perc = float(escbr_assemblable_ent.data_value)
            elif escbr_assemblable_ent.schema_id == 47508:
                self.deposit_perc = float(escbr_assemblable_ent.data_value)
            elif escbr_assemblable_ent.schema_id == 47504:
                self.max_term = int(escbr_assemblable_ent.data_value)
            elif escbr_assemblable_ent.schema_id == 45102:
                self.start_date = int(escbr_assemblable_ent.data_value)
            elif escbr_assemblable_ent.schema_id == 45103:
                self.end_date = int(escbr_assemblable_ent.data_value)
            elif escbr_assemblable_ent.schema_id == 45204:
                self.public_notes = escbr_assemblable_ent.data_value
            elif escbr_assemblable_ent.schema_id == 45209:
                self.internal_comms = escbr_assemblable_ent.data_value
            else:
                raise NotImplementedError('schema_id {0} is not implemented'.format(str(escbr_ent.schema_id)))

        if len(escbr_ent_list) < 1:
            raise IndexError("IncentiveEntity's escbr_ent_list cannot be empty")
        self.scavenge_common_data(escbr_ent=escbr_ent_list[0])
        for escbr_ent in escbr_ent_list:
            decode_raw_ent(escbr_assemblable_ent=escbr_ent)


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
