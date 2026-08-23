"""
Unit tests for UDS Message Parser
"""

import pytest
from UDS_parser import UDSMessage

class TestUDSMessageParsing:
    """Test basic UDS message parsing"""
    
    def test_diagnostic_session_control(self):
        """Test parsing 0x10 Diagnostic Session Control"""
        msg = UDSMessage([0x10, 0x01])
        assert msg.service_id == 0x10
        assert msg.get_service_name() == "Diagnostic Session Control"
        assert msg.data.hex() == "01"
    
    def test_read_data_by_identifier(self):
        """Test parsing 0x22 Read Data by Identifier"""
        msg = UDSMessage([0x22, 0xF1, 0x90])
        assert msg.service_id == 0x22
        assert msg.get_service_name() == "Read Data by Identifier"
        assert msg.data.hex().upper() == "F190"
    
    def test_negative_response(self):
        """Test parsing negative response 0x7F"""
        msg = UDSMessage([0x7F, 0x22, 0x33])
        assert msg.is_negative_response()
        assert msg.service_id == 0x7F
        assert msg.get_service_name() == "Negative Response"
    
    def test_raw_bytes_input(self):
        """Test parsing from raw bytes"""
        msg = UDSMessage(bytes([0x10, 0x01]))
        assert msg.service_id == 0x10
    
    def test_list_input(self):
        """Test parsing from list"""
        msg = UDSMessage([0x10, 0x01])
        assert msg.service_id == 0x10
    
    def test_hex_string_input(self):
        """Test parsing from hex string"""
        msg = UDSMessage("10 01")
        assert msg.service_id == 0x10

class TestDTCDecoding:
    """Test DTC database and decoding"""
    
    def test_dtc_p0101(self):
        """Test decoding P0101"""
        msg = UDSMessage([0x19])
        result = msg.decode_dtc("P0101")
        assert "Air Flow" in result
    
    def test_dtc_c1234(self):
        """Test decoding C1234"""
        msg = UDSMessage([0x19])
        result = msg.decode_dtc("C1234")
        assert "ABS" in result
    
    def test_dtc_u0100(self):
        """Test decoding U0100"""
        msg = UDSMessage([0x19])
        result = msg.decode_dtc("U0100")
        assert "ECM" in result
    
    def test_unknown_dtc(self):
        """Test handling of unknown DTC"""
        msg = UDSMessage([0x19])
        result = msg.decode_dtc("X9999")
        assert "Unknown" in result

class TestMessageTypes:
    """Test different message types"""
    
    def test_ecu_reset(self):
        """Test ECU Reset (0x11)"""
        msg = UDSMessage([0x11, 0x01])
        assert msg.get_service_name() == "ECU Reset"
    
    def test_read_dtc(self):
        """Test Read DTC (0x19)"""
        msg = UDSMessage([0x19, 0x01])
        assert msg.get_service_name() == "Read DTC Information"
    
    def test_positive_response(self):
        """Test positive response detection"""
        msg = UDSMessage([0x50, 0x01])  # Positive response to 0x10
        assert msg.is_positive_response()
        assert not msg.is_negative_response()

if __name__ == "__main__":
    pytest.main([__file__, "-v"])