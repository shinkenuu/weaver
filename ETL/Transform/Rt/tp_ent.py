#!/usr/bin/env python

from . import rt_ent
from datetime import datetime


class TpEntity(rt_ent.RtEntity):
    def __init__(self, raw_ents=None):
        self._sample_date = 19000101  # yyyMMdd
        self._transaction_price = 0.0
        super().__init__(raw_ents)

    @property
    def vehicle_id(self):
        return self._vehicle_id

    @vehicle_id.setter
    def vehicle_id(self, value):
        data_date = value[-8:]
        datetime.strptime(data_date, '%Y%m%d')  # check date format
        uid = value.replace(data_date, '')
        if 4 < len(uid) < 8 and str.isnumeric(uid):  # check uid
            self._vehicle_id = value

    @property
    def sample_date(self):
        return self._sample_date

    @sample_date.setter
    def sample_date(self, value):
        datetime.strptime(str(value), '%Y%m%d')  # check date format
        self._sample_date = value

    @property
    def transaction_price(self):
        return self._transaction_price

    @transaction_price.setter
    def transaction_price(self, value):
        self._transaction_price = float(value)

    def __str__(self):
        return '|'.join([str(self.vehicle_id), str(self.sample_date), str(self.transaction_price)])

    def _decode_raw_ent(self, raw_ent):
        raw_ent.uid = str(int(float(raw_ent.uid)))  # get rid of the '.00' that comes from MS Access
        self.vehicle_id = '{0}{1}'.format(raw_ent.uid, raw_ent.data_date)
        self.sample_date = raw_ent.sample_date
        self.transaction_price = raw_ent.transaction_price
