from templates import *

# This has been semi-automatically extracted from FCU_VDY.c (method FCU_IPC_e_CL_IUC_VEHICLE_SIGNALS)
# The dictionary includes the following information:
#  Key: Name of the method FCU calls
#  Value 1: BUS interface name
#  Value 2: BUS interface type
#  Value 3: BUS interface CBD (or is it CDL?) URL
necessary_stubs = {
    'Rte_Read_FCU_rActGearPos_ActGearPos': ('ps_rActGearPos_ActGearPos', 'uint8', 'CAN_FD_MFC_PUBLIC.ADAS_Vehicle_Bus_LRR_CAM_SRRs_MFC500.Gear.ActGearPos'),
    'Rte_Read_FCU_rActualGear_ActualGear': ('ps_rActualGear_ActualGear', 'uint8', 'CAN_FD_MFC_PUBLIC.ADAS_Vehicle_Bus_LRR_CAM_SRRs_MFC500.Gear.ActualGear'),
    'Rte_Read_FCU_rBrakeActLevel_BrakeActLevel': ('ps_rBrakeActLevel_BrakeActLevel', 'uint16', 'CAN_FD_MFC_PUBLIC.ADAS_Vehicle_Bus_LRR_CAM_SRRs_MFC500.Brake.BrakeActLevel'),
    'Rte_Read_FCU_rDriverBraking_DriverBraking': ('ps_rDriverBraking_DriverBraking', 'uint8', 'CAN_FD_MFC_PUBLIC.ADAS_Vehicle_Bus_LRR_CAM_SRRs_MFC500.Brake.DriverBraking'),
    'Rte_Read_FCU_rEnvTemp_EnvTemp': ('ps_rEnvTemp_EnvTemp', 'uint8', 'URL'),
    'Rte_Read_FCU_rFogLampFront_FogLampFront': ('ps_rFogLampFront_FogLampFront', 'uint8', 'CAN_FD_MFC_PUBLIC.ADAS_Vehicle_Bus_LRR_CAM_SRRs_MFC500.Lights.FogLampFront'),
    'Rte_Read_FCU_rFogLampRear_FogLampRear': ('ps_rFogLampRear_FogLampRear', 'uint8', 'CAN_FD_MFC_PUBLIC.ADAS_Vehicle_Bus_LRR_CAM_SRRs_MFC500.Lights.FogLampRear'),
    'Rte_Read_FCU_rGasPedalPos_GasPedalPos': ('ps_rGasPedalPos_GasPedalPos', 'uint16', 'CAN_FD_MFC_PUBLIC.ADAS_Vehicle_Bus_LRR_CAM_SRRs_MFC500.GasPedal.GasPedalPos'),
    'Rte_Read_FCU_rLatAccel_LatAccel': ('ps_rLatAccel_LatAccel', 'uint16', 'CAN_FD_MFC_PUBLIC.ADAS_Vehicle_Bus_LRR_CAM_SRRs_MFC500.LatAccel.LatAccel'),
    'Rte_Read_FCU_rOdometer_Odometer': ('ps_rOdometer_Odometer', 'uint32', 'CAN_FD_MFC_PUBLIC.ADAS_Vehicle_Bus_LRR_CAM_SRRs_MFC500.Tachometer.Odometer'),
    'Rte_Read_FCU_rSpeedUnit_SpeedUnit': ('ps_rSpeedUnit_SpeedUnit', 'uint8', 'CAN_FD_MFC_PUBLIC.ADAS_Vehicle_Bus_LRR_CAM_SRRs_MFC500.Tachometer.SpeedUnit'),
    'Rte_Read_FCU_rSpeedoSpeed_SpeedoSpeed': ('ps_rSpeedoSpeed_SpeedoSpeed', 'uint16', 'CAN_FD_MFC_PUBLIC.ADAS_Vehicle_Bus_LRR_CAM_SRRs_MFC500.Tachometer.SpeedoSpeed'),
    'Rte_Read_FCU_rStWheelAngle_StWheelAngle': ('ps_rStWheelAngle_StWheelAngle', 'uint16', 'CAN_FD_MFC_PUBLIC.ADAS_Vehicle_Bus_LRR_CAM_SRRs_MFC500.StWheeleAngle.StWheelAngle'),
    'Rte_Read_FCU_rStateBrakeActLevel_StateBrakeActLevel': ('ps_rStateBrakeActLevel_StateBrakeActLevel', 'uint8', 'CAN_FD_MFC_PUBLIC.ADAS_Vehicle_Bus_LRR_CAM_SRRs_MFC500.Brake.StateBrakeActLevel'),
    'Rte_Read_FCU_rStateParkBrake_StateParkBrake': ('ps_rStateParkBrake_StateParkBrake', 'uint8', 'CAN_FD_MFC_PUBLIC.ADAS_Vehicle_Bus_LRR_CAM_SRRs_MFC500.Brake.StateParkBrake'),
    'Rte_Read_FCU_rState_ActGearPos_State_ActGearPos': ('ps_rState_ActGearPos_State_ActGearPos', 'uint8', 'CAN_FD_MFC_PUBLIC.ADAS_Vehicle_Bus_LRR_CAM_SRRs_MFC500.Gear.State_ActGearPos'),
    'Rte_Read_FCU_rState_GasPedalPos_State_GasPedalPos': ('ps_rState_GasPedalPos_State_GasPedalPos', 'uint8', 'CAN_FD_MFC_PUBLIC.ADAS_Vehicle_Bus_LRR_CAM_SRRs_MFC500.GasPedal.GasPedalPos'),
    'Rte_Read_FCU_rState_LatAccel_State_LatAccel': ('ps_rState_LatAccel_State_LatAccel', 'uint8', 'CAN_FD_MFC_PUBLIC.ADAS_Vehicle_Bus_LRR_CAM_SRRs_MFC500.LatAccel.State_LatAccel'),
    'Rte_Read_FCU_rState_StWheelAngle_State_StWheelAngle': ('ps_rState_StWheelAngle_State_StWheelAngle', 'uint8', 'CAN_FD_MFC_PUBLIC.ADAS_Vehicle_Bus_LRR_CAM_SRRs_MFC500.StWheeleAngle.State_StWheelAngle'),
    'Rte_Read_FCU_rParkBrake_ParkBrake': ('ps_rParkBrake_ParkBrake', 'uint8', 'CAN_FD_MFC_PUBLIC.ADAS_Vehicle_Bus_LRR_CAM_SRRs_MFC500.Brake.ParkBrake'),
    'Rte_Read_FCU_rTrailerConnection_TrailerConnection': ('ps_rTrailerConnection_TrailerConnection', 'uint8', 'URL'),
    'Rte_Read_FCU_rTurnSignal_TurnSignal': ('ps_rTurnSignal_TurnSignal', 'uint8', 'CAN_FD_MFC_PUBLIC.ADAS_Vehicle_Bus_LRR_CAM_SRRs_MFC500.Lights.TurnSignal'),
    'Rte_Read_FCU_rState_VehLongAccelExt_State_VehLongAccelExt': ('ps_rState_VehLongAccelExt_State_VehLongAccelExt', 'uint8', 'CAN_FD_MFC_PUBLIC.ADAS_Vehicle_Bus_LRR_CAM_SRRs_MFC500.VehLongAccel.State_VehLongAccelExt'),
    'Rte_Read_FCU_rVehLongAccelExt_VehLongAccelExt': ('ps_rVehLongAccelExt_VehLongAccelExt', 'uint16', 'CAN_FD_MFC_PUBLIC.ADAS_Vehicle_Bus_LRR_CAM_SRRs_MFC500.VehLongAccel.VehLongAccelExt'),
    'Rte_Read_FCU_rVehLongDirExt_VehLongDirExt': ('ps_rVehLongDirExt_VehLongDirExt', 'uint8', 'CAN_FD_MFC_PUBLIC.ADAS_Vehicle_Bus_LRR_CAM_SRRs_MFC500.VehVelocity.VehLongDirExt'),
    'Rte_Read_FCU_rState_VehVelocity_State_VehVelocity': ('ps_rState_VehVelocity_State_VehVelocity', 'uint8', 'CAN_FD_MFC_PUBLIC.ADAS_Vehicle_Bus_LRR_CAM_SRRs_MFC500.VehVelocity.State_VehVelocity'),
    'Rte_Read_FCU_rVehVelocityExt_VehVelocityExt': ('ps_rVehVelocityExt_VehVelocityExt', 'uint16', 'CAN_FD_MFC_PUBLIC.ADAS_Vehicle_Bus_LRR_CAM_SRRs_MFC500.VehVelocity.VehVelocityExt'),
    'Rte_Read_FCU_rState_WhlVelFrLeft_State_WhlVelFrLeft': ('ps_rState_WhlVelFrLeft_State_WhlVelFrLeft', 'uint8', 'CAN_FD_MFC_PUBLIC.ADAS_Vehicle_Bus_LRR_CAM_SRRs_MFC500.WhlVelFr.State_WhlVelFrLeft'),
    'Rte_Read_FCU_rWhlVelFrLeft_WhlVelFrLeft': ('ps_rWhlVelFrLeft_WhlVelFrLeft', 'uint16', 'CAN_FD_MFC_PUBLIC.ADAS_Vehicle_Bus_LRR_CAM_SRRs_MFC500.WhlVelFr.WhlVelFrLeft'),
    'Rte_Read_FCU_rState_WhlVelFrRight_State_WhlVelFrRight': ('ps_rState_WhlVelFrRight_State_WhlVelFrRight', 'uint8', 'CAN_FD_MFC_PUBLIC.ADAS_Vehicle_Bus_LRR_CAM_SRRs_MFC500.WhlVelFr.State_WhlVelFrRight'),
    'Rte_Read_FCU_rWhlVelFrRight_WhlVelFrRight': ('ps_rWhlVelFrRight_WhlVelFrRight', 'uint16', 'CAN_FD_MFC_PUBLIC.ADAS_Vehicle_Bus_LRR_CAM_SRRs_MFC500.WhlVelFr.WhlVelFrRight'),
    'Rte_Read_FCU_rState_WhlVelReLeft_State_WhlVelReLeft': ('ps_rState_WhlVelReLeft_State_WhlVelReLeft', 'uint8', 'CAN_FD_MFC_PUBLIC.ADAS_Vehicle_Bus_LRR_CAM_SRRs_MFC500.WhlVelRe.State_WhlVelReLeft'),
    'Rte_Read_FCU_rWhlVelReLeft_WhlVelReLeft': ('ps_rWhlVelReLeft_WhlVelReLeft', 'uint16', 'CAN_FD_MFC_PUBLIC.ADAS_Vehicle_Bus_LRR_CAM_SRRs_MFC500.WhlVelRe.WhlVelReLeft'),
    'Rte_Read_FCU_rState_WhlVelReRight_State_WhlVelReRight': ('ps_rState_WhlVelReRight_State_WhlVelReRight', 'uint8', 'CAN_FD_MFC_PUBLIC.ADAS_Vehicle_Bus_LRR_CAM_SRRs_MFC500.WhlVelRe.State_WhlVelReRight'),
    'Rte_Read_FCU_rWhlVelReRight_WhlVelReRight': ('ps_rWhlVelReRight_WhlVelReRight', 'uint16', 'CAN_FD_MFC_PUBLIC.ADAS_Vehicle_Bus_LRR_CAM_SRRs_MFC500.WhlVelRe.WhlVelReRight'),
    'Rte_Read_FCU_rWiperOutParkPos_WiperOutParkPos': ('ps_rWiperOutParkPos_WiperOutParkPos', 'uint8', 'CAN_FD_MFC_PUBLIC.ADAS_Vehicle_Bus_LRR_CAM_SRRs_MFC500.Wiper.WiperOutParkPos'),
    'Rte_Read_FCU_rWiperStage_WiperStage': ('ps_rWiperStage_WiperStage', 'uint8', 'CAN_FD_MFC_PUBLIC.ADAS_Vehicle_Bus_LRR_CAM_SRRs_MFC500.Wiper.WiperStage'),
    'Rte_Read_FCU_rWiperState_WiperState': ('ps_rWiperState_WiperState', 'uint8', 'CAN_FD_MFC_PUBLIC.ADAS_Vehicle_Bus_LRR_CAM_SRRs_MFC500.Wiper.WiperState'),
    'Rte_Read_FCU_rState_YawRate_State_YawRate': ('ps_rState_YawRate_State_YawRate', 'uint8', 'CAN_FD_MFC_PUBLIC.ADAS_Vehicle_Bus_LRR_CAM_SRRs_MFC500.YawRate.State_YawRate'),
    'Rte_Read_FCU_rYawRate_YawRate': ('ps_rYawRate_YawRate', 'uint16', 'CAN_FD_MFC_PUBLIC.ADAS_Vehicle_Bus_LRR_CAM_SRRs_MFC500.YawRate.YawRate'),
    'Rte_Read_FCU_reHeightLevel_eHeightLevel': ('ps_reHeightLevel_eHeightLevel', 'uint8', 'URL'),
    'Rte_Read_FCU_rVehLongMotStateExt_VehLongMotStateExt': ('ps_rVehLongMotStateExt_VehLongMotStateExt', 'uint8', 'CAN_FD_MFC_PUBLIC.ADAS_Vehicle_Bus_LRR_CAM_SRRs_MFC500.VehVelocity.VehLongMotStateExt'),
}

types_mapping = {
    # This list is NOT complete
    # custom type: sim framework type
    'uint8': 'simUI8_t',
    'uint16': 'simUI16_t',
    'uint32': 'simUI32_t',
}


def write_stubs_file(file_name, member_declarations_list, stub_functions_code_list, setup_ports_function_code,
                     # stub_summons_function_code):
                     ):
    with open(file_name, 'w+') as f:
        f.write("\n".join(member_declarations_list))
        f.write("\n")
        f.write("\n\n".join(stub_functions_code_list))
        f.write("\n\n" + setup_ports_function_code)
        f.write("\n\n")
        # f.write(stub_summons_function_code)


def write_simudex_file(file_name, simudex_ports_list):
    with open(file_name, 'w+') as f:
        f.write("\n".join(simudex_ports_list))


def write_fcu_main_call_include_file(file_name, method_name_to_be_called):
    with open(file_name, 'w+') as f:
        f.write("  // Calls the FCU method that converts from BUS to Algo RTE interface (VehSig_t in this case)")
        f.write("\n  {method_name}();\n".format(method_name=method_name_to_be_called))


def generate_ports():
    ports = []
    for _, args in iter(necessary_stubs.items()):
        name, return_type, url = args
        ports.append(SIMUDEX_PRO_PORT_TEMPLATE.format(name=name, sim_data_type=types_mapping[return_type], url=url))

    return ports


def generate_stubs(class_name):
    stub_functions = []
    for stub_name, args in iter(necessary_stubs.items()):
        name, return_type, url = args
        stub_code = RTE_READ_SIGNAL_TEMPLATE.format(**locals())
        stub_functions.append(stub_code)
    return stub_functions


def generate_setup_ports_function(class_name):
    code = ""
    for stub_name, args in iter(necessary_stubs.items()):
        name, return_type, url = args
        stub_code = "  " + ADD_RECEIVE_PORT_TEMPLATE.format(name=name, return_type=types_mapping[return_type]) + "\n"
        code += stub_code
    return SETUP_PORTS_FUNCTION_TEMPLATE.format(class_name=class_name, code=code)


def write_simcon_file(file_name, simcon_connections_list):
    with open(file_name, 'w+') as f:
        f.write(SIMCON_FILE_TEMPLATE.format(connections="\n".join(simcon_connections_list)))


def generate_connections():
    connections = []
    for stub_name, args in iter(necessary_stubs.items()):
        name, _, _ = args
        connections.append(CONNECTION_TEMPLATE.format(name=name))

    return connections


def generate_member_declarations():
    declarations = []
    for _, args in iter(necessary_stubs.items()):
        name, return_type, _ = args
        declarations.append(MEMBER_DECLARATION_TEMPLATE.format(name=name, return_type=return_type))

    return declarations


# def generate_stub_summons_function(class_name):
#     stub_summons = []
#     for stub_name, args in iter(necessary_stubs.items()):
#         name, _, _ = args
#         stub_summons.append("  " + STUB_SUMMON_TEMPLATE.format(stub_name=stub_name, name=name))
#     code = STUB_SUMMONS_FUNCTION_TEMPLATE.format(class_name=class_name, code="\n".join(stub_summons))
#     return code


if __name__ == '__main__':
    COMP_CLASS_NAME = "CSimSwcVDY"
    FCU_METHOD_NAME = "FCU_IPC_e_CL_IUC_VEHICLE_SIGNALS"
    _stub_functions_list = generate_stubs(COMP_CLASS_NAME)
    _setup_ports_function_code = generate_setup_ports_function(COMP_CLASS_NAME)
    _member_declarations_list = generate_member_declarations()
    # _stub_summons_function_code = generate_stub_summons_function(COMP_CLASS_NAME)
    # write_header_file("fcu_vdy_stubs.h", _member_declarations_list, _stub_functions_list, _setup_ports_function_code, _stub_summons_function_code)
    write_stubs_file("fcu_vdy_stubs.h", _member_declarations_list, _stub_functions_list, _setup_ports_function_code)

    write_fcu_main_call_include_file("fcu_vdy_main_call.h", FCU_METHOD_NAME)

    _simudex_ports_list = generate_ports()
    write_simudex_file("fcu_vdy.simudex", _simudex_ports_list)

    _simcon_connections_list = generate_connections()
    write_simcon_file("fcu_vdy.simcon", _simcon_connections_list)

