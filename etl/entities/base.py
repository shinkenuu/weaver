import abc
from datetime import datetime


def build_vehicle_id(uid: int, data_date: int):
    """
    Check uid and datadate to build a vehicle_id
    :param uid: 
    :param data_date: 
    :return: vehicle_id
    """
    str_uid = str(uid)
    str_data_date = str(data_date)
    if 5 < len(str_uid) < 8 and check_date_format(str(str_data_date)):
        return '{}{}'.format(str_uid, str_data_date)
    else:
        raise ValueError('{}{} is not a valid vehicle_id'.format(str_uid, str_data_date))


def check_date_format(value: str):
    """
    Check date %Y%m%d format. May raise ValueError
    :param value: the date to be checked
    :return: True if date is OK. False otherwise
    """
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


class AssemblerEntity(object, metaclass=abc.ABCMeta):
    """
        A entity to be assembly multiple AssemblableEntity
    """
    def __init__(self):
        pass

    @abc.abstractmethod
    def scavenge_common_data(self, assemblable: AssemblableEntity):
        """
        Instead of setting the common data from each assemblable, get it all from just one
        :param assemblable: a assemblable sample with data in common with all other assemblables of that this assemblies
        :return: 
        """
        pass

    @abc.abstractmethod
    def assembly(self, assemblables_list: [AssemblableEntity]):
        """
        Assemblies multiple assemblable entities into the AssemblerEntity
        :param assemblables_list: a list with AssemblableEntities to be assembly and populate the caller entity
        :return: 
        """
        pass
