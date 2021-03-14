import os
import shutil
import stat

from ims_project import IMSProject


class CheckoutConfig(object):
    def __init__(self, project_name, ims_project):
        self.project_name = project_name
        self.ims_project = ims_project
        self.resynced_subdirs = []
        self.shortcuts = []
        self.files_to_unlock = []
        self.excluded_filemasks = ['*.pdb', '*.pyo', '*.pyc', '*.h', '*.c']
        self.post_checkout_action = None # accepts sandbox dir and checkpoint name as arguments


def checkout_config_for_project(project):
    if project == IMSProject.MFC431TA19:
        return _checkout_config_for_mfc431(project)

    if project == IMSProject.MFC431LO19:
        return  _checkout_config_for_mfc431_lo19(project)

    if project == IMSProject.AL_ARS510TA19:
        return _checkout_config_for_ars510()


def _checkout_config_for_mfc431(project):
    config = CheckoutConfig(project_name=project.name, ims_project=project.path)
    config.resynced_subdirs = _mfc431_resynced_subdirs()
    config.shortcuts = _mfc431_shortcuts(project)

    config.files_to_unlock = [
        r'MTS/05_Testing/MTS/mts_measurement/cfg/00_Projects/MFC431/GA/input_sync_port_cfg.par',
        r'DPU/05_Testing/05_Test_Environment/Dynamic_Tests/Project_Specific/MFC431/SVT/ecu_sil_custom/cfg/temp.bpl'
    ]

    def ta19_post_checkout_action(sandbox, checkpoint):
        print('>>> Updating SWVersion in ECU SIL report config files')
        test_config_dir = os.path.join(sandbox,
                                       'DPU/05_Testing/05_Test_Environment/Dynamic_Tests/Project_Specific/MFC431/SVT/ecu_sil_custom/cfg')

        for file in os.listdir(test_config_dir):
            ext = os.path.splitext(file)[-1]
            if ext not in ['.cfg', '.bpl']:
                continue

            _replace_string_in_file(os.path.join(test_config_dir, file),
                                    old_str='MFC431TA19_400B_MPT_CW42_05.00.08_special',
                                    new_str=checkpoint)

    config.post_checkout_action = ta19_post_checkout_action if project == IMSProject.MFC431TA19 else None
    return config


def _checkout_config_for_mfc431_lo19(project):
    config = CheckoutConfig(project_name=project.name, ims_project=project.path)
    config.resynced_subdirs = _mfc431_resynced_subdirs()
    config.shortcuts = _mfc431_shortcuts(project)
    config.files_to_unlock = [
        r'MTS/05_Testing/MTS/mts_measurement/cfg/00_Projects/MFC431/GA/input_sync_port_cfg.par'
    ]
    return config


def _mfc431_shortcuts(project):
    return [
        (r'jointsim_cfg.lnk',
         r'MTS/05_Testing/MTS/mts_measurement/cfg/00_Projects/{project}/JOINT'.format(project=project.name)),
        (r'mts_app.lnk', 'MTS/05_Testing/MTS/mts_system/measapp.exe'),
        (r'mts_measurement.lnk', 'MTS/05_Testing/MTS/mts_measurement'),
        (r'report_gen.lnk',
         'DPU/05_Testing/05_Test_Environment/Dynamic_Tests/Project_Specific/MFC431/SVT/ecu_sil_custom')]


def _mfc431_resynced_subdirs():
    return [r'MTS',
            r'DPU/05_Testing/05_Test_Environment/Dynamic_Tests/SVT',
            r'DPU/05_Testing/05_Test_Environment/Dynamic_Tests/Project_Specific/MFC431/SVT']


def _checkout_config_for_ars510():
    project = IMSProject.AL_ARS510TA19
    config = CheckoutConfig(project_name=project.name, ims_project=project.path)
    config.resynced_subdirs = [r'05_Testing/06_Test_Tools/mts_measurement',
                               r'05_Testing/06_Test_Tools/mts']
    config.shortcuts = [(r'jointsim_cfg.lnk', '05_Testing/06_Test_Tools/mts_measurement/cfg/algo/joint'),
                        (r'mts_measurement.lnk', '05_Testing/06_Test_Tools/mts_measurement'),
                        (r'mts_app.lnk', '05_Testing/06_Test_Tools/mts/measapp.exe')]

    def post_checkout_action(sandbox, checkpoint):
        print('>>> Disabling FCT parameter overrule in simulation')
        filepath = os.path.join(sandbox, r'05_Testing\06_Test_Tools\mts_measurement\cfg\algo\fct\fct_parameter.par')
        _replace_string_in_file(filepath, old_str='[Sim_OverruleEnable].Value=1',
                                new_str='[Sim_OverruleEnable].Value=0')

    config.post_checkout_action = post_checkout_action
    return config


def _replace_string_in_file(filepath, old_str, new_str):
    with open(filepath, 'r') as src, open(filepath + '.upd', 'w') as dst:
        for line in src:
            dst.write(line.replace(old_str, new_str))

    os.chmod(filepath, stat.S_IWRITE)
    os.remove(filepath)
    shutil.move(filepath + '.upd', filepath)


