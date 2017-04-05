from . import rt_ent


class IncentiveEntity(rt_ent.RtEntity):
    def __init__(self, raw_ents=None):
        self.jato_value = ''
        self.take_rate = ''
        self.dealer_contrib_msrp = ''
        self.manuf_contrib_msrp = ''
        self.gov_contrib_msrp = ''
        self.deposit_perc = ''
        self.max_term = ''
        self.interest = ''
        self.start_date = ''
        self.end_date = ''
        self.public_notes = ''
        self.internal_comms = ''
        super().__init__(raw_ents)

    def __str__(self):
        return '|'.join([str(self.vehicle_id), str(self.jato_value), str(self.take_rate), str(self.dealer_contrib_msrp),
                         str(self.manuf_contrib_msrp), str(self.gov_contrib_msrp), 
                         str(self.deposit_perc), str(self.max_term), str(self.interest), str(self.start_date),
                         str(self.end_date), str(self.public_notes), str(self.internal_comms)])

    def _decode_raw_ent(self, raw_ent):
        self.vehicle_id = raw_ent.vehicle_id
        if raw_ent.schema_id == '47002':
            self.jato_value = raw_ent.data_value
        elif raw_ent.schema_id == '47102':
            self.take_rate = raw_ent.data_value
        elif raw_ent.schema_id == '47508':
            self.deposit_perc = raw_ent.data_value
        elif raw_ent.schema_id == '47504':
            self.max_term = raw_ent.data_value
        elif raw_ent.schema_id == '47505':
            self.interest = raw_ent.data_value
        elif raw_ent.schema_id == '45102':
            self.start_date = raw_ent.data_value
        elif raw_ent.schema_id == '45103':
            self.end_date = raw_ent.data_value
        elif raw_ent.schema_id == '51208':
            self.dealer_contrib_msrp = raw_ent.data_value
        elif raw_ent.schema_id == '51209':
            self.manuf_contrib_msrp = raw_ent.data_value
        elif raw_ent.schema_id == '51210':
            self.gov_contrib_msrp = raw_ent.data_value
        elif raw_ent.schema_id == '45204':
            self.public_notes = raw_ent.data_value
        elif raw_ent.schema_id == '45209':
            self.internal_comms = raw_ent.data_value
        else:
            raise NotImplementedError('schema_id ' + raw_ent.schema_id + ' is not implemented')

