
from etl import extractor
from etl.entities import base as base_ents, cs2002 as cs2002_ents, msaccess as msaccess_ents, rt as rt_ents

READY_FILES_ROOT_DIR_PATH = '/mnt/jatobrfiles/Weaver/etl/ready/'

READY_FILES_PATH_DICT = {
    'mssql|rt.vehicles': '{}rt/vehicles_from_mssql.txt'.format(READY_FILES_ROOT_DIR_PATH),
    'mssql|rt.incentives': '{}rt/incentives_from_mssql.txt'.format(READY_FILES_ROOT_DIR_PATH),
    'msaccess|rt.incentives': '{}rt/incentives_from_msaccess.txt'.format(READY_FILES_ROOT_DIR_PATH),
    'msaccess|rt.tp': '{}rt/tp_from_msaccess.txt'.format(READY_FILES_ROOT_DIR_PATH),
}

READY_TYPES_DICT = {
    'rt.vehicles': rt_ents.VehicleEntity,
    'rt.incentives': rt_ents.IncentiveEntity,
    'rt.tp': rt_ents.TpEntity
}

RAW_TYPES_DICT = {
    'mssql|rt.vehicles': cs2002_ents.Cs2002Entity,
    'mssql|rt.incentives': cs2002_ents.EscbrBrPublicIncentiveEntity,
    'msaccess|rt.incentives': msaccess_ents.CsRtIncentivesEntity,
    'msaccess|rt.tp': msaccess_ents.CsRtTpCompletaEntity
}

EXTRACTED_FILES_DICT = {
    'mssql|rt.vehicles': ('sscbr_cs2002.txt', 'nscbr_cs2002.txt'),
    'mssql|rt.incentives': ('escbr_cs2002_br_public_incentive.txt', ),
    'msaccess|rt.incentives': ('CS_RT_INCENTIVES.txt', ),
    'msaccess|rt.tp': ('CS_RT_TP_COMPLETA.txt', )
}


def transform(into: str, source: str, input_data: list):
    """
    Transforms raw entities into entities ready to bulk insert
    :param into: The final entity. Usage: database.table
    :param source: The data source
    :param input_data: file path or tuple with extracted data
    :return: 
    """
    def from_file(file_path: str, into_raw_type: type):
        ents = []
        with open(file_path, 'r') as file:
            for line in file:
                raw_ent = into_raw_type(raw_data=line)
                ents.append(raw_ent)
        return ents

    def from_memory(read_data: list, into_raw_type: type):
        ents = []
        for data in read_data:
            raw_ent = into_raw_type(raw_data=data)
            ents.append(raw_ent)
        return ents

    def from_raw(raw_ent_list: [base_ents.RawEntity], into_ready_type: type):
        if not raw_ent_list:
            raise IndexError('raw_ent_list must not be empty')
        ready_ents = []
        if isinstance(raw_ent_list[0], base_ents.AssemblableEntity) \
                and isinstance(into_ready_type(), base_ents.AssemblerEntity):
            ents_to_assemble = []
            for assemblable_ent in raw_ent_list:
                # if there is no ent to assembly yet OR if this ent assemblies with the current assemblables
                if len(ents_to_assemble) == 0 or ents_to_assemble[0].assemblies_with(assemblable_ent):
                    ents_to_assemble.append(assemblable_ent)
                else:
                    ready_ent = into_ready_type(raw_ent_list=ents_to_assemble)
                    ready_ents.append(ready_ent)
                    ents_to_assemble.clear()
                    ents_to_assemble.append(assemblable_ent)
        else:
            for raw_ent in raw_ent_list:
                ready_ent = into_ready_type(raw_ent=raw_ent)
                ready_ents.append(ready_ent)
        return ready_ents

    def write_ents_to_disc(ents: list, output_path: str):
        doc = '\n'.join(str(ent) for ent in ents)
        with open(output_path, 'w') as file:
            file.truncate()
            file.write(doc)
        return output_path

    key = '{0}|{1}'.format(source, into)
    if input_data:
        input_data = from_memory(read_data=input_data, into_raw_type=RAW_TYPES_DICT[key])
    else:
        input_data = []
        for necessary_file in EXTRACTED_FILES_DICT[key]:
                input_data.extend(from_file(
                    file_path='{0}{1}/{2}'.format(extractor.EXTRACTED_DIR_PATH, source, necessary_file),
                    into_raw_type=RAW_TYPES_DICT[key]))
    input_data = from_raw(raw_ent_list=input_data, into_ready_type=READY_TYPES_DICT[into])
    return write_ents_to_disc(input_data, READY_FILES_PATH_DICT[key])
