# UDS Message Parser

ISO 14229-1 Unified Diagnostic Services (UDS) message parser in Python.

Parses automotive diagnostic messages, identifies services, session types, and error codes.

## Usage

```python
from uds_parser import UDSMessage

msg = UDSMessage([0x10, 0x01])
print(msg.detailed_info())
```

## Features
- Service ID parsing (0x10, 0x11, 0x14, 0x19, 0x22, 0x2E, 0x31, etc.)
- Session type identification (Default, Extended, Safety System)
- Error code mapping (General Reject, Service Not Supported, etc.)
- Negative response handling (0x7F)
- Detailed message analysis

## Supported Services
- 0x10: Diagnostic Session Control
- 0x11: ECU Reset
- 0x19: Read DTC Information
- 0x22: Read Data by Identifier
- 0x2E: Write Data by Identifier
- 0x31: Routine Control
- And more...
