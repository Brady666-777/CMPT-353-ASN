"""
UDP Client for Client-Server Communication Assignment
Connects to UDP server on port 53444
Measures RTT for communication
"""

import socket
import time

class UDPClient:
    def __init__(self, host='localhost', port=53444):
        self.host = host
        self.port = port
    
    def send_single_message(self):
        """Send a single message and measure RTT"""
        try:
            # Create socket
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            
            print(f"Connecting to UDP server at {self.host}:{self.port}")
            
            # Prepare message
            message = "Hello UDP"
            
            # Measure RTT (excluding packet construction time)
            start_time = time.time()
            
            # Send message
            client_socket.sendto(message.encode('utf-8'), (self.host, self.port))
            print(f"Sent: {message}")
            
            # Receive response
            response, _ = client_socket.recvfrom(1024)
            
            end_time = time.time()
            
            # Calculate RTT
            rtt = (end_time - start_time) * 1000  # Convert to milliseconds
            
            print(f"Received: {response.decode('utf-8')}")
            print(f"UDP RTT: {rtt:.3f} ms")
            
            client_socket.close()
            return rtt
            
        except Exception as e:
            print(f"UDP Client error: {e}")
            return None
    
    def send_bulk_messages(self, count=1000):
        """Send multiple messages with only one reply at the end"""
        try:
            # Create socket
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            
            print(f"Connecting to UDP server at {self.host}:{self.port}")
            
            # Record start time before sending first message
            start_time = time.time()
            
            # Send bulk messages
            for i in range(count - 1):
                message = f"Hello UDP {i+1}"
                client_socket.sendto(message.encode('utf-8'), (self.host, self.port))
            
            # Send final message
            final_message = f"Hello UDP {count}"
            client_socket.sendto(final_message.encode('utf-8'), (self.host, self.port))
            print(f"Sent {count} messages")
            
            # Receive single response
            response, _ = client_socket.recvfrom(1024)
            
            end_time = time.time()
            
            # Calculate total time
            total_time = (end_time - start_time) * 1000  # Convert to milliseconds
            
            print(f"Received: {response.decode('utf-8')}")
            print(f"UDP Total time for {count} messages: {total_time:.3f} ms")
            
            client_socket.close()
            return total_time
            
        except Exception as e:
            print(f"UDP Client bulk error: {e}")
            return None

def main():
    client = UDPClient()
    
    print("=== UDP Client Test ===")
    print("\n1. Single message RTT test:")
    rtt = client.send_single_message()
    
    print("\n2. Bulk message test (1000 messages):")
    bulk_time = client.send_bulk_messages(1000)
    
    if rtt and bulk_time:
        print(f"\nSummary:")
        print(f"Single message RTT: {rtt:.3f} ms")
        print(f"Bulk 1000 messages time: {bulk_time:.3f} ms")

if __name__ == "__main__":
    main()
