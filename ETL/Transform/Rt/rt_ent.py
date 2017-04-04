import abc


class AssemblerEntity:
    """
        
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        self.vehicle_id = 0

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
