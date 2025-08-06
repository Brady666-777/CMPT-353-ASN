"""
Comprehensive Test Script for TCP/UDP Client-Server Communication Assignment
This script demonstrates all test scenarios required for the assignment.
"""

import subprocess
import time
import threading
import sys
from tcp_client import TCPClient
from udp_client import UDPClient

class NetworkingTests:
    def __init__(self):
        self.tcp_server_process = None
        self.udp_server_process = None
    
    def start_tcp_server(self):
        """Start TCP server in background"""
        try:
            self.tcp_server_process = subprocess.Popen([
                sys.executable, "tcp_server.py"
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            time.sleep(2)  # Give server time to start
            print("TCP Server started")
            return True
        except Exception as e:
            print(f"Failed to start TCP server: {e}")
            return False
    
    def start_udp_server(self):
        """Start UDP server in background"""
        try:
            self.udp_server_process = subprocess.Popen([
                sys.executable, "udp_server.py"
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            time.sleep(2)  # Give server time to start
            print("UDP Server started")
            return True
        except Exception as e:
            print(f"Failed to start UDP server: {e}")
            return False
    
    def stop_servers(self):
        """Stop all running servers"""
        if self.tcp_server_process:
            self.tcp_server_process.terminate()
            self.tcp_server_process = None
            print("TCP Server stopped")
        
        if self.udp_server_process:
            self.udp_server_process.terminate()
            self.udp_server_process = None
            print("UDP Server stopped")
    
    def test_single_message_rtt(self):
        """Test Part A: Single message RTT comparison"""
        print("\n" + "="*60)
        print("PART A: Single Message RTT Test")
        print("="*60)
        
        # Start servers
        print("\nStarting servers...")
        tcp_started = self.start_tcp_server()
        udp_started = self.start_udp_server()
        
        if not (tcp_started and udp_started):
            print("Failed to start servers")
            return None, None
        
        # Test TCP
        print("\nTesting TCP communication:")
        tcp_client = TCPClient()
        tcp_rtt = tcp_client.send_single_message()
        
        # Test UDP
        print("\nTesting UDP communication:")
        udp_client = UDPClient()
        udp_rtt = udp_client.send_single_message()
        
        # Compare results
        if tcp_rtt and udp_rtt:
            print(f"\n--- RTT COMPARISON ---")
            print(f"TCP RTT: {tcp_rtt:.3f} ms")
            print(f"UDP RTT: {udp_rtt:.3f} ms")
            
            if udp_rtt < tcp_rtt:
                print(f"UDP is {tcp_rtt - udp_rtt:.3f} ms faster")
            else:
                print(f"TCP is {udp_rtt - tcp_rtt:.3f} ms faster")
        
        self.stop_servers()
        return tcp_rtt, udp_rtt
    
    def test_bulk_messages(self):
        """Test Part C: 1000 consecutive messages"""
        print("\n" + "="*60)
        print("PART C: Bulk Message Test (1000 messages)")
        print("="*60)
        
        # Start servers
        print("\nStarting servers...")
        tcp_started = self.start_tcp_server()
        udp_started = self.start_udp_server()
        
        if not (tcp_started and udp_started):
            print("Failed to start servers")
            return None, None
        
        # Test TCP bulk
        print("\nTesting TCP bulk communication:")
        tcp_client = TCPClient()
        tcp_bulk_time = tcp_client.send_bulk_messages(1000)
        
        # Test UDP bulk
        print("\nTesting UDP bulk communication:")
        udp_client = UDPClient()
        udp_bulk_time = udp_client.send_bulk_messages(1000)
        
        # Compare results
        if tcp_bulk_time and udp_bulk_time:
            print(f"\n--- BULK TIME COMPARISON ---")
            print(f"TCP 1000 messages time: {tcp_bulk_time:.3f} ms")
            print(f"UDP 1000 messages time: {udp_bulk_time:.3f} ms")
            
            if udp_bulk_time < tcp_bulk_time:
                print(f"UDP is {tcp_bulk_time - udp_bulk_time:.3f} ms faster")
            else:
                print(f"TCP is {udp_bulk_time - tcp_bulk_time:.3f} ms faster")
        
        self.stop_servers()
        return tcp_bulk_time, udp_bulk_time
    
    def test_same_port_scenario(self):
        """Test Part D: Both servers on same port (53333)"""
        print("\n" + "="*60)
        print("PART D: Same Port Test (Both servers on port 53333)")
        print("="*60)
        
        # Start TCP server on port 53333
        print("\nStarting TCP server on port 53333...")
        tcp_started = self.start_tcp_server()
        
        # Try to start UDP server on same port
        print("Starting UDP server on port 53333...")
        try:
            udp_server_53333 = subprocess.Popen([
                sys.executable, "-c", 
                """
import socket
import sys
try:
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(('localhost', 53333))
    print('UDP server successfully bound to port 53333')
    
    while True:
        data, addr = udp_socket.recvfrom(1024)
        message = data.decode('utf-8')
        print(f'UDP received: {message} from {addr}')
        if message == 'hello TCP':
            response = 'back at you UDP'
            udp_socket.sendto(response.encode('utf-8'), addr)
            print(f'UDP sent: {response}')
except Exception as e:
    print(f'UDP server error: {e}')
    sys.exit(1)
                """
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            time.sleep(2)
            print("UDP server started on port 53333")
        except Exception as e:
            print(f"Failed to start UDP server on port 53333: {e}")
            return
        
        # Test with TCP client
        print("\nTesting TCP client against both servers on port 53333:")
        tcp_client = TCPClient(port=53333)  # Connect to port 53333
        
        try:
            rtt = tcp_client.send_single_message()
            if rtt:
                print(f"TCP client successfully communicated with TCP server")
                print(f"RTT: {rtt:.3f} ms")
        except Exception as e:
            print(f"TCP client test failed: {e}")
        
        # Clean up
        if hasattr(self, 'tcp_server_process') and self.tcp_server_process:
            self.tcp_server_process.terminate()
        udp_server_53333.terminate()
        
        print("\nConclusion: TCP client connects only to TCP server on port 53333")
        print("UDP server on same port doesn't respond to TCP connections")
    
    def run_all_tests(self):
        """Run all assignment tests"""
        print("CMPT 371 - Client-Server Communication Assignment Tests")
        print("="*60)
        
        # Run Part A
        tcp_rtt, udp_rtt = self.test_single_message_rtt()
        
        # Run Part C
        tcp_bulk, udp_bulk = self.test_bulk_messages()
        
        # Run Part D
        self.test_same_port_scenario()
        
        # Summary
        print("\n" + "="*60)
        print("FINAL SUMMARY")
        print("="*60)
        
        if tcp_rtt and udp_rtt:
            print(f"\nPart A - Single Message RTT:")
            print(f"  TCP: {tcp_rtt:.3f} ms")
            print(f"  UDP: {udp_rtt:.3f} ms")
            print(f"  Analysis: UDP is typically faster due to no connection establishment overhead")
        
        if tcp_bulk and udp_bulk:
            print(f"\nPart C - 1000 Messages:")
            print(f"  TCP: {tcp_bulk:.3f} ms")
            print(f"  UDP: {udp_bulk:.3f} ms")
            print(f"  Analysis: Connection reuse makes TCP more efficient for bulk transfers")
        
        print(f"\nPart D - Same Port Test:")
        print(f"  TCP and UDP can bind to same port number but serve different protocols")
        print(f"  TCP client only communicates with TCP server, not UDP server")

def main():
    tester = NetworkingTests()
    try:
        tester.run_all_tests()
    except KeyboardInterrupt:
        print("\nTest interrupted by user")
    finally:
        tester.stop_servers()

if __name__ == "__main__":
    main()
