"""
UDS (Unified Diagnostic Services) Message Parser
ISO 14229-1 Implementation
"""

class UDSMessage:
    """Parse and interpret UDS diagnostic messages"""
    
    # UDS Service IDs (common ones)
    SERVICES = {
        0x10: "Diagnostic Session Control",
        0x11: "ECU Reset",
        0x14: "Clear Diagnostic Information",
        0x19: "Read DTC Information",
        0x22: "Read Data by Identifier",
        0x23: "Read Memory by Address",
        0x2E: "Write Data by Identifier",
        0x2F: "Input Output Control by Identifier",
        0x31: "Routine Control",
        0x34: "Request Download",
        0x35: "Request Upload",
        0x36: "Transfer Data",
        0x37: "Request Transfer Exit",
        0x3D: "Write Memory by Address",
        0x3E: "Tester Present",
    }
    
    # Diagnostic Session Types (for 0x10 service)
    SESSION_TYPES = {
        0x01: "Default Session",
        0x03: "Extended Diagnostic Session",
        0x10: "Safety System Diagnostic Session",
    }
    
    # Error codes (negative response 0x7F)
    ERROR_CODES = {
        0x10: "General Reject",
        0x11: "Service Not Supported",
        0x12: "Sub-function Not Supported",
        0x13: "Incorrect Message Length",
        0x22: "Conditions Not Correct",
        0x24: "Request Sequence Error",
        0x31: "Request Out Of Range",
        0x33: "Security Access Denied",
    }
    
    def __init__(self, raw_bytes):
        """Initialize with raw UDS message bytes"""
        if isinstance(raw_bytes, str):
            # Handle hex string input (e.g., "10 01")
            self.raw = bytes.fromhex(raw_bytes.replace(" ", ""))
        elif isinstance(raw_bytes, list):
            # Handle list input (e.g., [0x10, 0x01])
            self.raw = bytes(raw_bytes)
        else:
            self.raw = raw_bytes
        
        if len(self.raw) == 0:
            raise ValueError("Empty message")
        
        self.service_id = self.raw[0]
        self.data = self.raw[1:] if len(self.raw) > 1 else b''
    
    def is_negative_response(self):
        """Check if this is a negative response (0x7F)"""
        return self.service_id == 0x7F
    
    def is_positive_response(self):
        """Check if this is a positive response (service ID + 0x40)"""
        return self.service_id >= 0x40 and self.service_id <= 0x7E
    
    def get_service_name(self):
        """Get human-readable service name"""
        if self.is_negative_response():
            return "Negative Response"
        
        # For positive response, subtract 0x40 to get original service
        original_service = self.service_id - 0x40 if self.is_positive_response() else self.service_id
        return self.SERVICES.get(original_service, f"Unknown Service (0x{original_service:02X})")
    
    def parse_diagnostic_session(self):
        """Parse Diagnostic Session Control service (0x10)"""
        if self.service_id != 0x10:
            return None
        
        if len(self.data) == 0:
            return {"error": "No session type specified"}
        
        session_type = self.data[0]
        return {
            "service": "Diagnostic Session Control",
            "session_type": self.SESSION_TYPES.get(session_type, f"Unknown (0x{session_type:02X})"),
            "session_code": f"0x{session_type:02X}"
        }
    
    def parse_read_did(self):
        """Parse Read Data by Identifier service (0x22)"""
        if self.service_id != 0x22:
            return None
        
        if len(self.data) < 2:
            return {"error": "Invalid DID format"}
        
        # DID is typically 2 bytes
        did = int.from_bytes(self.data[:2], 'big')
        return {
            "service": "Read Data by Identifier",
            "did": f"0x{did:04X}",
            "did_decimal": did
        }
    
    def parse_negative_response(self):
        """Parse negative response (0x7F)"""
        if not self.is_negative_response():
            return None
        
        if len(self.data) < 2:
            return {"error": "Invalid negative response format"}
        
        requested_service = self.data[0]
        error_code = self.data[1]
        
        return {
            "type": "Negative Response",
            "requested_service": self.SERVICES.get(requested_service, f"Unknown (0x{requested_service:02X})"),
            "error_code": f"0x{error_code:02X}",
            "error_description": self.ERROR_CODES.get(error_code, "Unknown Error"),
        }
    
    def __str__(self):
        """String representation of the message"""
        msg_type = "Response" if self.is_positive_response() else "Request"
        return f"[{msg_type}] Service: {self.get_service_name()} | Raw: {self.raw.hex().upper()}"
    
    def detailed_info(self):
        """Return detailed information about the message"""
        info = f"Raw Bytes: {self.raw.hex().upper()}\n"
        info += f"Service ID: 0x{self.service_id:02X}\n"
        info += f"Service Name: {self.get_service_name()}\n"
        info += f"Data Bytes: {self.data.hex().upper() if self.data else 'None'}\n"
        
        if self.is_negative_response():
            parsed = self.parse_negative_response()
            if parsed:
                info += f"\nNegative Response Details:\n"
                for key, value in parsed.items():
                    info += f"  {key}: {value}\n"
        
        return info


# Example usage
if __name__ == "__main__":
    # Test 1: Start diagnostic session
    print("Test 1: Start Diagnostic Session")
    msg1 = UDSMessage([0x10, 0x01])
    print(msg1)
    print(msg1.detailed_info())
    print()
    
    # Test 2: Read DID
    print("Test 2: Read Data by Identifier")
    msg2 = UDSMessage([0x22, 0xF1, 0x90])
    print(msg2)
    print(msg2.detailed_info())
    print()
    
    # Test 3: Negative response
    print("Test 3: Negative Response")
    msg3 = UDSMessage([0x7F, 0x22, 0x33])
    print(msg3)
    print(msg3.detailed_info())
    