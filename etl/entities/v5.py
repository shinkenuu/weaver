from . import base


class V5Entity(base.RawEntity):
    """
        V5 entity
    """
    def __init__(self, raw_data):
        self.uid = 0
        self.data_date = 0
        super().__init__(raw_data=raw_data)

    def from_line(self, line: str):
        """
        Set this entity from a line of text
        :param line: the line of text to set from
        :return: 
        """
        raise NotImplementedError()

    def from_iterable(self, iterable):
        """
        Set this entity from a iterable
        :param iterable:
        :return: 
        """
        raise NotImplementedError()

    def from_dict(self, dictionary: dict):
        """
        Set this entity from a dictionary
        :param dictionary:
        :return: 
        """
        raise NotImplementedError()


class SpecsEntity(V5Entity):
    """
        SCBR Entity
    """
    def __init__(self, raw_data):
        self.uid = None
        self.data_date = None
        self.version_state = None
        self.make = None
        self.model = None
        self.version = None
        self.production_year = None
        self.model_year = None
        self.trim_level = None
        self.number_of_doors = None
        self.body_type = None
        self.liters = None
        self.price = None
        self.transmission_header = None
        self.transmission_description = None
        self.driven_wheels_header = None
        self.driven_wheels = None
        self.fuel_header = None
        self.fuel_type = None
        self.other_fuel_type = None
        super().__init__(raw_data=raw_data)

    def from_line(self, line: str):
        self.from_iterable(tuple(line.strip('\n').split('|')))

    def from_iterable(self, iterable: tuple):
        raise NotImplementedError()

    def from_dict(self, dictionary: dict):
        self.uid = None if not dictionary['UID'] else int(dictionary['UID'])
        self.data_date = None if not dictionary['Data dos dados'] else int(dictionary['Data dos dados'])
        self.version_state = dictionary['Estado Versão']
        self.make = dictionary['Marca']
        self.model = dictionary['Modelo']
        self.version = dictionary['Versão']
        self.production_year = None if not dictionary['Ano de Prod.'] else int(dictionary['Ano de Prod.'])
        self.model_year = None if not dictionary['Ano modelo'] else int(dictionary['Ano modelo'])
        self.trim_level = dictionary['Nível acabam.']
        self.number_of_doors = None if not dictionary['n° de portas'] else int(dictionary['n° de portas'])
        self.body_type = dictionary['Carroceria']
        self.liters = None if not dictionary['litros'] else float(dictionary['litros'])
        self.price = None if not dictionary['Preço'] else float(dictionary['Preço'])
        self.transmission_header = dictionary['Transmissão']
        self.transmission_description = dictionary['descr.transmis.']
        self.driven_wheels_header = dictionary['Tração']
        self.driven_wheels = dictionary['Tração']
        self.fuel_header = dictionary['Combustível']
        self.fuel_type = dictionary['Tipo Combust.']
        self.other_fuel_type = dictionary['outro combust.']


class IncentiveEntity(V5Entity):
    """
        V5 Incentives entity
    """
    def __init__(self, raw_data):
        self.incentive_value_header = None
        self.jato_value = None
        self.take_rate_header = None
        self.take_rate = None
        self.contribution_header = None
        self.dealer_contrib_price = None
        self.government_contrib_price = None
        self.manufacturer_contrib_price = None
        self.finance_header = None
        self.first_max_interest = None
        self.deposit_percent = None
        self.first_max_term = None
        self.final_balance = None
        self.incentive_header = None
        self.inc_data_date = None  # %d/%m/%Y
        self.inc_start_date = None  # %d/%m/%Y
        self.inc_end_date = None  # %d/%m/%Y
        self.incentive_comments_header = None
        self.internal_comments = None
        self.public_notes = None
        super().__init__(raw_data=raw_data)

    def from_line(self, line: str):
        self.from_iterable(tuple(line.strip('\n').split('|')))

    def from_iterable(self, iterable: tuple):
        self.uid = int(iterable[0])
        self.data_date = iterable[1]  # %d/%m/%Y
        self.incentive_value_header = iterable[2]
        self.jato_value = float(iterable[3])
        self.take_rate_header = iterable[4]
        self.take_rate = float(iterable[5])
        self.contribution_header = iterable[6]
        self.dealer_contrib_price = float(iterable[7])
        self.government_contrib_price = float(iterable[8])
        self.manufacturer_contrib_price = float(iterable[9])
        self.finance_header = iterable[10]
        self.first_max_interest = float(iterable[11])
        self.deposit_percent = float(iterable[12])
        self.first_max_term = int(iterable[13])
        self.incentive_header = iterable[14]
        self.inc_data_date = iterable[15]  # %d/%m/%Y
        self.inc_start_date = iterable[16]  # %d/%m/%Y
        self.inc_end_date = iterable[17]  # %d/%m/%Y
        self.incentive_comments_header = iterable[18]
        self.internal_comments = iterable[19]
        self.public_notes = iterable[20]

    def from_dict(self, dictionary: dict):
        self.uid = int(dictionary['UID'])
        self.data_date = dictionary['Data dos dados']  # %d/%m/%Y
        self.incentive_value_header = dictionary['Valor incentivo']
        self.jato_value = None if not dictionary['valor JATO'] else float(dictionary['valor JATO'])
        self.take_rate_header = dictionary['Taxa Penetração']
        self.take_rate = None if not dictionary['Tx penetração-%'] else float(dictionary['Tx penetração-%'])
        self.contribution_header = dictionary['Contribuição']
        self.dealer_contrib_price = None if not dictionary['contr.con.-prç'] else float(dictionary['contr.con.-prç'])
        self.government_contrib_price = None if not dictionary['contr.gov.-prç'] \
            else float(dictionary['contr.gov.-prç'])
        self.manufacturer_contrib_price = None if not dictionary['contr.fab.-prç'] \
            else float(dictionary['contr.fab.-prç'])
        self.finance_header = dictionary['Financiamento']
        self.first_max_interest = None if not dictionary['1º per tx juros'] else float(dictionary['1º per tx juros'])
        self.deposit_percent = None if not dictionary['ent (%pç)'] else float(dictionary['ent (%pç)'])
        self.first_max_term = None if not dictionary['1ºper max meses'] else int(dictionary['1ºper max meses'])
        self.final_balance = None if not dictionary['bal.final (%pç)'] else float(dictionary['bal.final (%pç)'])
        self.incentive_header = dictionary['Incentivo']
        self.inc_data_date = dictionary['data envio']  # %d/%m/%Y
        self.inc_start_date = dictionary['data início']  # %d/%m/%Y
        self.inc_end_date = dictionary['data fim']  # %d/%m/%Y
        self.incentive_comments_header = dictionary['Comen.incentivo']
        self.internal_comments = dictionary['com.int. - nota']
        self.public_notes = dictionary['notas públicas']
