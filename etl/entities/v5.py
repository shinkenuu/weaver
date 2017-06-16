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


class IncentiveEntity(V5Entity):
    """
        V5 Incentives entity
    """
    def __init__(self, raw_data):
        self.incentive_value_header = ''
        self.jato_value = 0.0
        self.take_rate_header = ''
        self.take_rate = 0.0
        self.contribution_header = ''
        self.dealer_contrib_price = 0.0
        self.government_contrib_price = 0.0
        self.manufacturer_contrib_price = 0.0
        self.finance_header = ''
        self.first_max_interest = None
        self.deposit_percent = None
        self.first_max_term = None
        self.final_balance = None
        self.incentive_header = ''
        self.inc_data_date = 0  # %d/%m/%Y
        self.inc_start_date = 0  # %d/%m/%Y
        self.inc_end_date = 0  # %d/%m/%Y
        self.incentive_comments_header = ''
        self.internal_comments = ''
        self.public_notes = ''
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
