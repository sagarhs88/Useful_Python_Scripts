"""
This generator scripts reads the xlsx file (which contains signal URLS to be used for V3M vs V3H compare script) 
and write it in a jason format

"""


from template import *

import xlrd
import re
from collections import OrderedDict


file_location = "E:\Python Script\SIL_SIL_V3H_V3M_Jason_Generator\\edp_sil.xlsx"
workbook = xlrd.open_workbook(file_location)
sheet = workbook.sheet_by_index(0)

data = [[sheet.cell_value(r,c) for c in range (sheet.ncols)] for r in range(sheet.nrows)]


# pport_officila_list = []
# signal_url = []
signal_dictionary = OrderedDict()
num = 0
count = []
cfg_func = ''


def generate_export_urls():
    export_url_list = []
    for pport_official, v in signal_dictionary.items():
        print (pport_official, v)
        signal_url_lists = "\",\n\t\t\t\t\"".join(v)
        export_url_list.append(INDIVIDUAL_SIGNAL.format(**locals()))
    return export_url_list


def write_to_json(file_name, export_url_list):
    with open(file_name, 'w+') as f:
        # f.write("\n".join(export_url_list))
        f.write(EXPORT_TEMPLETE)
        f.write(export_url_list)


for content in data[1:]:
    pport_officilal = (content[5]).strip()
    signal_url = content[6].split('SIM VFB.')[1]

    if content[5] in signal_dictionary:
        # signal_dictionary[content[5]].append(content[6].split('SIM VFB.')[1])
        signal_dictionary[pport_officilal].append(signal_url)
    else:
        # signal_dictionary[content[5]] = [content[6].split('SIM VFB.')[1]]
        signal_dictionary[pport_officilal] = [signal_url]
    count.append(num)
    num = num + 1


if __name__ == '__main__':
    _export_url_list = generate_export_urls()
    _exporter_signal_list = "".join(_export_url_list)
    _signals_complete = SIGNALS_OVERALL.format(exporter_signal_list=_exporter_signal_list)
    # To Remove comma of last object in a string to make a valid JSON
    _parsed_signals_complete = re.sub(r"\},\s*\}", r"}\n\t}", _signals_complete)

    write_to_json('edp_sil_exporter_setup.json', _parsed_signals_complete)


