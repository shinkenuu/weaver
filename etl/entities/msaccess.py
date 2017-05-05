import csv
import io
from . import base


class MsAccessEntity(base.RawEntity):
    """
        Microsoft Access Entity
    """
    def __init__(self, raw_data):
        self._uid = 0
        self._data_date = 19000101
        super().__init__(raw_data=raw_data)

    @property
    def uid(self):
        return self._uid

    @uid.setter
    def uid(self, value: int):
        if 5 < len(str(value)) < 8:  # Between 6 and 7 digits
            self._uid = value
        else:
            raise ValueError('{} doesnt meet the uid criteria')

    @property
    def data_date(self):
        return self._data_date

    @data_date.setter
    def data_date(self, value: int):
        if base.check_date_format(str(value)):
            self._data_date = value  # check date format
        else:
            raise ValueError('{} doesnt meet the data_date format criteria')

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
            self._start = value
        else:
            raise ValueError('{} doesnt meet the start_date criteria')

    @property
    def end(self):
        return self._end

    @end.setter
    def end(self, value: int):
        if base.check_date_format(str(value)):
            self._end = value
        else:
            raise ValueError('{} doesnt meet the end_date format criteria')

    def __str__(self):
        return '|'.join([str(self.uid), str(self.data_date), str(self.jato_val),
                        str(self.inc_aaaaa), str(self.start), str(self.end)])

    def from_line(self, line: str):
        super().from_line(line=line)

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
