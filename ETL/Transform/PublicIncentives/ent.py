#!/usr/bin/env python3


from ETL.Extract.CS_2002 import ents as cs_2002_ents


class IncentiveEntity(cs_2002_ents.AssembledEntity):
    vehicle_id = 0
    jato_value = ''
    take_rate = ''
    dealer_contrib_msrp = ''
    manuf_contrib_msrp = ''
    gov_contrib_msrp = ''
    deposit_perc = ''
    max_term = ''
    interest = ''
    start_date = ''
    end_date = ''
    public_notes = ''
    internal_comms = ''

    def __init__(self):
        super(cs_2002_ents.AssembledEntity, self).__init__()

    def __str__(self):
        return '|'.join([str(self.vehicle_id), str(self.jato_value), str(self.take_rate), str(self.dealer_contrib_msrp),
                         str(self.manuf_contrib_msrp), str(self.gov_contrib_msrp), 
                         str(self.deposit_perc), str(self.max_term), str(self.interest), str(self.start_date),
                         str(self.end_date), str(self.public_notes), str(self.internal_comms) + "'"])

    def _decode_result(self, result):
        self.vehicle_id = result.vehicle_id
        if result.schema_id == '47002':
            self.jato_value = result.data_value
        elif result.schema_id == '47102':
            self.take_rate = result.data_value
        elif result.schema_id == '47508':
            self.deposit_perc = result.data_value
        elif result.schema_id == '47504':
            self.max_term = result.data_value
        elif result.schema_id == '47505':
            self.interest = result.data_value
        elif result.schema_id == '45102':
            self.start_date = result.data_value
        elif result.schema_id == '45103':
            self.end_date = result.data_value
        elif result.schema_id == '51208':
            self.dealer_contrib_msrp = result.data_value
        elif result.schema_id == '51209':
            self.manuf_contrib_msrp = result.data_value
        elif result.schema_id == '51210':
            self.gov_contrib_msrp = result.data_value
        elif result.schema_id == '45204':
            self.public_notes = result.data_value
        elif result.schema_id == '45209':
            self.internal_comms = result.data_value
        else:
            raise NotImplementedError('schema_id ' + result.schema_id + ' is not implemented')

