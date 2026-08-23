#!/usr/bin/env python3
"""
UDS Message Analyzer - Command Line Tool
Decode UDS diagnostic messages from files
"""

import json
import csv
import argparse
import sys
from pathlib import Path
from UDS_parser import UDSMessage

def analyze_messages(input_file, output_file=None, output_format='json'):
    """Read messages from input file and decode them"""
    
    # Read input file
    with open(input_file, 'r') as f:
        if input_file.endswith('.json'):
            messages = json.load(f)
        else:
            # CSV format
            reader = csv.DictReader(f)
            messages = list(reader)
    
    # Decode messages
    results = []
    for msg in messages:
        try:
            if isinstance(msg, dict) and 'bytes' in msg:
                raw_bytes = msg['bytes']
            else:
                continue
            
            uds_msg = UDSMessage(raw_bytes)
            decoded = {
                "name": msg.get("name", ""),
                "raw_hex": uds_msg.raw.hex().upper(),
                "raw_list": list(uds_msg.raw),
                "service_id": f"0x{uds_msg.service_id:02X}",
                "service_name": uds_msg.get_service_name(),
                "data_bytes": uds_msg.data.hex().upper() if uds_msg.data else "None"
            }
            
            # Add negative response details if applicable
            if uds_msg.is_negative_response():
                parsed = uds_msg.parse_negative_response()
                if parsed:
                    decoded["negative_response_details"] = parsed
            
            results.append(decoded)
        except Exception as e:
            results.append({"name": msg.get("name", ""), "error": str(e)})
    
    # Write output
    if output_file:
        with open(output_file, 'w') as f:
            if output_format == 'json':
                json.dump(results, f, indent=2)
            elif output_format == 'csv':
                writer = csv.DictWriter(f, fieldnames=['name', 'raw_hex', 'service_name', 'data_bytes'])
                writer.writeheader()
                for result in results:
                    writer.writerow({k: v for k, v in result.items() if k in ['name', 'raw_hex', 'service_name', 'data_bytes']})
        print(f"Results written to {output_file}")
    else:
        # Print to console
        print(json.dumps(results, indent=2))

def main():
    parser = argparse.ArgumentParser(
        description='UDS Message Analyzer - Decode automotive diagnostic messages'
    )
    parser.add_argument('input', help='Input file (JSON or CSV with UDS messages)')
    parser.add_argument('-o', '--output', help='Output file (default: print to console)')
    parser.add_argument('-f', '--format', choices=['json', 'csv'], default='json', 
                        help='Output format (default: json)')
    
    args = parser.parse_args()
    
    # Check if input file exists
    if not Path(args.input).exists():
        print(f"Error: Input file '{args.input}' not found")
        sys.exit(1)
    
    try:
        analyze_messages(args.input, args.output, args.format)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
