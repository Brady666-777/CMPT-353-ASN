"""
Simple Demo Script for Individual Testing
Run this to test each component separately for screenshots and manual verification
"""

import sys
import time
import subprocess
from pathlib import Path

def run_demo():
    python_exe = "C:/Users/wohai/AppData/Local/Microsoft/WindowsApps/python3.11.exe"
    
    print("CMPT 371 - Network Programming Assignment Demo")
    print("=" * 50)
    
    print("\nThis demo will show each part of the assignment:")
    print("1. TCP client-server communication")
    print("2. UDP client-server communication") 
    print("3. RTT comparison")
    print("4. Bulk message testing")
    print("5. Same port protocol testing")
    
    print("\nPress Enter to start TCP demo...")
    input()
    
    # TCP Demo
    print("\n--- TCP DEMO ---")
    print("Starting TCP server in background...")
    tcp_server = subprocess.Popen([python_exe, "tcp_server.py"])
    time.sleep(2)
    
    print("Running TCP client...")
    tcp_result = subprocess.run([python_exe, "tcp_client.py"], 
                               capture_output=True, text=True)
    print(tcp_result.stdout)
    
    tcp_server.terminate()
    print("TCP server stopped")
    
    print("\nPress Enter to start UDP demo...")
    input()
    
    # UDP Demo
    print("\n--- UDP DEMO ---")
    print("Starting UDP server in background...")
    udp_server = subprocess.Popen([python_exe, "udp_server.py"])
    time.sleep(2)
    
    print("Running UDP client...")
    udp_result = subprocess.run([python_exe, "udp_client.py"], 
                               capture_output=True, text=True)
    print(udp_result.stdout)
    
    udp_server.terminate()
    print("UDP server stopped")
    
    print("\n--- DEMO COMPLETE ---")
    print("For complete automated testing, run: python run_tests.py")

if __name__ == "__main__":
    run_demo()
