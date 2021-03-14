
#TODO : generate bsig files for each recording in the bpl file
import xml.etree.ElementTree as ET
import time
import subprocess
import shutil, os
import re
MTS_DEFAULT_ARGS = [ "-norestart" ,"-silent", "-showmaximized", "-pal", "-eab" ]
MTS_CONFIG_ARG = "-lc"
MTS_REC_ARG = "-lr"
MTS_BPL_ARG = "-lb"

PLAY_BATCH = True # upload an entire recording (True) or a snippet (False, also the config file will be changed from BatchPlayerMode=1 to BatchPlayerMode=0 belonging to [MTS Player V2])
# modify for mts run
measapp_path = r"D:\sandboxes\Build\AL_ARS410LO19_07.00.00_INT-1\05_Testing\06_Test_Tools\mts\measapp.exe"
mts_cfg_path = r"D:\sandboxes\Build\AL_ARS410LO19_07.00.00_INT-1\05_Testing\06_Test_Tools\mts_measurement\cfg\algo\joint\ecu_sil_all_sim_joint.cfg"
bpl_path = r"D:\sandboxes\Build\AL_ARS410LO19_07.00.00_INT-1\05_Testing\06_Test_Tools\mts_measurement\cfg\algo\joint\ARS410LO19_SW701_Country_LND.bpl"
#newpath = r"D:\sandboxes\Build\AL_ARS410LO19_07.00.00_INT-1\05_Testing\06_Test_Tools\mts_measurement\log_RESULT"

tree = ET.parse(bpl_path)
root = tree.getroot()
bpl_recs = []

for child in root:
    bpl_recs.append(child.attrib["fileName"])

print "generates bsig files for each recording in the bpl file\n"
print "Total number of recs in bpl file : %s" %len(bpl_recs)
cnt = 0

if PLAY_BATCH:
    for rec_path in bpl_recs:
        cnt +=1
        print "loading rec #%s out of %s: \n %s" %( cnt,len(bpl_recs) ,rec_path )
        mts_arg_list = [ measapp_path ]
        mts_arg_list = mts_arg_list + MTS_DEFAULT_ARGS
        mts_arg_list = mts_arg_list + [ MTS_CONFIG_ARG + mts_cfg_path ]
        mts_arg_list = mts_arg_list + [ MTS_REC_ARG + rec_path ]
        # mts_arg_list = mts_arg_list + [ MTS_BPL_ARG + bpl_path ]

        time.sleep(3)
        tmp_ret_code = subprocess.call( mts_arg_list )
else:
    print "to be done\n"
