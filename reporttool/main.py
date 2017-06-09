#!/usr/env python3

import argparse
import pymssql

import credential
import warder
from reporttool import ford

_warder = warder.Warder()

REPORT_TYPES_DICT = {
    'ford_inc_equip': ford.EquipmentAndIncentives,
}

REPORT_VIEWS_DICT = {
    'ford_inc_equip': 'select vehicle_id, make, model, version, production_year, model_year, msrp, sample_date, volume,'
                      'value, code, jato_value, take_rate, manuf_contrib_msrp, interest_perc, deposit_perc, max_term, '
                      'internal_comments, public_notes '
                      'from vw_ford_incentive_equipment '
                      'where sample_date between {0} and {1} '
                      'order by make, model, version, production_year, model_year, sample_date, code',
}


def report(report_name: str, min_date: int, max_date: int):
    def retrieve_data():
        cred = credential.get_credential(owner='reporttool', subject='ukvsqlbdrep01')
        with pymssql.connect(host=cred['address'], user=cred['username'], password=cred['password'],
                             database='rt') as conn:
            with conn.cursor() as cursor:
                cursor.execute(REPORT_VIEWS_DICT[report_name].format(str(min_date), str(max_date)))
                return cursor.fetchall()
    try:
        _report = REPORT_TYPES_DICT[report_name](retrieve_data())
        _report.generate_report()
    except Exception as err:
        _warder.ward_error('reporttool', err)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate formatted reports')
    parser.add_argument('report_name', nargs=1, type=str,
                        help='the report to be generated\'s name')
    parser.add_argument('--mindate', nargs=1, type=int,
                        help='yyyymmdd - the minimum date to be considered in the report')
    parser.add_argument('--maxdate', nargs=1, type=int,
                        help='yyyymmdd - the maximum date to be considered in the report')
    args = parser.parse_args()
    report(report_name=args.report_name[0], min_date=args.mindate[0], max_date=args.maxdate[0])
