#!/usr/bin/env python3
"""
Ethernet Frame CRC-32 Checksum Calculator

This script calculates the CRC-32 checksum for an Ethernet frame containing
the message "HELLO" sent between two stations.

Frame format:
- Destination MAC: 00:09:f6:01:cc:b3
- Source MAC: 00:40:05:1c:0e:9f  
- EtherType/Length: Will be calculated based on payload
- Payload: "HELLO" in ASCII
- Padding: Added if needed to meet minimum frame size
- FCS: CRC-32 checksum (what we're calculating)
"""

import binascii
import struct

def mac_to_bytes(mac_str):
    """Convert MAC address string to bytes"""
    return bytes.fromhex(mac_str.replace(':', ''))

def calculate_crc32_ethernet(data):
    """Calculate CRC-32 checksum using Ethernet polynomial"""
    # Using Python's built-in CRC-32 which uses the IEEE 802.3 polynomial
    # The result needs to be inverted for Ethernet
    crc = binascii.crc32(data) & 0xffffffff
    # Invert the result for Ethernet FCS
    return crc ^ 0xffffffff

def construct_ethernet_frame():
    """Construct the Ethernet frame for the HELLO message"""
    
    # Frame components
    dest_mac = mac_to_bytes("00:09:f6:01:cc:b3")
    src_mac = mac_to_bytes("00:40:05:1c:0e:9f")
    
    # Payload - "HELLO" in ASCII
    payload = b"HELLO"
    
    # EtherType/Length field
    # For 802.3, this should be the length of the payload
    # Since we have 5 bytes, we need to pad to minimum 46 bytes
    payload_length = len(payload)
    min_payload_size = 46  # Minimum payload size for Ethernet
    
    if payload_length < min_payload_size:
        # Pad with zeros
        padding_needed = min_payload_size - payload_length
        payload += b'\x00' * padding_needed
    
    # Length field (2 bytes, big endian)
    length_field = struct.pack('>H', len(payload))
    
    # Construct frame without FCS
    frame_without_fcs = dest_mac + src_mac + length_field + payload
    
    return frame_without_fcs, dest_mac, src_mac, length_field, payload

def main():
    print("Ethernet Frame CRC-32 Checksum Calculator")
    print("=" * 50)
    
    # Construct the frame
    frame_without_fcs, dest_mac, src_mac, length_field, payload = construct_ethernet_frame()
    
    print(f"Destination MAC: {dest_mac.hex(':')}")
    print(f"Source MAC: {src_mac.hex(':')}")
    print(f"Length field: {int.from_bytes(length_field, 'big')} bytes")
    print(f"Original payload: HELLO")
    print(f"Padded payload length: {len(payload)} bytes")
    print()
    
    # Display frame components in hex
    print("Frame components (hex):")
    print(f"Destination MAC: {dest_mac.hex(' ').upper()}")
    print(f"Source MAC: {src_mac.hex(' ').upper()}")
    print(f"Length: {length_field.hex(' ').upper()}")
    print(f"Payload (first 10 bytes): {payload[:10].hex(' ').upper()}")
    print(f"Payload (ASCII): {payload[:5].decode('ascii')} + padding")
    print()
    
    # Calculate CRC-32
    crc32 = calculate_crc32_ethernet(frame_without_fcs)
    
    print("CRC-32 Calculation:")
    print(f"Frame without FCS length: {len(frame_without_fcs)} bytes")
    print(f"Frame without FCS (hex): {frame_without_fcs.hex(' ').upper()}")
    print()
    print(f"CRC-32 checksum: 0x{crc32:08X}")
    print(f"CRC-32 bytes (big endian): {struct.pack('>I', crc32).hex(' ').upper()}")
    
    # Complete frame
    complete_frame = frame_without_fcs + struct.pack('>I', crc32)
    print()
    print(f"Complete frame length: {len(complete_frame)} bytes")
    print(f"Complete frame (hex): {complete_frame.hex(' ').upper()}")
    
    # Generate different input formats for CRC calculators
    print()
    print("=" * 50)
    print("INPUT FORMATS FOR DIFFERENT CRC CALCULATORS:")
    print("=" * 50)
    
    # For calculators with "Bytes" option
    print("1. FOR 'BYTES' INPUT TYPE:")
    print("   Copy and paste these comma-separated decimal values:")
    bytes_format = ', '.join(str(b) for b in frame_without_fcs)
    print(f"   {bytes_format}")
    print()
    
    # For calculators with "Binary string" option  
    print("2. FOR 'BINARY STRING' INPUT TYPE:")
    print("   Copy and paste this binary string:")
    binary_format = ''.join(format(b, '08b') for b in frame_without_fcs)
    print(f"   {binary_format}")
    print()
    
    # For calculators with "String" option (if they accept hex strings)
    print("3. FOR 'STRING' INPUT TYPE (if hex is supported):")
    print("   Copy and paste this hex string (no spaces):")
    hex_format = frame_without_fcs.hex().upper()
    print(f"   {hex_format}")
    print()
    
    # Generate a file with raw bytes that can be uploaded
    with open('ethernet_frame_data.bin', 'wb') as f:
        f.write(frame_without_fcs)
    print("4. RAW BINARY FILE CREATED:")
    print("   File 'ethernet_frame_data.bin' has been created")
    print("   You can upload this file if the calculator accepts file input")
    print()
    
    # Verification
    print()
    print("Verification:")
    print("You can verify this checksum using an online CRC-32 calculator with:")
    print("- Configuration: CRC-32 (Ethernet)")
    print("- Generator: Normal")
    print("- Byte order: Big Endian")
    print(f"- Input data: {frame_without_fcs.hex().upper()}")

if __name__ == "__main__":
    main()
