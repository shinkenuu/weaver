from ETL.Extract.MsAccess import ents as msAccess_ents
from datetime import datetime


class TpEntity(msAccess_ents.AssembledEntity):
    def __init__(self, raw_ents=None):
        super().__init__()
        self.vehicle_id = 0
        self.sample_date = 0
        self.transaction_price = 0.0
        if raw_ents:
            super().assembly(raw_ents)

    @property
    def vehicle_id(self):
        return self.vehicle_id

    @vehicle_id.setter
    def vehicle_id(self, vehicle_id):
        uid = vehicle_id[-8:]
        data_date = str(vehicle_id).replace(uid, '')
        datetime.strptime(data_date, '%Y%m%d') # check date format
        if 4 < len(uid) < 8 and str.isnumeric(uid): # check uid
            self.vehicle_id = vehicle_id

    @property
    def sample_date(self):
        return self.sample_date

    @sample_date.setter
    def sample_date(self, sample_date):
        datetime.strptime(sample_date, '%Y%m%d') # check date format
        self.sample_date = sample_date

    @property
    def transaction_price(self):
        return self.sample_date

    @transaction_price.setter
    def transaction_price(self, transaction_price):
        self.transaction_price = float(transaction_price)

    def __str__(self):
        return '|'.join([str(self.vehicle_id), str(self.sample_date), str(self.transaction_price)])

    def _decode_raw_ent(self, raw_ent):
        raw_ent.uid = str(int(float(raw_ent.uid))) # get rid of the '.00' that comes from MS Access
        self.vehicle_id = '{0}{1}'.format(raw_ent.uid, raw_ent.data_date)
        self.sample_date = raw_ent.sample_date
        self.transaction_price = raw_ent.transaction_price
