
# For C++ code
RTE_READ_SIGNAL_TEMPLATE = r"""
Std_ReturnType {class_name}::{stub_name}({return_type} * {name})
{{
  // Stub function - replaces reading from RTE by reading from a sim plugin request port
  // TODO: Add 'if' clause for the case that there's nothing received (not dirty)
  *{name} = m_rp_{name};
  return RTE_E_OK;
}}"""

MEMBER_DECLARATION_TEMPLATE = r"""{return_type} m_rp_{name};"""

ADD_RECEIVE_PORT_TEMPLATE = r"""AddReceivePort("{name}", {return_type}, &m_rp_{name}, sizeof({return_type}));"""

SETUP_PORTS_FUNCTION_TEMPLATE = r"""
long {class_name}::SetupPortsFcu(void)
{{
{code}
  return 0;
}}"""

# STUB_SUMMONS_FUNCTION_TEMPLATE = r"""
# long {class_name}::ReadFcuPorts(void)
# {{
# {code}
#   return 0;
# }}
# """

# STUB_SUMMON_TEMPLATE = r"""{stub_name}({name});"""

# For SIL FW configuration files
SIMUDEX_PRO_PORT_TEMPLATE = r"""
[PPort {name}]
CfgSectionType = UdexProvidePort::SignalURL
Name           = {name}
URL.0          = {url}
DataType       = {sim_data_type}
"""

SIMCON_FILE_TEMPLATE = r"""
[Request2ProvideConnections]
CfgSectionType=Request2ProvideConnection

{connections}
"""

CONNECTION_TEMPLATE = r"""SIM VDY.{name} = FCU VDY.{name}"""