#!/usr/bin/env python3

import abc


class ExtractedResult:
    vehicle_id = 0
    schema_id = None
    data_value = None

    def __init__(self):
        pass

    def from_line(self, line):
        """
        Constructor from a line of text (vehicle_id|schema_id|data_value)
        :param line: 
        :return: 
        """
        self.vehicle_id = line.split('|')[0]
        self.schema_id = line.split('|')[1]
        self.data_value = line.split('|')[2].strip('\n')


class Entity:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def _decode_result(self, result):
        """
            Populates this Entity with data from an extracted result
        :return:
        """
        return

    def assembly(self, results):
        """
            Assemblies data from results and store into this Entity
        :param results: list of Result this entity is to be composed of
        :return:
        """
        for result in results:
            self._decode_result(result)
