from ETL.Entities import raw as raw


class Cs2002Entity(raw.RawEntity):
    """
        CS_2002 entity
    """
    def __init__(self, raw_data):
        self.vehicle_id = 0
        self.schema_id = 0
        self.data_value = ''
        super().__init__(raw_data=raw_data)

    def from_line(self, line: str):
        """
        Set this entity from a line of text [vehicle_id|schema_id|data_value]
        :param line: the line of text to set from
        :return: 
        """
        self.vehicle_id, self.schema_id, self.data_value = line.strip('\n').split('|')

    def from_iterable(self, iterable):
        """
        Set this entity from a iterable
        :param iterable: (vehicle_id, schema_id, data_value)
        :return: 
        """
        self.vehicle_id, self.schema_id, self.data_value = iterable

    def belongs_with(self, other):
        return self.vehicle_id == other.vehicle_id


class EscbrBrPublicIncentiveEntity(Cs2002Entity):
    """
        Escbr_BR_Public_Incentive entity
    """
    def __init__(self, raw_data):
        self.vehicle_id = 0
        self.schema_id = 0
        self.data_value = ''
        self.option_id = 0
        self.option_code = ''
        self.rule_type = 0
        self.option_rule = ''
        super().__init__(raw_data=raw_data)

    def from_line(self, line: str):
        self.vehicle_id, self.schema_id, self.data_value, self.option_id, self.option_code, self.rule_type,\
            self.option_rule = line.strip('\n').split('|')

    def from_iterable(self, iterable: tuple):
        self.vehicle_id, self.schema_id, self.data_value, self.option_id, self.option_code, self.rule_type,\
            self.option_rule = iterable

    def belongs_with(self, other):
        return super().belongs_with(other) and other.option_id == self.option_id
