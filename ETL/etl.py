import os
import warder
from .Extract import raw_ents
from .Transform import transformer
from .Transform.Rt import vehicle_ent, tp_ent, public_inc_ent

_warder = warder.Warder()

dirs_dict = {
    'root': '{}/weaver/etl/'.format(os.path.expanduser('~')),
    'raw': '{}/weaver/etl/raw/'.format(os.path.expanduser('~')),
    'ready': '{}/weaver/etl/ready/'.format(os.path.expanduser('~')),
}

raw_ent_types_dict = {
    'sscbr_cs_2002': raw_ents.Cs2002Entity,
    'nscbr_cs_2002': raw_ents.Cs2002Entity,
    'escbr_cs_2002_br_public_incentive': raw_ents.Cs2002Entity,
    'cs_rt_tp_completa': raw_ents.MsAccessTpEntity,
    'cs_rt_tp_toyota': raw_ents.MsAccessTpEntity
}

ready_ent_types_dict = {
    'rt.vehicles': vehicle_ent.VehicleEntity,
    'rt.incentives': public_inc_ent.IncentiveEntity,
    'rt.tp': tp_ent.TpEntity
}


def etl(command : str, input, target):
    try:
        if command == 'extract':
            raise NotImplementedError('Extraction module of ETL')
        elif command == 'transform':
            transformer.transform(
                into_ent_type=ready_ent_types_dict[target],
                raw_data_file_names=input)
        elif command == 'load':
            raise NotImplementedError('Loading module of ETL')
        else:
            raise NotImplementedError('Invalid command: {}'.format(command))
    except Exception as err:
        _warder.ward_error('etl', err)
