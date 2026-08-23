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

    # Diagnostic Trouble Codes (DTC) Database
    DTCS = {
        # Powertrain Codes (P)
        "P0101": "Mass or Volume Air Flow Circuit Range/Performance",
        "P0102": "Mass or Volume Air Flow Circuit Low",
        "P0103": "Mass or Volume Air Flow Circuit High",
        "P0104": "Mass or Volume Air Flow Circuit Intermittent",
        "P0105": "Manifold Absolute Pressure/Barometric Pressure Circuit",
        "P0106": "MAP/Barometric Pressure Circuit Range/Performance",
        "P0107": "MAP/Barometric Pressure Circuit Low",
        "P0108": "MAP/Barometric Pressure Circuit High",
        "P0110": "Intake Air Temperature Circuit",
        "P0111": "Intake Air Temperature Circuit Range/Performance",
        "P0112": "Intake Air Temperature Circuit Low",
        "P0113": "Intake Air Temperature Circuit High",
        "P0114": "Intake Air Temperature Circuit Intermittent",
        "P0115": "Engine Coolant Temperature Circuit",
        "P0116": "Engine Coolant Temperature Circuit Range/Performance",
        "P0117": "Engine Coolant Temperature Circuit Low",
        "P0118": "Engine Coolant Temperature Circuit High",
        "P0120": "Throttle/Pedal Position Sensor/Switch Circuit",
        "P0121": "Throttle/Pedal Position Sensor/Switch Circuit Range/Performance",
        "P0122": "Throttle/Pedal Position Sensor/Switch Circuit Low",
        "P0123": "Throttle/Pedal Position Sensor/Switch Circuit High",
        "P0125": "Insufficient Coolant Temperature for Closed Loop Fuel Control",
        "P0128": "Coolant Thermostat (Coolant Temp Regulation) malfunction",
        "P0130": "O2 Sensor Circuit",
        "P0131": "O2 Sensor Circuit Low Voltage",
        "P0132": "O2 Sensor Circuit High Voltage",
        "P0133": "O2 Sensor Circuit Slow Response",
        "P0134": "O2 Sensor Circuit No Activity",
        "P0200": "Injector Circuit",
        "P0201": "Injector Circuit Cylinder 1",
        "P0202": "Injector Circuit Cylinder 2",
        "P0203": "Injector Circuit Cylinder 3",
        "P0204": "Injector Circuit Cylinder 4",
        "P0300": "Random/Multiple Cylinder Misfire Detected",
        "P0301": "Cylinder 1 Misfire Detected",
        "P0302": "Cylinder 2 Misfire Detected",
        "P0303": "Cylinder 3 Misfire Detected",
        "P0304": "Cylinder 4 Misfire Detected",
        "P0400": "EGR System Malfunction",
        "P0401": "EGR Insufficient Flow",
        "P0402": "EGR Excessive Flow",
        "P0500": "Vehicle Speed Sensor Malfunction",
        "P0505": "Idle Speed Control System Malfunction",
        "P0601": "Internal Control Module Memory Check Sum Error",
        "P0602": "Control Module Programming Error",
        "P0603": "Internal Control Module Keep Alive Memory Error",
        "P0604": "Internal Control Module Random Access Memory Error",
        "P0605": "Internal Control Module Read Only Memory Error",
        "P0700": "Transmission Control System Malfunction",
        "P0800": "Transmission Control System Malfunction",
        
        # Chassis Codes (C)
        "C0100": "ABS Module Fault",
        "C0121": "Wheel Speed Sensor Fault",
        "C0145": "Loss of ABS Brake Fluid",
        "C0200": "ABS Pump Motor Fault",
        "C0235": "Wheel Speed Sensor Open Circuit",
        "C0241": "Wheel Speed Sensor Circuit High",
        "C1001": "Loss of Anti-Lock Brake Pressure",
        "C1234": "ABS Solenoid Valve Stuck On",
        
        # Body Codes (B)
        "B0001": "Battery Voltage High",
        "B0002": "Battery Voltage Low",
        "B1000": "Headlamp Circuit Fault",
        "B1234": "Driver Seat Occupancy Sensor Fault",
        
        # Network/Communication Codes (U)
        "U0100": "Lost Communication with ECM",
        "U0101": "Lost Communication with TCM",
        "U0102": "Lost Communication with ABS",
        "U0103": "Lost Communication with Instrument Cluster",
        "U0110": "Lost Communication with Gateway Module",
        "U0121": "Lost Communication with Transmission Control Module",
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
    
    def decode_dtc(self, dtc_code):
        """Decode a DTC (Diagnostic Trouble Code)"""
        if isinstance(dtc_code, str):
            code = dtc_code.upper()
        else:
            # Convert from hex bytes if needed
            code = f"P{dtc_code:04X}" if dtc_code < 0x10000 else dtc_code
    
        return DTCS.get(code, f"Unknown DTC: {code}")

    def extract_and_decode_dtcs(self):
        """Extract DTCs from diagnostic messages (e.g., 0x19 service)"""
        if self.service_id == 0x19:  # Read DTC Information
        # For now, return a placeholder
        # Real implementation would parse DTC data
            return {"raw_data": self.data.hex(), "note": "DTC extraction logic to be implemented"}
        return None
    
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
        info = f"\n{'='*70}\n"
        info += f"Raw Bytes (Hex): {self.raw.hex().upper()}\n"
        info += f"Raw Bytes (List): {list(self.raw)}\n"
        info += f"{'='*70}\n"
        info += f"Service ID: 0x{self.service_id:02X}\n"
        info += f"Service Name: {self.get_service_name()}\n"
        info += f"Data Bytes: {self.data.hex().upper() if self.data else 'None'}\n"
        info += f"{'='*70}\n"
    
        if self.is_negative_response():
            parsed = self.parse_negative_response()
            if parsed:
                info += "NEGATIVE RESPONSE DETAILS:\n"
                for key, value in parsed.items():
                    info += f"  {key}: {value}\n"
                info += f"{'='*70}\n"
    
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
        
    # Test 3: Negative response (UPDATED)
    print("Test 3: Negative Response (7F 22 33)")
    msg3 = UDSMessage([0x7F, 0x22, 0x33])
    print(msg3.detailed_info())
    