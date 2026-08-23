# UDS Message Parser & Analyzer

A professional-grade automotive diagnostic tool for parsing and analyzing UDS (Unified Diagnostic Services) messages according to ISO 14229-1 standard.

## 🎯 Overview

This project provides a complete UDS diagnostic message parsing solution for automotive testing engineers, enabling rapid interpretation of ECU communication in real-world validation scenarios.

**Key Use Cases:**
- Decode diagnostic messages captured from CANalyzer, INCA, or Dianalyzer
- Batch process UDS message logs for analysis
- Extract and interpret diagnostic trouble codes (DTCs)
- Integrate diagnostic parsing into test automation frameworks

---

## ✨ Features

### Core Parser (`UDS_parser.py`)
- ✅ Parse UDS messages from multiple input formats (hex strings, byte lists, raw bytes)
- ✅ Service ID recognition (15+ UDS services: 0x10, 0x11, 0x19, 0x22, 0x2E, 0x3E, etc.)
- ✅ Negative response detection and parsing (0x7F service)
- ✅ Error code interpretation with 8 standardized NRC (Negative Response Codes)
- ✅ Comprehensive DTC database (70+ SAE J2012 codes: P-codes, C-codes, U-codes)
- ✅ Detailed message formatting with raw bytes and decoded data

### CLI Tool (`uds_analyzer_cli.py`)
- ✅ Batch process UDS messages from JSON/CSV input files
- ✅ Export results to JSON or CSV output formats
- ✅ Command-line interface for integration into test pipelines
- ✅ Comprehensive error handling

### Testing (`test_uds_parser.py`)
- ✅ 13 unit tests covering all major functionality
- ✅ Input validation tests (hex strings, byte lists, raw bytes)
- ✅ DTC decoding verification
- ✅ Message type classification tests

---

## 🚀 Quick Start

### Installation

```bash
git clone https://github.com/shahmichael/uds_msg_parser.git
cd uds_msg_parser
pip3 install pytest  # Optional, for running tests
```

### Basic Usage

```python
from UDS_parser import UDSMessage

# Parse a diagnostic session control message
msg = UDSMessage([0x10, 0x01])
print(msg)
# Output: [Request] Service: Diagnostic Session Control | Raw: 1001

# Get detailed information
print(msg.detailed_info())
# Output:
# ======================================================================
# Raw Bytes (Hex): 1001
# Raw Bytes (List): [16, 1]
# ======================================================================
# Service ID: 0x10
# Service Name: Diagnostic Session Control
# Data Bytes: 01
# ======================================================================
```

### Decode Error Codes

```python
msg = UDSMessage([0x7F, 0x22, 0x33])

# Check if negative response
if msg.is_negative_response():
    print(msg.detailed_info())
    
# Decode DTC
dtc_meaning = msg.decode_dtc("P0101")
print(dtc_meaning)
# Output: Mass or Volume Air Flow Circuit Range/Performance
```

### Batch Processing with CLI

```bash
# Analyze messages from file and print to console
python3 uds_analyzer_cli.py sample_messages.json

# Export results to JSON
python3 uds_analyzer_cli.py sample_messages.json -o decoded_output.json

# Export results to CSV
python3 uds_analyzer_cli.py sample_messages.json -o decoded_output.csv -f csv
```

---

## 📊 Supported UDS Services

| Service ID | Service Name | Status |
|-----------|--------------|--------|
| 0x10 | Diagnostic Session Control | ✅ |
| 0x11 | ECU Reset | ✅ |
| 0x14 | Clear Diagnostic Information | ✅ |
| 0x19 | Read DTC Information | ✅ |
| 0x22 | Read Data by Identifier | ✅ |
| 0x23 | Read Memory by Address | ✅ |
| 0x24 | Read Scaling Data by Identifier | ✅ |
| 0x2E | Write Data by Identifier | ✅ |
| 0x3D | Write Memory by Address | ✅ |
| 0x3E | Tester Present | ✅ |
| 0x7F | Negative Response | ✅ |

---

## 🏗️ Architecture

```UDS_parser.py
├── SERVICES (dict) → Service ID mappings
├── ERROR_CODES (dict) → NRC (Negative Response Code) definitions
├── DTCS (dict) → Diagnostic Trouble Code database (70+ codes)
│
└── UDSMessage (class)
├── init() → Parse raw bytes, hex string, or list
├── is_negative_response() → Check if message is 0x7F
├── is_positive_response() → Check if message is positive response
├── get_service_name() → Retrieve service description
├── parse_negative_response() → Extract NRC details
├── decode_dtc() → Interpret DTC codes
├── detailed_info() → Return formatted message analysis
└── str() → Human-readable message summary
uds_analyzer_cli.py
├── analyze_messages() → Process input file and decode all messages
└── main() → CLI argument parsing and file I/O

---```

## 📥 Input Formats

### JSON Input (`sample_messages.json`)
```json
[
  {"name": "Diagnostic Session Start", "bytes": [16, 1]},
  {"name": "Read DID", "bytes": [34, 241, 144]},
  {"name": "Negative Response", "bytes": [127, 34, 51]}
]
```

### CSV Input
```csv
name,bytes
Diagnostic Session Start,"[16, 1]"
Read DID,"[34, 241, 144]"
Negative Response,"[127, 34, 51]"
```

---

## 📤 Output Format

### JSON Output Example
```json
[
  {
    "name": "Negative Response",
    "raw_hex": "7F2233",
    "raw_list": [127, 34, 51],
    "service_id": "0x7F",
    "service_name": "Negative Response",
    "data_bytes": "2233",
    "negative_response_details": {
      "type": "Negative Response",
      "requested_service": "Read Data by Identifier",
      "error_code": "0x33",
      "error_description": "Security Access Denied"
    }
  }
]
```

---

## 🧪 Testing

Run all tests:
```bash
python3 -m pytest test_uds_parser.py -v
```

Test coverage includes:
- ✅ Message parsing from multiple input formats
- ✅ Service ID recognition
- ✅ Negative response detection
- ✅ DTC decoding (P-codes, C-codes, U-codes)
- ✅ Message type classification
- ✅ Edge case handling

**Result:** 13/13 tests passing ✅

---

## 📚 Technical Details

### UDS Standard Compliance
- **ISO 14229-1:** Unified Diagnostic Services (UDS) protocol
- **SAE J2012:** Diagnostic Trouble Code definitions
- **OBD-II:** On-Board Diagnostics standard codes

### Supported Message Types
- **Request Messages:** ECU diagnostic requests (Service IDs 0x10–0x3E)
- **Positive Responses:** ECU acknowledgments (Service ID + 0x40)
- **Negative Responses:** Error indications (0x7F service)

### Error Codes (NRC)
- 0x10 → General Reject
- 0x11 → Service Not Supported
- 0x12 → Sub-function Not Supported
- 0x13 → Incorrect Message Length
- 0x22 → Conditions Not Correct
- 0x24 → Request Sequence Error
- 0x31 → Request Out Of Range
- 0x33 → Security Access Denied

---

## 🛠️ Use Cases

### 1. Real-Time Diagnostic Analysis
```bash
# Capture UDS responses in CANalyzer → Export to JSON
# Use CLI tool to batch decode all messages
python3 uds_analyzer_cli.py captured_messages.json -o results.json
```

### 2. Test Automation Integration
```python
from UDS_parser import UDSMessage

def validate_ecu_response(raw_bytes):
    msg = UDSMessage(raw_bytes)
    if msg.is_negative_response():
        error = msg.parse_negative_response()
        print(f"ECU Error: {error['error_description']}")
        return False
    return True
```

### 3. DTC Interpretation
```python
# Extract DTCs from diagnostic logs
msg = UDSMessage([0x19, 0x01])
dtc_code = "P0101"
meaning = msg.decode_dtc(dtc_code)
# → "Mass or Volume Air Flow Circuit Range/Performance"
```

---

## 📝 Example Workflow

**Scenario:** Testing Stellantis ECU with INCA

1. **Capture:** Send UDS requests via INCA, record responses
2. **Export:** Export captured messages to `messages.json`
3. **Analyze:** Run CLI tool
```bash
   python3 uds_analyzer_cli.py messages.json -o analysis.json
```
4. **Review:** Open `analysis.json` to see detailed decoded messages
5. **Integrate:** Use parser in test scripts for automated validation

---

## 🤝 Compatibility

- **Python:** 3.6+
- **OS:** macOS, Linux, Windows
- **Dependencies:** pytest (optional, for testing)
- **Tools:** Works with CANalyzer, INCA, Dianalyzer exported logs

---

## 📈 Project Stats

- **Lines of Code:** 350+ (parser) + 100+ (CLI) + 200+ (tests)
- **Test Coverage:** 13 passing unit tests
- **UDS Services:** 15+ supported
- **DTC Database:** 70+ standardized codes
- **Commit History:** Clean, iterative development

---

## 🎓 Learning Resources

- ISO 14229-1 UDS Standard
- OBD-II Diagnostic Codes (SAE J2012)
- Automotive CAN Protocol
- Python Unit Testing with pytest

---

## 📄 License

MIT License - Free for educational and professional use

---

## 👤 Author

**Mehdi Shahkaram**  
System & Software Testing Engineer | Automotive Diagnostics Specialist

---

## 🔗 Links

- **GitHub:** [shahmichael/uds_msg_parser](https://github.com/shahmichael/uds_msg_parser)
- **Portfolio:** [GitHub Profile](https://github.com/shahmichael)

---

## ✅ Project Roadmap

- [x] Core UDS parser (Phase 1)
- [x] DTC database (Phase 1)
- [x] CLI tool with batch processing (Phase 2)
- [x] Comprehensive unit tests (Phase 3)
- [x] Documentation & examples (Phase 4)
- [ ] Real-time CAN listener
- [ ] Multi-ECU support
- [ ] Web UI dashboard

---

**Last Updated:** August 2026  
**Status:** Complete & Production Ready ✅