#!/usr/bin/env python3


from ETL.Extract.MsAccess import ents as msAccess_ents
from datetime import datetime


class TpEntity(msAccess_ents.AssembledEntity):
    vehicle_id = 0
    delivery_date = 0
    transaction_price = 0

    def __init__(self):
        super(msAccess_ents.AssembledEntity, self).__init__()

    def __str__(self):
        return '|'.join([str(self.vehicle_id), str(self.delivery_date), str(self.transaction_price)])

    def _validate_vehicle_id(self, uid, data_date):
        try:
            datetime.strptime(data_date, '%Y%m%d') # check data_date
            return 4 < len(uid) < 8 and str.isnumeric(uid) # check uid
        except:
            return False

    def _validate_delivery_date(self, delivery_date):
        try:
            datetime.strptime(delivery_date, '%Y%m%d')
            return True
        except:
            return False

    def _validate_transaction_price(self, transaction_price):
        return str.isnumeric(transaction_price)

    def _decode_raw_ent(self, raw_ent):
        raw_ent.uid = int(raw_ent.uid)
        if self._validate_vehicle_id(raw_ent.uid, raw_ent.data_date):
            self.vehicle_id = str.join(raw_ent.uid, raw_ent.data_date)
        if self._validate_delivery_date(raw_ent.delivery_date):
            self.delivery_date = raw_ent.delivery_date
        if self._validate_transaction_price(raw_ent.transaction_price):
            self.transaction_price = raw_ent.transaction_price
