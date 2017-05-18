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
        pass

    def from_iterable(self, iterable):
        """
        Set this entity from a iterable
        :param iterable:
        :return: 
        """
        pass


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
        self.first_max_interest = 0.0
        self.deposit_percent = 0.0
        self.first_max_term = 0
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
        self.first_max_interest = float(iterable[11]) if iterable[11] else None
        self.deposit_percent = float(iterable[12]) if iterable[12] else None
        self.first_max_term = int(iterable[13]) if iterable[12] else None
        self.incentive_header = iterable[14]
        self.inc_data_date = iterable[15]  # %d/%m/%Y
        self.inc_start_date = iterable[16]  # %d/%m/%Y
        self.inc_end_date = iterable[17]  # %d/%m/%Y
        self.incentive_comments_header = iterable[18]
        self.internal_comments = iterable[19]
        self.public_notes = iterable[20]
