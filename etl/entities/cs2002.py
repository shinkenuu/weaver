from . import base


class Cs2002Entity(base.RawEntity, base.AssemblableEntity):
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
        split_line = line.strip('\n').split('|')
        self.vehicle_id = int(split_line[0])
        self.schema_id = int(split_line[1])
        self.data_value = split_line[2]

    def from_iterable(self, iterable):
        """
        Set this entity from a iterable
        :param iterable: (vehicle_id, schema_id, data_value)
        :return: 
        """
        self.vehicle_id, self.schema_id, self.data_value = iterable

    def from_dict(self, dictionary: dict):
        """
        Set this entity from a dictionary
        :param dictionary:
        :return: 
        """
        raise NotImplementedError()

    def assemblies_with(self, other):
        return self.vehicle_id == other.vehicle_id


class EscbrBrPublicIncentiveEntity(Cs2002Entity, base.AssemblableEntity):
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
        split_line = line.strip('\n').split('|')
        self.vehicle_id = int(split_line[0])
        self.schema_id = int(split_line[1])
        self.data_value = split_line[2]
        self.option_id = int(split_line[3])
        self.option_code = split_line[4]
        self.rule_type = int(split_line[5])
        self.option_rule = split_line[6]

    def from_iterable(self, iterable: tuple):
        self.vehicle_id, self.schema_id, self.data_value, self.option_id, self.option_code, self.rule_type,\
            self.option_rule = iterable

    def from_dict(self, dictionary: dict):
        super().from_dict(dictionary=dictionary)

    def assemblies_with(self, other):
        return super().assemblies_with(other) and other.option_id == self.option_id
