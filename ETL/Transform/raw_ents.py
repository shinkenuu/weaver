#!/usr/bin/env python

import abc


class RawEntity(object, metaclass=abc.ABCMeta):
    def __init__(self, raw_data):
        if isinstance(raw_data, str):
            self.from_line(raw_data)
        elif isinstance(raw_data, tuple) or isinstance(raw_data, list):
            self.from_iterable(raw_data)
        else:
            raise TypeError('raw_data must be str or iterable')

    @abc.abstractmethod
    def from_line(self, line: str):
        """
            Populates this Entity with raw data from a file's line
        :return:
        """
        pass

    @abc.abstractmethod
    def from_iterable(self, iterable):
        """
            Populates this Entity with raw data from a iterable
        :return:
        """
        pass

    @abc.abstractmethod
    def belongs_with(self, other):
        """
            Compares two instances of raw_ent and check if they belong to the same transformed_ent
        :param other: another instance of raw_ent to be compared to this one
        :return: True if this and other raw_ent belongs to the same transfline='', iterable: tuple=Noneormed_ent
        """
        pass


class Cs2002Entity(RawEntity):
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


class MsAccessTpEntity(RawEntity):
    """
        Microsoft Access Rt entity
    """
    def __init__(self, raw_data):
        self.uid = 0
        self.data_date = 0  # %Y%m%d
        self._sample_date = 20000101  # %Y%m%d
        self._transaction_price = 0.0
        super().__init__(raw_data=raw_data)

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

    def from_line(self, line: str):
        """
        Set this entity from a line of text (uid|data_date|sample_date|transaction_price)
        :param line: the line of text to set from
        :return: 
        """
        self.uid, self.data_date, self.sample_date, self.transaction_price = line.strip('\n').split('|')

    def from_iterable(self, iterable):
        """
        Set this entity from a iterable
        :param iterable: (uid|data_date, sample_date, transaction_price)
        :return: 
        """
        self.uid, self.data_date, self.sample_date, self.transaction_price = iterable

    def belongs_with(self, other):
        return self.uid == other.uid and self.data_date == other.data_date and self.sample_date == other.sample_date
