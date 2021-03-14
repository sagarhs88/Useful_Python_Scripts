uint32 m_rp_ps_rOdometer_Odometer;
uint8 m_rp_ps_rEnvTemp_EnvTemp;
uint16 m_rp_ps_rVehVelocityExt_VehVelocityExt;
uint16 m_rp_ps_rVehLongAccelExt_VehLongAccelExt;
uint8 m_rp_ps_rFogLampRear_FogLampRear;
uint16 m_rp_ps_rWhlVelFrRight_WhlVelFrRight;
uint8 m_rp_ps_rState_VehLongAccelExt_State_VehLongAccelExt;
uint16 m_rp_ps_rWhlVelReLeft_WhlVelReLeft;
uint8 m_rp_ps_reHeightLevel_eHeightLevel;
uint16 m_rp_ps_rGasPedalPos_GasPedalPos;
uint8 m_rp_ps_rState_VehVelocity_State_VehVelocity;
uint8 m_rp_ps_rState_ActGearPos_State_ActGearPos;
uint8 m_rp_ps_rActualGear_ActualGear;
uint8 m_rp_ps_rState_YawRate_State_YawRate;
uint8 m_rp_ps_rTrailerConnection_TrailerConnection;
uint16 m_rp_ps_rYawRate_YawRate;
uint8 m_rp_ps_rFogLampFront_FogLampFront;
uint8 m_rp_ps_rState_WhlVelFrLeft_State_WhlVelFrLeft;
uint8 m_rp_ps_rActGearPos_ActGearPos;
uint8 m_rp_ps_rState_WhlVelReLeft_State_WhlVelReLeft;
uint8 m_rp_ps_rVehLongDirExt_VehLongDirExt;
uint8 m_rp_ps_rState_WhlVelReRight_State_WhlVelReRight;
uint8 m_rp_ps_rWiperStage_WiperStage;
uint8 m_rp_ps_rState_GasPedalPos_State_GasPedalPos;
uint8 m_rp_ps_rStateBrakeActLevel_StateBrakeActLevel;
uint16 m_rp_ps_rLatAccel_LatAccel;
uint8 m_rp_ps_rTurnSignal_TurnSignal;
uint16 m_rp_ps_rBrakeActLevel_BrakeActLevel;
uint8 m_rp_ps_rState_WhlVelFrRight_State_WhlVelFrRight;
uint8 m_rp_ps_rState_StWheelAngle_State_StWheelAngle;
uint16 m_rp_ps_rSpeedoSpeed_SpeedoSpeed;
uint8 m_rp_ps_rParkBrake_ParkBrake;
uint16 m_rp_ps_rWhlVelFrLeft_WhlVelFrLeft;
uint8 m_rp_ps_rState_LatAccel_State_LatAccel;
uint8 m_rp_ps_rDriverBraking_DriverBraking;
uint8 m_rp_ps_rVehLongMotStateExt_VehLongMotStateExt;
uint8 m_rp_ps_rSpeedUnit_SpeedUnit;
uint8 m_rp_ps_rWiperState_WiperState;
uint16 m_rp_ps_rStWheelAngle_StWheelAngle;
uint16 m_rp_ps_rWhlVelReRight_WhlVelReRight;
uint8 m_rp_ps_rStateParkBrake_StateParkBrake;
uint8 m_rp_ps_rWiperOutParkPos_WiperOutParkPos;

Std_ReturnType CSimSwcVDY::Rte_Read_FCU_rOdometer_Odometer(uint32 * ps_rOdometer_Odometer)
{
  // Stub function - replaces reading from RTE by reading from a sim plugin request port
  // TODO: Add 'if' clause for the case that there's nothing received (not dirty)
  *ps_rOdometer_Odometer = m_rp_ps_rOdometer_Odometer;
  return RTE_E_OK;
}


Std_ReturnType CSimSwcVDY::Rte_Read_FCU_rEnvTemp_EnvTemp(uint8 * ps_rEnvTemp_EnvTemp)
{
  // Stub function - replaces reading from RTE by reading from a sim plugin request port
  // TODO: Add 'if' clause for the case that there's nothing received (not dirty)
  *ps_rEnvTemp_EnvTemp = m_rp_ps_rEnvTemp_EnvTemp;
  return RTE_E_OK;
}


Std_ReturnType CSimSwcVDY::Rte_Read_FCU_rVehVelocityExt_VehVelocityExt(uint16 * ps_rVehVelocityExt_VehVelocityExt)
{
  // Stub function - replaces reading from RTE by reading from a sim plugin request port
  // TODO: Add 'if' clause for the case that there's nothing received (not dirty)
  *ps_rVehVelocityExt_VehVelocityExt = m_rp_ps_rVehVelocityExt_VehVelocityExt;
  return RTE_E_OK;
}


Std_ReturnType CSimSwcVDY::Rte_Read_FCU_rVehLongAccelExt_VehLongAccelExt(uint16 * ps_rVehLongAccelExt_VehLongAccelExt)
{
  // Stub function - replaces reading from RTE by reading from a sim plugin request port
  // TODO: Add 'if' clause for the case that there's nothing received (not dirty)
  *ps_rVehLongAccelExt_VehLongAccelExt = m_rp_ps_rVehLongAccelExt_VehLongAccelExt;
  return RTE_E_OK;
}


Std_ReturnType CSimSwcVDY::Rte_Read_FCU_rFogLampRear_FogLampRear(uint8 * ps_rFogLampRear_FogLampRear)
{
  // Stub function - replaces reading from RTE by reading from a sim plugin request port
  // TODO: Add 'if' clause for the case that there's nothing received (not dirty)
  *ps_rFogLampRear_FogLampRear = m_rp_ps_rFogLampRear_FogLampRear;
  return RTE_E_OK;
}


Std_ReturnType CSimSwcVDY::Rte_Read_FCU_rWhlVelFrRight_WhlVelFrRight(uint16 * ps_rWhlVelFrRight_WhlVelFrRight)
{
  // Stub function - replaces reading from RTE by reading from a sim plugin request port
  // TODO: Add 'if' clause for the case that there's nothing received (not dirty)
  *ps_rWhlVelFrRight_WhlVelFrRight = m_rp_ps_rWhlVelFrRight_WhlVelFrRight;
  return RTE_E_OK;
}


Std_ReturnType CSimSwcVDY::Rte_Read_FCU_rState_VehLongAccelExt_State_VehLongAccelExt(uint8 * ps_rState_VehLongAccelExt_State_VehLongAccelExt)
{
  // Stub function - replaces reading from RTE by reading from a sim plugin request port
  // TODO: Add 'if' clause for the case that there's nothing received (not dirty)
  *ps_rState_VehLongAccelExt_State_VehLongAccelExt = m_rp_ps_rState_VehLongAccelExt_State_VehLongAccelExt;
  return RTE_E_OK;
}


Std_ReturnType CSimSwcVDY::Rte_Read_FCU_rWhlVelReLeft_WhlVelReLeft(uint16 * ps_rWhlVelReLeft_WhlVelReLeft)
{
  // Stub function - replaces reading from RTE by reading from a sim plugin request port
  // TODO: Add 'if' clause for the case that there's nothing received (not dirty)
  *ps_rWhlVelReLeft_WhlVelReLeft = m_rp_ps_rWhlVelReLeft_WhlVelReLeft;
  return RTE_E_OK;
}


Std_ReturnType CSimSwcVDY::Rte_Read_FCU_reHeightLevel_eHeightLevel(uint8 * ps_reHeightLevel_eHeightLevel)
{
  // Stub function - replaces reading from RTE by reading from a sim plugin request port
  // TODO: Add 'if' clause for the case that there's nothing received (not dirty)
  *ps_reHeightLevel_eHeightLevel = m_rp_ps_reHeightLevel_eHeightLevel;
  return RTE_E_OK;
}


Std_ReturnType CSimSwcVDY::Rte_Read_FCU_rGasPedalPos_GasPedalPos(uint16 * ps_rGasPedalPos_GasPedalPos)
{
  // Stub function - replaces reading from RTE by reading from a sim plugin request port
  // TODO: Add 'if' clause for the case that there's nothing received (not dirty)
  *ps_rGasPedalPos_GasPedalPos = m_rp_ps_rGasPedalPos_GasPedalPos;
  return RTE_E_OK;
}


Std_ReturnType CSimSwcVDY::Rte_Read_FCU_rState_VehVelocity_State_VehVelocity(uint8 * ps_rState_VehVelocity_State_VehVelocity)
{
  // Stub function - replaces reading from RTE by reading from a sim plugin request port
  // TODO: Add 'if' clause for the case that there's nothing received (not dirty)
  *ps_rState_VehVelocity_State_VehVelocity = m_rp_ps_rState_VehVelocity_State_VehVelocity;
  return RTE_E_OK;
}


Std_ReturnType CSimSwcVDY::Rte_Read_FCU_rState_ActGearPos_State_ActGearPos(uint8 * ps_rState_ActGearPos_State_ActGearPos)
{
  // Stub function - replaces reading from RTE by reading from a sim plugin request port
  // TODO: Add 'if' clause for the case that there's nothing received (not dirty)
  *ps_rState_ActGearPos_State_ActGearPos = m_rp_ps_rState_ActGearPos_State_ActGearPos;
  return RTE_E_OK;
}


Std_ReturnType CSimSwcVDY::Rte_Read_FCU_rActualGear_ActualGear(uint8 * ps_rActualGear_ActualGear)
{
  // Stub function - replaces reading from RTE by reading from a sim plugin request port
  // TODO: Add 'if' clause for the case that there's nothing received (not dirty)
  *ps_rActualGear_ActualGear = m_rp_ps_rActualGear_ActualGear;
  return RTE_E_OK;
}


Std_ReturnType CSimSwcVDY::Rte_Read_FCU_rState_YawRate_State_YawRate(uint8 * ps_rState_YawRate_State_YawRate)
{
  // Stub function - replaces reading from RTE by reading from a sim plugin request port
  // TODO: Add 'if' clause for the case that there's nothing received (not dirty)
  *ps_rState_YawRate_State_YawRate = m_rp_ps_rState_YawRate_State_YawRate;
  return RTE_E_OK;
}


Std_ReturnType CSimSwcVDY::Rte_Read_FCU_rTrailerConnection_TrailerConnection(uint8 * ps_rTrailerConnection_TrailerConnection)
{
  // Stub function - replaces reading from RTE by reading from a sim plugin request port
  // TODO: Add 'if' clause for the case that there's nothing received (not dirty)
  *ps_rTrailerConnection_TrailerConnection = m_rp_ps_rTrailerConnection_TrailerConnection;
  return RTE_E_OK;
}


Std_ReturnType CSimSwcVDY::Rte_Read_FCU_rYawRate_YawRate(uint16 * ps_rYawRate_YawRate)
{
  // Stub function - replaces reading from RTE by reading from a sim plugin request port
  // TODO: Add 'if' clause for the case that there's nothing received (not dirty)
  *ps_rYawRate_YawRate = m_rp_ps_rYawRate_YawRate;
  return RTE_E_OK;
}


Std_ReturnType CSimSwcVDY::Rte_Read_FCU_rFogLampFront_FogLampFront(uint8 * ps_rFogLampFront_FogLampFront)
{
  // Stub function - replaces reading from RTE by reading from a sim plugin request port
  // TODO: Add 'if' clause for the case that there's nothing received (not dirty)
  *ps_rFogLampFront_FogLampFront = m_rp_ps_rFogLampFront_FogLampFront;
  return RTE_E_OK;
}


Std_ReturnType CSimSwcVDY::Rte_Read_FCU_rState_WhlVelFrLeft_State_WhlVelFrLeft(uint8 * ps_rState_WhlVelFrLeft_State_WhlVelFrLeft)
{
  // Stub function - replaces reading from RTE by reading from a sim plugin request port
  // TODO: Add 'if' clause for the case that there's nothing received (not dirty)
  *ps_rState_WhlVelFrLeft_State_WhlVelFrLeft = m_rp_ps_rState_WhlVelFrLeft_State_WhlVelFrLeft;
  return RTE_E_OK;
}


Std_ReturnType CSimSwcVDY::Rte_Read_FCU_rActGearPos_ActGearPos(uint8 * ps_rActGearPos_ActGearPos)
{
  // Stub function - replaces reading from RTE by reading from a sim plugin request port
  // TODO: Add 'if' clause for the case that there's nothing received (not dirty)
  *ps_rActGearPos_ActGearPos = m_rp_ps_rActGearPos_ActGearPos;
  return RTE_E_OK;
}


Std_ReturnType CSimSwcVDY::Rte_Read_FCU_rState_WhlVelReLeft_State_WhlVelReLeft(uint8 * ps_rState_WhlVelReLeft_State_WhlVelReLeft)
{
  // Stub function - replaces reading from RTE by reading from a sim plugin request port
  // TODO: Add 'if' clause for the case that there's nothing received (not dirty)
  *ps_rState_WhlVelReLeft_State_WhlVelReLeft = m_rp_ps_rState_WhlVelReLeft_State_WhlVelReLeft;
  return RTE_E_OK;
}


Std_ReturnType CSimSwcVDY::Rte_Read_FCU_rVehLongDirExt_VehLongDirExt(uint8 * ps_rVehLongDirExt_VehLongDirExt)
{
  // Stub function - replaces reading from RTE by reading from a sim plugin request port
  // TODO: Add 'if' clause for the case that there's nothing received (not dirty)
  *ps_rVehLongDirExt_VehLongDirExt = m_rp_ps_rVehLongDirExt_VehLongDirExt;
  return RTE_E_OK;
}


Std_ReturnType CSimSwcVDY::Rte_Read_FCU_rState_WhlVelReRight_State_WhlVelReRight(uint8 * ps_rState_WhlVelReRight_State_WhlVelReRight)
{
  // Stub function - replaces reading from RTE by reading from a sim plugin request port
  // TODO: Add 'if' clause for the case that there's nothing received (not dirty)
  *ps_rState_WhlVelReRight_State_WhlVelReRight = m_rp_ps_rState_WhlVelReRight_State_WhlVelReRight;
  return RTE_E_OK;
}


Std_ReturnType CSimSwcVDY::Rte_Read_FCU_rWiperStage_WiperStage(uint8 * ps_rWiperStage_WiperStage)
{
  // Stub function - replaces reading from RTE by reading from a sim plugin request port
  // TODO: Add 'if' clause for the case that there's nothing received (not dirty)
  *ps_rWiperStage_WiperStage = m_rp_ps_rWiperStage_WiperStage;
  return RTE_E_OK;
}


Std_ReturnType CSimSwcVDY::Rte_Read_FCU_rState_GasPedalPos_State_GasPedalPos(uint8 * ps_rState_GasPedalPos_State_GasPedalPos)
{
  // Stub function - replaces reading from RTE by reading from a sim plugin request port
  // TODO: Add 'if' clause for the case that there's nothing received (not dirty)
  *ps_rState_GasPedalPos_State_GasPedalPos = m_rp_ps_rState_GasPedalPos_State_GasPedalPos;
  return RTE_E_OK;
}


Std_ReturnType CSimSwcVDY::Rte_Read_FCU_rStateBrakeActLevel_StateBrakeActLevel(uint8 * ps_rStateBrakeActLevel_StateBrakeActLevel)
{
  // Stub function - replaces reading from RTE by reading from a sim plugin request port
  // TODO: Add 'if' clause for the case that there's nothing received (not dirty)
  *ps_rStateBrakeActLevel_StateBrakeActLevel = m_rp_ps_rStateBrakeActLevel_StateBrakeActLevel;
  return RTE_E_OK;
}


Std_ReturnType CSimSwcVDY::Rte_Read_FCU_rLatAccel_LatAccel(uint16 * ps_rLatAccel_LatAccel)
{
  // Stub function - replaces reading from RTE by reading from a sim plugin request port
  // TODO: Add 'if' clause for the case that there's nothing received (not dirty)
  *ps_rLatAccel_LatAccel = m_rp_ps_rLatAccel_LatAccel;
  return RTE_E_OK;
}


Std_ReturnType CSimSwcVDY::Rte_Read_FCU_rTurnSignal_TurnSignal(uint8 * ps_rTurnSignal_TurnSignal)
{
  // Stub function - replaces reading from RTE by reading from a sim plugin request port
  // TODO: Add 'if' clause for the case that there's nothing received (not dirty)
  *ps_rTurnSignal_TurnSignal = m_rp_ps_rTurnSignal_TurnSignal;
  return RTE_E_OK;
}


Std_ReturnType CSimSwcVDY::Rte_Read_FCU_rBrakeActLevel_BrakeActLevel(uint16 * ps_rBrakeActLevel_BrakeActLevel)
{
  // Stub function - replaces reading from RTE by reading from a sim plugin request port
  // TODO: Add 'if' clause for the case that there's nothing received (not dirty)
  *ps_rBrakeActLevel_BrakeActLevel = m_rp_ps_rBrakeActLevel_BrakeActLevel;
  return RTE_E_OK;
}


Std_ReturnType CSimSwcVDY::Rte_Read_FCU_rState_WhlVelFrRight_State_WhlVelFrRight(uint8 * ps_rState_WhlVelFrRight_State_WhlVelFrRight)
{
  // Stub function - replaces reading from RTE by reading from a sim plugin request port
  // TODO: Add 'if' clause for the case that there's nothing received (not dirty)
  *ps_rState_WhlVelFrRight_State_WhlVelFrRight = m_rp_ps_rState_WhlVelFrRight_State_WhlVelFrRight;
  return RTE_E_OK;
}


Std_ReturnType CSimSwcVDY::Rte_Read_FCU_rState_StWheelAngle_State_StWheelAngle(uint8 * ps_rState_StWheelAngle_State_StWheelAngle)
{
  // Stub function - replaces reading from RTE by reading from a sim plugin request port
  // TODO: Add 'if' clause for the case that there's nothing received (not dirty)
  *ps_rState_StWheelAngle_State_StWheelAngle = m_rp_ps_rState_StWheelAngle_State_StWheelAngle;
  return RTE_E_OK;
}


Std_ReturnType CSimSwcVDY::Rte_Read_FCU_rSpeedoSpeed_SpeedoSpeed(uint16 * ps_rSpeedoSpeed_SpeedoSpeed)
{
  // Stub function - replaces reading from RTE by reading from a sim plugin request port
  // TODO: Add 'if' clause for the case that there's nothing received (not dirty)
  *ps_rSpeedoSpeed_SpeedoSpeed = m_rp_ps_rSpeedoSpeed_SpeedoSpeed;
  return RTE_E_OK;
}


Std_ReturnType CSimSwcVDY::Rte_Read_FCU_rParkBrake_ParkBrake(uint8 * ps_rParkBrake_ParkBrake)
{
  // Stub function - replaces reading from RTE by reading from a sim plugin request port
  // TODO: Add 'if' clause for the case that there's nothing received (not dirty)
  *ps_rParkBrake_ParkBrake = m_rp_ps_rParkBrake_ParkBrake;
  return RTE_E_OK;
}


Std_ReturnType CSimSwcVDY::Rte_Read_FCU_rWhlVelFrLeft_WhlVelFrLeft(uint16 * ps_rWhlVelFrLeft_WhlVelFrLeft)
{
  // Stub function - replaces reading from RTE by reading from a sim plugin request port
  // TODO: Add 'if' clause for the case that there's nothing received (not dirty)
  *ps_rWhlVelFrLeft_WhlVelFrLeft = m_rp_ps_rWhlVelFrLeft_WhlVelFrLeft;
  return RTE_E_OK;
}


Std_ReturnType CSimSwcVDY::Rte_Read_FCU_rState_LatAccel_State_LatAccel(uint8 * ps_rState_LatAccel_State_LatAccel)
{
  // Stub function - replaces reading from RTE by reading from a sim plugin request port
  // TODO: Add 'if' clause for the case that there's nothing received (not dirty)
  *ps_rState_LatAccel_State_LatAccel = m_rp_ps_rState_LatAccel_State_LatAccel;
  return RTE_E_OK;
}


Std_ReturnType CSimSwcVDY::Rte_Read_FCU_rDriverBraking_DriverBraking(uint8 * ps_rDriverBraking_DriverBraking)
{
  // Stub function - replaces reading from RTE by reading from a sim plugin request port
  // TODO: Add 'if' clause for the case that there's nothing received (not dirty)
  *ps_rDriverBraking_DriverBraking = m_rp_ps_rDriverBraking_DriverBraking;
  return RTE_E_OK;
}


Std_ReturnType CSimSwcVDY::Rte_Read_FCU_rVehLongMotStateExt_VehLongMotStateExt(uint8 * ps_rVehLongMotStateExt_VehLongMotStateExt)
{
  // Stub function - replaces reading from RTE by reading from a sim plugin request port
  // TODO: Add 'if' clause for the case that there's nothing received (not dirty)
  *ps_rVehLongMotStateExt_VehLongMotStateExt = m_rp_ps_rVehLongMotStateExt_VehLongMotStateExt;
  return RTE_E_OK;
}


Std_ReturnType CSimSwcVDY::Rte_Read_FCU_rSpeedUnit_SpeedUnit(uint8 * ps_rSpeedUnit_SpeedUnit)
{
  // Stub function - replaces reading from RTE by reading from a sim plugin request port
  // TODO: Add 'if' clause for the case that there's nothing received (not dirty)
  *ps_rSpeedUnit_SpeedUnit = m_rp_ps_rSpeedUnit_SpeedUnit;
  return RTE_E_OK;
}


Std_ReturnType CSimSwcVDY::Rte_Read_FCU_rWiperState_WiperState(uint8 * ps_rWiperState_WiperState)
{
  // Stub function - replaces reading from RTE by reading from a sim plugin request port
  // TODO: Add 'if' clause for the case that there's nothing received (not dirty)
  *ps_rWiperState_WiperState = m_rp_ps_rWiperState_WiperState;
  return RTE_E_OK;
}


Std_ReturnType CSimSwcVDY::Rte_Read_FCU_rStWheelAngle_StWheelAngle(uint16 * ps_rStWheelAngle_StWheelAngle)
{
  // Stub function - replaces reading from RTE by reading from a sim plugin request port
  // TODO: Add 'if' clause for the case that there's nothing received (not dirty)
  *ps_rStWheelAngle_StWheelAngle = m_rp_ps_rStWheelAngle_StWheelAngle;
  return RTE_E_OK;
}


Std_ReturnType CSimSwcVDY::Rte_Read_FCU_rWhlVelReRight_WhlVelReRight(uint16 * ps_rWhlVelReRight_WhlVelReRight)
{
  // Stub function - replaces reading from RTE by reading from a sim plugin request port
  // TODO: Add 'if' clause for the case that there's nothing received (not dirty)
  *ps_rWhlVelReRight_WhlVelReRight = m_rp_ps_rWhlVelReRight_WhlVelReRight;
  return RTE_E_OK;
}


Std_ReturnType CSimSwcVDY::Rte_Read_FCU_rStateParkBrake_StateParkBrake(uint8 * ps_rStateParkBrake_StateParkBrake)
{
  // Stub function - replaces reading from RTE by reading from a sim plugin request port
  // TODO: Add 'if' clause for the case that there's nothing received (not dirty)
  *ps_rStateParkBrake_StateParkBrake = m_rp_ps_rStateParkBrake_StateParkBrake;
  return RTE_E_OK;
}


Std_ReturnType CSimSwcVDY::Rte_Read_FCU_rWiperOutParkPos_WiperOutParkPos(uint8 * ps_rWiperOutParkPos_WiperOutParkPos)
{
  // Stub function - replaces reading from RTE by reading from a sim plugin request port
  // TODO: Add 'if' clause for the case that there's nothing received (not dirty)
  *ps_rWiperOutParkPos_WiperOutParkPos = m_rp_ps_rWiperOutParkPos_WiperOutParkPos;
  return RTE_E_OK;
}


long CSimSwcVDY::SetupPortsFcu(void)
{
  AddReceivePort("ps_rOdometer_Odometer", simUI32_t, &m_rp_ps_rOdometer_Odometer, sizeof(simUI32_t));
  AddReceivePort("ps_rEnvTemp_EnvTemp", simUI8_t, &m_rp_ps_rEnvTemp_EnvTemp, sizeof(simUI8_t));
  AddReceivePort("ps_rVehVelocityExt_VehVelocityExt", simUI16_t, &m_rp_ps_rVehVelocityExt_VehVelocityExt, sizeof(simUI16_t));
  AddReceivePort("ps_rVehLongAccelExt_VehLongAccelExt", simUI16_t, &m_rp_ps_rVehLongAccelExt_VehLongAccelExt, sizeof(simUI16_t));
  AddReceivePort("ps_rFogLampRear_FogLampRear", simUI8_t, &m_rp_ps_rFogLampRear_FogLampRear, sizeof(simUI8_t));
  AddReceivePort("ps_rWhlVelFrRight_WhlVelFrRight", simUI16_t, &m_rp_ps_rWhlVelFrRight_WhlVelFrRight, sizeof(simUI16_t));
  AddReceivePort("ps_rState_VehLongAccelExt_State_VehLongAccelExt", simUI8_t, &m_rp_ps_rState_VehLongAccelExt_State_VehLongAccelExt, sizeof(simUI8_t));
  AddReceivePort("ps_rWhlVelReLeft_WhlVelReLeft", simUI16_t, &m_rp_ps_rWhlVelReLeft_WhlVelReLeft, sizeof(simUI16_t));
  AddReceivePort("ps_reHeightLevel_eHeightLevel", simUI8_t, &m_rp_ps_reHeightLevel_eHeightLevel, sizeof(simUI8_t));
  AddReceivePort("ps_rGasPedalPos_GasPedalPos", simUI16_t, &m_rp_ps_rGasPedalPos_GasPedalPos, sizeof(simUI16_t));
  AddReceivePort("ps_rState_VehVelocity_State_VehVelocity", simUI8_t, &m_rp_ps_rState_VehVelocity_State_VehVelocity, sizeof(simUI8_t));
  AddReceivePort("ps_rState_ActGearPos_State_ActGearPos", simUI8_t, &m_rp_ps_rState_ActGearPos_State_ActGearPos, sizeof(simUI8_t));
  AddReceivePort("ps_rActualGear_ActualGear", simUI8_t, &m_rp_ps_rActualGear_ActualGear, sizeof(simUI8_t));
  AddReceivePort("ps_rState_YawRate_State_YawRate", simUI8_t, &m_rp_ps_rState_YawRate_State_YawRate, sizeof(simUI8_t));
  AddReceivePort("ps_rTrailerConnection_TrailerConnection", simUI8_t, &m_rp_ps_rTrailerConnection_TrailerConnection, sizeof(simUI8_t));
  AddReceivePort("ps_rYawRate_YawRate", simUI16_t, &m_rp_ps_rYawRate_YawRate, sizeof(simUI16_t));
  AddReceivePort("ps_rFogLampFront_FogLampFront", simUI8_t, &m_rp_ps_rFogLampFront_FogLampFront, sizeof(simUI8_t));
  AddReceivePort("ps_rState_WhlVelFrLeft_State_WhlVelFrLeft", simUI8_t, &m_rp_ps_rState_WhlVelFrLeft_State_WhlVelFrLeft, sizeof(simUI8_t));
  AddReceivePort("ps_rActGearPos_ActGearPos", simUI8_t, &m_rp_ps_rActGearPos_ActGearPos, sizeof(simUI8_t));
  AddReceivePort("ps_rState_WhlVelReLeft_State_WhlVelReLeft", simUI8_t, &m_rp_ps_rState_WhlVelReLeft_State_WhlVelReLeft, sizeof(simUI8_t));
  AddReceivePort("ps_rVehLongDirExt_VehLongDirExt", simUI8_t, &m_rp_ps_rVehLongDirExt_VehLongDirExt, sizeof(simUI8_t));
  AddReceivePort("ps_rState_WhlVelReRight_State_WhlVelReRight", simUI8_t, &m_rp_ps_rState_WhlVelReRight_State_WhlVelReRight, sizeof(simUI8_t));
  AddReceivePort("ps_rWiperStage_WiperStage", simUI8_t, &m_rp_ps_rWiperStage_WiperStage, sizeof(simUI8_t));
  AddReceivePort("ps_rState_GasPedalPos_State_GasPedalPos", simUI8_t, &m_rp_ps_rState_GasPedalPos_State_GasPedalPos, sizeof(simUI8_t));
  AddReceivePort("ps_rStateBrakeActLevel_StateBrakeActLevel", simUI8_t, &m_rp_ps_rStateBrakeActLevel_StateBrakeActLevel, sizeof(simUI8_t));
  AddReceivePort("ps_rLatAccel_LatAccel", simUI16_t, &m_rp_ps_rLatAccel_LatAccel, sizeof(simUI16_t));
  AddReceivePort("ps_rTurnSignal_TurnSignal", simUI8_t, &m_rp_ps_rTurnSignal_TurnSignal, sizeof(simUI8_t));
  AddReceivePort("ps_rBrakeActLevel_BrakeActLevel", simUI16_t, &m_rp_ps_rBrakeActLevel_BrakeActLevel, sizeof(simUI16_t));
  AddReceivePort("ps_rState_WhlVelFrRight_State_WhlVelFrRight", simUI8_t, &m_rp_ps_rState_WhlVelFrRight_State_WhlVelFrRight, sizeof(simUI8_t));
  AddReceivePort("ps_rState_StWheelAngle_State_StWheelAngle", simUI8_t, &m_rp_ps_rState_StWheelAngle_State_StWheelAngle, sizeof(simUI8_t));
  AddReceivePort("ps_rSpeedoSpeed_SpeedoSpeed", simUI16_t, &m_rp_ps_rSpeedoSpeed_SpeedoSpeed, sizeof(simUI16_t));
  AddReceivePort("ps_rParkBrake_ParkBrake", simUI8_t, &m_rp_ps_rParkBrake_ParkBrake, sizeof(simUI8_t));
  AddReceivePort("ps_rWhlVelFrLeft_WhlVelFrLeft", simUI16_t, &m_rp_ps_rWhlVelFrLeft_WhlVelFrLeft, sizeof(simUI16_t));
  AddReceivePort("ps_rState_LatAccel_State_LatAccel", simUI8_t, &m_rp_ps_rState_LatAccel_State_LatAccel, sizeof(simUI8_t));
  AddReceivePort("ps_rDriverBraking_DriverBraking", simUI8_t, &m_rp_ps_rDriverBraking_DriverBraking, sizeof(simUI8_t));
  AddReceivePort("ps_rVehLongMotStateExt_VehLongMotStateExt", simUI8_t, &m_rp_ps_rVehLongMotStateExt_VehLongMotStateExt, sizeof(simUI8_t));
  AddReceivePort("ps_rSpeedUnit_SpeedUnit", simUI8_t, &m_rp_ps_rSpeedUnit_SpeedUnit, sizeof(simUI8_t));
  AddReceivePort("ps_rWiperState_WiperState", simUI8_t, &m_rp_ps_rWiperState_WiperState, sizeof(simUI8_t));
  AddReceivePort("ps_rStWheelAngle_StWheelAngle", simUI16_t, &m_rp_ps_rStWheelAngle_StWheelAngle, sizeof(simUI16_t));
  AddReceivePort("ps_rWhlVelReRight_WhlVelReRight", simUI16_t, &m_rp_ps_rWhlVelReRight_WhlVelReRight, sizeof(simUI16_t));
  AddReceivePort("ps_rStateParkBrake_StateParkBrake", simUI8_t, &m_rp_ps_rStateParkBrake_StateParkBrake, sizeof(simUI8_t));
  AddReceivePort("ps_rWiperOutParkPos_WiperOutParkPos", simUI8_t, &m_rp_ps_rWiperOutParkPos_WiperOutParkPos, sizeof(simUI8_t));

  return 0;
}

