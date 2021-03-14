import os

data_directory = "E:\Sandboxes\Build_SBs\SIL_SIL_MFC431TA19_402B_MPT_CW04_05.10.03_normal\MTS\\05_Testing\MTS\mts_measurement\data\sil"
temp = os.listdir(data_directory)
for output in [os.path.join(data_directory, output) for output in os.listdir(data_directory)
               if os.path.isfile(os.path.join(data_directory, output))]:
    # replace "TXXXXX" by the task_id for every file
    os.rename(output, output.replace("-m", '_m'))