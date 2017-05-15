import csv
import io
from . import base


class MsAccessEntity(base.RawEntity):
    """
        Microsoft Access Entity
    """
    def __init__(self, raw_data):
        self._uid = 0
        self._data_date = 0
        super().__init__(raw_data=raw_data)

    @property
    def uid(self):
        return self._uid

    @uid.setter
    def uid(self, value: int):
        if 5 < len(str(value)) < 8:  # Between 6 and 7 digits
            self._uid = value
        else:
            raise ValueError('{} doesnt meet the uid length criteria'.format(str(value)))

    @property
    def data_date(self):
        return self._data_date

    @data_date.setter
    def data_date(self, value: int):
        if base.check_date_format(str(value)):
            self._data_date = value  # check date format
        else:
            raise ValueError('{} doesnt meet the data_date format criteria'.format(str(value)))

    def from_line(self, line: str):
        with io.StringIO(line.strip('\n')) as file_io:
            reader = csv.reader(file_io, delimiter=',')
            for row in reader:
                self.from_iterable(iterable=row)

    def from_iterable(self, iterable):
        raise NotImplementedError()


class CsRtIncentivesEntity(MsAccessEntity):
    """
        Incentives Entity from Microsoft Access TB_CODIFICACAO
    """
    def __init__(self, raw_data):
        self.jato_val = 0.0
        self.take_rate = 0.0
        self.inc_aaaaa = ''
        self.manuf_cont = 0.0
        self.dealer_cont = 0.0
        self._start = 0
        self._end = 0
        self.perc_dep = 0.0
        self.months_pay = 0.0
        self.int_rate = 0.0
        self.public_notes = ''
        self.internal_comments = ''
        super().__init__(raw_data=raw_data)

    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, value: int):
        if base.check_date_format(str(value)):
            if value < self.end:
                self._start = value
            else:
                raise ValueError(
                    'start {} must be between end {}'.format(str(value),
                                                             str(self.data_date)))
        else:
            raise ValueError('{} doesnt meet the start_date criteria'.format(str(value)))

    @property
    def end(self):
        return self._end

    @end.setter
    def end(self, value: int):
        if base.check_date_format(str(value)):
            if self.start <= value:
                self._end = value
            else:
                raise ValueError(
                    'end {} must be higher or equal to start {}'.format(str(value),
                                                                        str(self.start)))
        else:
            raise ValueError('{} doesnt meet the end_date format criteria'.format(str(value)))

    def __str__(self):
        return '|'.join([str(self.uid), str(self.data_date), str(self.jato_val),
                        str(self.inc_aaaaa), str(self.start), str(self.end)])

    def from_line(self, line: str):
        split_line = line.strip('\n').split('|')
        self.uid = int(split_line[0])
        self.data_date = int(split_line[1])
        self.jato_val = float(split_line[2])
        self.take_rate = float(split_line[3])
        self.inc_aaaaa = split_line[4]
        self.manuf_cont = float(split_line[5])
        self.dealer_cont = float(split_line[6])
        self.start = int(split_line[7])
        self.end = int(split_line[8])
        self.perc_dep = float(split_line[9])
        self.months_pay = int(split_line[10])
        self.int_rate = float(split_line[11])
        self.public_notes = split_line[12]
        self.internal_comments = split_line[13]

    def from_iterable(self, iterable):
        self.uid, self.data_date, self.jato_val, self.take_rate, self.inc_aaaaa, self.manuf_cont, self.dealer_cont, \
            self.start, self.end, self.perc_dep, self.months_pay, self.int_rate, self.public_notes, \
            self.internal_comments = iterable


class CsRtTpCompletaEntity(MsAccessEntity):
    """
        Transaction Price Entity Microsoft Access
    """
    def __init__(self, raw_data):
        self.uid = 0
        self.data_date = 0  # %Y%m%d
        self._sample_date = 0  # %Y%m%d
        self._transaction_price = 0.0
        super().__init__(raw_data=raw_data)

    @property
    def sample_date(self):
        return self._sample_date

    @sample_date.setter
    def sample_date(self, value: int):
        if base.check_date_format(str(value)):
            if value >= self.data_date:
                self._sample_date = value
            else:
                raise ValueError('sample_date {} must be higher or equal to data_date {}'.format(str(value),
                                                                                                 str(self.data_date)))
        else:
            raise ValueError('{} doesnt meet the sample_date format criteria'.format(str(value)))

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
        split_line = line.strip('\n').split('|')
        self.uid = int(split_line[0])
        self.data_date = int(split_line[1])
        self.sample_date = int(split_line[2])
        self.transaction_price = float(split_line[3])

    def from_iterable(self, iterable):
        """
        Set this entity from a iterable
        :param iterable: (uid|data_date, sample_date, transaction_price)
        :return: 
        """
        self.uid, self.data_date, self.sample_date, self.transaction_price = iterable
