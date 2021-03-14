import os

data_directory = "D:\Reports\MFC431TA19_410B_1A_CW09_R04.21.04_normal\Bsigs\day\sil"
temp = os.listdir(data_directory)
for output in [os.path.join(data_directory, output) for output in os.listdir(data_directory)
               if os.path.isfile(os.path.join(data_directory, output))]:
    # replace "TXXXXX" by the task_id for every file
    os.rename(output, output.replace("-m", '_m'))