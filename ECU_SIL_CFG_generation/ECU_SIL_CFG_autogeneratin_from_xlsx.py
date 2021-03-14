# import pandas as pd
# print (pd.__version__)
# file_path = 'C:\Users\uids3923\Desktop\ecu_sil_cfg.xlsx'
# my_sheet = 'Tabelle1'
# df = pd.read_excel(file_path, sheetname=my_sheet)
# data = df.to_dict()
# print(df.head())


import xlrd

SIGNAL_TEMPlATE = r'{brace_open}0: ''\'{signal_url}''\',     1:''\'{signal_url}''\',    ''\'type''\':{signal_type},     \'alias\':''\'{signal_alias}''\',        \'diff\':{signal_tolerance},        \'passRate\': \'{signal_expected_pass_rate}%\',     \'unit\':\'{signal_unit}\'{brace_close},'

SIGNAL_TYPE = {
    'Continous': 0,
    'Discrete': 1
}
file_location = "E:\Python Script\ECU_SIL_CFG_generation\ecu_sil_cfg.xlsx"
workbook = xlrd.open_workbook(file_location)
sheet = workbook.sheet_by_index(0)

data = [[sheet.cell_value(r,c) for c in range (sheet.ncols)] for r in range(sheet.nrows)]

signal_url = []
signal_tolerance = []
signal_type = []
signal_unit = []
signal_expected_pass_rate = []
num = 0
count = []
cfg_func = ''
for content in data[1:]:
    signal_url.append(content[0])
    signal_tolerance.append(content[1])
    signal_type.append(content[2])
    signal_unit.append(content[3])
    signal_expected_pass_rate.append(content[4])
    count.append(num)
    num = num + 1

for i in count:
    sub_cfg = SIGNAL_TEMPlATE.format(brace_open='{', signal_url=signal_url[i], signal_type=SIGNAL_TYPE[signal_type[i]],signal_alias=signal_url[i], signal_unit=signal_unit[i], signal_expected_pass_rate=signal_expected_pass_rate[i], signal_tolerance=signal_tolerance[i],brace_close='}') + '\n'
    cfg_func += sub_cfg

with open('ecu_sil.txt', 'w+') as f:
    f.write(cfg_func)
