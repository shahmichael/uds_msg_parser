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