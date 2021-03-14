EXPORT_TEMPLETE = r"""{
    "exporter": {
        "default": {
            "cycle_id": "0x41",
            "name": "Sil Sil Exporter",
            "test_type": "edp_sil",
            "rec_file_extension": "",
            "signals": []
        }
    },"""

SIGNALS_OVERALL = r"""
    "signals": {{
        {exporter_signal_list}
    }} 
}}
"""


INDIVIDUAL_SIGNAL = r"""
        "{pport_official}": {{
            "meas_freezes": [
                "{signal_url_lists}"
            ]
        }},     
"""
