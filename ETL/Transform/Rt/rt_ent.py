#!/usr/bin/env python

import abc
from ETL.Extract import raw_ents


class RtEntity:
    """
        Base RT entity that satisfy the needs of any child RT entity
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self, raw_ents: [raw_ents.RawEntity] = None) -> None:
        self._vehicle_id = 0
        if raw_ents:
            self.assembly(raw_ents)

    @property
    def vehicle_id(self):
        return self._vehicle_id

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
