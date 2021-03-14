RTE_READ_SIGNAL_TEMPLATE = r"""
Std_ReturnType {stub_name}({return_type} {name})
{{
  // Stub function
  return this.m_rp_{name}.value();
}}"""
ADD_RECEIVE_PORT_TEMPLATE = r"""
AddReceivePort("{name}", {return_type}, &m_rp_{name}, sizeof({return_type}));"""
SETUP_PORTS_FUNCTION_TEMPLATE = r"""
long CSimSwcVDY::SetupPorts(void)
{{
  {code}

  return 0;
}}"""

necessary_stubs = {
    'Rte_Read_rActGearPos_ActGearPos': ('ps_rActGearPos_ActGearPos', 'uint8', 'CAN_FD_MFC_PUBLIC.ADAS_Vehicle_Bus_LRR_CAM_SRRs_MFC500.Gear.ActGearPos'),
    'Rte_Read_rActualGear_ActualGear': ('ps_rActualGear_ActualGear', 'uint8', 'CAN_FD_MFC_PUBLIC.ADAS_Vehicle_Bus_LRR_CAM_SRRs_MFC500.Gear.ActualGear'),
    'Rte_Read_rBrakeActLevel_BrakeActLevel': ('ps_rBrakeActLevel_BrakeActLevel', 'uint16', 'CAN_FD_MFC_PUBLIC.ADAS_Vehicle_Bus_LRR_CAM_SRRs_MFC500.Brake.BrakeActLevel'),
    'Rte_Read_rDriverBraking_DriverBraking': ('ps_rDriverBraking_DriverBraking', 'uint8', 'CAN_FD_MFC_PUBLIC.ADAS_Vehicle_Bus_LRR_CAM_SRRs_MFC500.Brake.DriverBraking'),
    'Rte_Read_rEnvTemp_EnvTemp': ('ps_rEnvTemp_EnvTemp', 'uint8', 'URL'),
    'Rte_Read_rFogLampFront_FogLampFront': ('ps_rFogLampFront_FogLampFront', 'uint8', 'CAN_FD_MFC_PUBLIC.ADAS_Vehicle_Bus_LRR_CAM_SRRs_MFC500.Lights.FogLampFront'),
    'Rte_Read_rFogLampRear_FogLampRear': ('ps_rFogLampRear_FogLampRear', 'uint8', 'CAN_FD_MFC_PUBLIC.ADAS_Vehicle_Bus_LRR_CAM_SRRs_MFC500.Lights.FogLampRear'),
    'Rte_Read_rGasPedalPos_GasPedalPos': ('ps_rGasPedalPos_GasPedalPos', 'uint16', 'CAN_FD_MFC_PUBLIC.ADAS_Vehicle_Bus_LRR_CAM_SRRs_MFC500.GasPedal.GasPedalPos'),
    'Rte_Read_rLatAccel_LatAccel': ('ps_rLatAccel_LatAccel', 'uint16', 'CAN_FD_MFC_PUBLIC.ADAS_Vehicle_Bus_LRR_CAM_SRRs_MFC500.LatAccel.LatAccel'),
    'Rte_Read_rOdometer_Odometer': ('ps_rOdometer_Odometer', 'uint32', 'CAN_FD_MFC_PUBLIC.ADAS_Vehicle_Bus_LRR_CAM_SRRs_MFC500.Tachometer.Odometer'),
    'Rte_Read_rSpeedUnit_SpeedUnit': ('ps_rSpeedUnit_SpeedUnit', 'uint8', 'CAN_FD_MFC_PUBLIC.ADAS_Vehicle_Bus_LRR_CAM_SRRs_MFC500.Tachometer.SpeedUnit'),
    'Rte_Read_rSpeedoSpeed_SpeedoSpeed': ('ps_rSpeedoSpeed_SpeedoSpeed', 'uint16', 'CAN_FD_MFC_PUBLIC.ADAS_Vehicle_Bus_LRR_CAM_SRRs_MFC500.Tachometer.SpeedoSpeed'),
    'Rte_Read_rStWheelAngle_StWheelAngle': ('ps_rStWheelAngle_StWheelAngle', 'uint16', 'CAN_FD_MFC_PUBLIC.ADAS_Vehicle_Bus_LRR_CAM_SRRs_MFC500.StWheeleAngle.StWheelAngle'),
    'Rte_Read_rStateBrakeActLevel_StateBrakeActLevel': ('ps_rStateBrakeActLevel_StateBrakeActLevel', 'uint8', 'CAN_FD_MFC_PUBLIC.ADAS_Vehicle_Bus_LRR_CAM_SRRs_MFC500.Brake.StateBrakeActLevel'),
    'Rte_Read_rStateParkBrake_StateParkBrake': ('ps_rStateParkBrake_StateParkBrake', 'uint8', 'CAN_FD_MFC_PUBLIC.ADAS_Vehicle_Bus_LRR_CAM_SRRs_MFC500.Brake.StateParkBrake'),
    'Rte_Read_rState_ActGearPos_State_ActGearPos': ('ps_rState_ActGearPos_State_ActGearPos', 'uint8', 'CAN_FD_MFC_PUBLIC.ADAS_Vehicle_Bus_LRR_CAM_SRRs_MFC500.Gear.State_ActGearPos'),
    'Rte_Read_rState_GasPedalPos_State_GasPedalPos': ('ps_rState_GasPedalPos_State_GasPedalPos', 'uint8', 'CAN_FD_MFC_PUBLIC.ADAS_Vehicle_Bus_LRR_CAM_SRRs_MFC500.GasPedal.GasPedalPos'),
    'Rte_Read_rState_LatAccel_State_LatAccel': ('ps_rState_LatAccel_State_LatAccel', 'uint8', 'CAN_FD_MFC_PUBLIC.ADAS_Vehicle_Bus_LRR_CAM_SRRs_MFC500.LatAccel.State_LatAccel'),
    'Rte_Read_rState_StWheelAngle_State_StWheelAngle': ('ps_rState_StWheelAngle_State_StWheelAngle', 'uint8', 'CAN_FD_MFC_PUBLIC.ADAS_Vehicle_Bus_LRR_CAM_SRRs_MFC500.StWheeleAngle.State_StWheelAngle'),
    'Rte_Read_rParkBrake_ParkBrake': ('ps_rParkBrake_ParkBrake', 'uint8', 'CAN_FD_MFC_PUBLIC.ADAS_Vehicle_Bus_LRR_CAM_SRRs_MFC500.Brake.ParkBrake'),
    'Rte_Read_rTrailerConnection_TrailerConnection': ('ps_rTrailerConnection_TrailerConnection', 'uint8', 'URL'),
    'Rte_Read_rTurnSignal_TurnSignal': ('ps_rTurnSignal_TurnSignal', 'uint8', 'CAN_FD_MFC_PUBLIC.ADAS_Vehicle_Bus_LRR_CAM_SRRs_MFC500.Lights.TurnSignal'),
    'Rte_Read_rState_VehLongAccelExt_State_VehLongAccelExt': ('ps_rState_VehLongAccelExt_State_VehLongAccelExt', 'uint8', 'CAN_FD_MFC_PUBLIC.ADAS_Vehicle_Bus_LRR_CAM_SRRs_MFC500.VehLongAccel.State_VehLongAccelExt'),
    'Rte_Read_rVehLongAccelExt_VehLongAccelExt': ('ps_rVehLongAccelExt_VehLongAccelExt', 'uint16', 'CAN_FD_MFC_PUBLIC.ADAS_Vehicle_Bus_LRR_CAM_SRRs_MFC500.VehLongAccel.VehLongAccelExt'),
    'Rte_Read_rVehLongDirExt_VehLongDirExt': ('ps_rVehLongDirExt_VehLongDirExt', 'uint8', 'CAN_FD_MFC_PUBLIC.ADAS_Vehicle_Bus_LRR_CAM_SRRs_MFC500.VehVelocity.VehLongDirExt'),
    'Rte_Read_rState_VehVelocity_State_VehVelocity': ('ps_rState_VehVelocity_State_VehVelocity', 'uint8', 'CAN_FD_MFC_PUBLIC.ADAS_Vehicle_Bus_LRR_CAM_SRRs_MFC500.VehVelocity.State_VehVelocity'),
    'Rte_Read_rVehVelocityExt_VehVelocityExt': ('ps_rVehVelocityExt_VehVelocityExt', 'uint16', 'CAN_FD_MFC_PUBLIC.ADAS_Vehicle_Bus_LRR_CAM_SRRs_MFC500.VehVelocity.VehVelocityExt'),
    'Rte_Read_rState_WhlVelFrLeft_State_WhlVelFrLeft': ('ps_rState_WhlVelFrLeft_State_WhlVelFrLeft', 'uint8', 'CAN_FD_MFC_PUBLIC.ADAS_Vehicle_Bus_LRR_CAM_SRRs_MFC500.WhlVelFr.State_WhlVelFrLeft'),
    'Rte_Read_rWhlVelFrLeft_WhlVelFrLeft': ('ps_rWhlVelFrLeft_WhlVelFrLeft', 'uint16', 'CAN_FD_MFC_PUBLIC.ADAS_Vehicle_Bus_LRR_CAM_SRRs_MFC500.WhlVelFr.WhlVelFrLeft'),
    'Rte_Read_rState_WhlVelFrRight_State_WhlVelFrRight': ('ps_rState_WhlVelFrRight_State_WhlVelFrRight', 'uint8', 'CAN_FD_MFC_PUBLIC.ADAS_Vehicle_Bus_LRR_CAM_SRRs_MFC500.WhlVelFr.State_WhlVelFrRight'),
    'Rte_Read_rWhlVelFrRight_WhlVelFrRight': ('ps_rWhlVelFrRight_WhlVelFrRight', 'uint16', 'CAN_FD_MFC_PUBLIC.ADAS_Vehicle_Bus_LRR_CAM_SRRs_MFC500.WhlVelFr.WhlVelFrRight'),
    'Rte_Read_rState_WhlVelReLeft_State_WhlVelReLeft': ('ps_rState_WhlVelReLeft_State_WhlVelReLeft', 'uint8', 'CAN_FD_MFC_PUBLIC.ADAS_Vehicle_Bus_LRR_CAM_SRRs_MFC500.WhlVelRe.State_WhlVelReLeft'),
    'Rte_Read_rWhlVelReLeft_WhlVelReLeft': ('ps_rWhlVelReLeft_WhlVelReLeft', 'uint16', 'CAN_FD_MFC_PUBLIC.ADAS_Vehicle_Bus_LRR_CAM_SRRs_MFC500.WhlVelRe.WhlVelReLeft'),
    'Rte_Read_rState_WhlVelReRight_State_WhlVelReRight': ('ps_rState_WhlVelReRight_State_WhlVelReRight', 'uint8', 'CAN_FD_MFC_PUBLIC.ADAS_Vehicle_Bus_LRR_CAM_SRRs_MFC500.WhlVelRe.State_WhlVelReRight'),
    'Rte_Read_rWhlVelReRight_WhlVelReRight': ('ps_rWhlVelReRight_WhlVelReRight', 'uint16', 'CAN_FD_MFC_PUBLIC.ADAS_Vehicle_Bus_LRR_CAM_SRRs_MFC500.WhlVelRe.WhlVelReRight'),
    'Rte_Read_rWiperOutParkPos_WiperOutParkPos': ('ps_rWiperOutParkPos_WiperOutParkPos', 'uint8', 'CAN_FD_MFC_PUBLIC.ADAS_Vehicle_Bus_LRR_CAM_SRRs_MFC500.Wiper.WiperOutParkPos'),
    'Rte_Read_rWiperStage_WiperStage': ('ps_rWiperStage_WiperStage', 'uint8', 'CAN_FD_MFC_PUBLIC.ADAS_Vehicle_Bus_LRR_CAM_SRRs_MFC500.Wiper.WiperStage'),
    'Rte_Read_rWiperState_WiperState': ('ps_rWiperState_WiperState', 'uint8', 'CAN_FD_MFC_PUBLIC.ADAS_Vehicle_Bus_LRR_CAM_SRRs_MFC500.Wiper.WiperState'),
    'Rte_Read_rState_YawRate_State_YawRate': ('ps_rState_YawRate_State_YawRate', 'uint8', 'CAN_FD_MFC_PUBLIC.ADAS_Vehicle_Bus_LRR_CAM_SRRs_MFC500.YawRate.State_YawRate'),
    'Rte_Read_rYawRate_YawRate': ('ps_rYawRate_YawRate', 'uint16', 'CAN_FD_MFC_PUBLIC.ADAS_Vehicle_Bus_LRR_CAM_SRRs_MFC500.YawRate.YawRate'),
    'Rte_Read_reHeightLevel_eHeightLevel': ('ps_reHeightLevel_eHeightLevel', 'uint8', 'URL'),
    'Rte_Read_rVehLongMotStateExt_VehLongMotStateExt': ('ps_rVehLongMotStateExt_VehLongMotStateExt', 'uint8', 'CAN_FD_MFC_PUBLIC.ADAS_Vehicle_Bus_LRR_CAM_SRRs_MFC500.VehVelocity.VehLongMotStateExt'),
}

types_mapping = {
    'uint8': 'simUI8_t',
    'uint16': 'simUI16_t',
    'uint32': 'simUI32_t',
}


def generate_file(stubs, setup_ports_function):
    with open("fcu_vdy_stubs.h", 'w+') as f:
        f.write("\n\n".join(stubs))
        f.write("\n\n" + setup_ports_function)


def write_stubs():
    stub_functions = []
    for stub_name, args in necessary_stubs.iteritems():
        name, return_type, url = args
        stub_code = RTE_READ_SIGNAL_TEMPLATE.format(**locals())
        stub_functions.append(stub_code)
    return stub_functions


def write_setup_ports_function():
    code = ""
    for stub_name, args in necessary_stubs.iteritems():
        name, return_type, url = args
        stub_code = ADD_RECEIVE_PORT_TEMPLATE.format(name=name, return_type=types_mapping[return_type])
        code += stub_code
    return SETUP_PORTS_FUNCTION_TEMPLATE.format(code=code)

if __name__ == '__main__':
    stubs = write_stubs()
    setup_ports_function = write_setup_ports_function()
    generate_file(stubs, setup_ports_function)

