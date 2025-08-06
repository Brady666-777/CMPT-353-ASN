"""
UDP Server on Port 53333 for Same Port Testing (Part D)
This server binds to the same port as TCP server to test protocol separation
"""

import socket
import sys

def main():
    try:
        # Create UDP socket
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        # Attempt to bind to port 53333 (same as TCP server)
        udp_socket.bind(('localhost', 53333))
        print("UDP server successfully bound to port 53333")
        print("Waiting for messages...")
        
        while True:
            # Receive data
            data, addr = udp_socket.recvfrom(1024)
            message = data.decode('utf-8')
            print(f"UDP server received: '{message}' from {addr}")
            
            # Respond to any message
            response = "back at you UDP (from port 53333)"
            udp_socket.sendto(response.encode('utf-8'), addr)
            print(f"UDP server sent: '{response}' to {addr}")
            
    except socket.error as e:
        print(f"UDP server socket error: {e}")
        print("This is expected if TCP server is already using port 53333")
    except Exception as e:
        print(f"UDP server error: {e}")
    finally:
        if 'udp_socket' in locals():
            udp_socket.close()
        print("UDP server on port 53333 stopped")

if __name__ == "__main__":
    main()
