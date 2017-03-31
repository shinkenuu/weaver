#!/usr/bin/env python3

import abc


class RawEntity:
    """
    RT_CS_TP_? raw entity
    """
    uid = 0
    data_date = 0
    delivery_date = 0
    transaction_price = 0.0

    def __init__(self):
        pass

    def from_line(self, line):
        """
        Constructor from a line of text (uid|data_date|delivery_date|transaction_price)
        :param line: 
        :return: 
        """
        self.uid = line.split('|')[0]
        self.data_date = line.split('|')[1]
        self.delivery_date = line.split('|')[2]
        self.transaction_price = line.split('|')[3].strip('\n')


class AssembledEntity:
    """
    Super class for assembled Incentives entities
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
