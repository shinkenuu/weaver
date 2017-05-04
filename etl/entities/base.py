import abc
from datetime import datetime


def check_date_format(value: str):
    try:
        datetime.strptime(value, '%Y%m%d')  # check date format
        return True
    except ValueError:
        return False


class RawEntity(object, metaclass=abc.ABCMeta):
    def __init__(self, raw_data):
        if isinstance(raw_data, str):
            self.from_line(raw_data)
        elif isinstance(raw_data, tuple) or isinstance(raw_data, list):
            self.from_iterable(raw_data)
        else:
            raise TypeError('raw_data must be str or __iter__')

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


class AssemblableEntity(object, metaclass=abc.ABCMeta):
    """
        A entity to be assembled with others Assemblable entities
    """
    def __init__(self):
        pass

    @abc.abstractmethod
    def assemblies_with(self, other):
        """
            Compares two instances of assemblable ents and check if they belong to the same assembled entity
        :param other: another assemblable to be compared to this one
        :return: True if this and other assemblable belongs to the same assembled entity
        """
        pass


class EntityAssembler(object, metaclass=abc.ABCMeta):
    """
        A entity to be assembly multiple AssemblableEntity
    """
    def __init__(self):
        pass

    @abc.abstractmethod
    def assembly(self, assemblables_list: [raw.AssemblableEntity]):
        """
        Assemblies multiple assemblable entities into the AssemblerEntity
        :param assemblables_list: a list with AssemblableEntities to be assembly and populate the caller entity
        :return: 
        """
        pass