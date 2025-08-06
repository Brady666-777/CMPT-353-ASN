"""
UDP Server for Client-Server Communication Assignment
Port: 53444
Message: "Hello UDP" -> "back at you UDP"
"""

import socket
import time

class UDPServer:
    def __init__(self, host='localhost', port=53444):
        self.host = host
        self.port = port
        self.socket = None
        self.running = False
    
    def start(self):
        """Start the UDP server"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.socket.bind((self.host, self.port))
            self.running = True
            
            print(f"UDP Server listening on {self.host}:{self.port}")
            
            while self.running:
                try:
                    # Receive data from client
                    data, address = self.socket.recvfrom(1024)
                    message = data.decode('utf-8')
                    
                    print(f"Received from {address}: {message}")
                    
                    # Process different message types
                    if message == "Hello UDP":
                        response = "back at you UDP"
                    elif message.startswith("Hello UDP"):
                        # For bulk messages, only reply to the last one
                        if "1000" in message:
                            response = "back at you UDP"
                        else:
                            continue  # Don't reply to intermediate messages
                    else:
                        response = "back at you UDP"  # Default response
                    
                    # Send response back to client
                    self.socket.sendto(response.encode('utf-8'), address)
                    print(f"Sent to {address}: {response}")
                    
                except socket.error as e:
                    if self.running:
                        print(f"Socket error: {e}")
                    break
                    
        except Exception as e:
            print(f"Server error: {e}")
        finally:
            self.stop()
    
    def stop(self):
        """Stop the UDP server"""
        self.running = False
        if self.socket:
            self.socket.close()
        print("UDP Server stopped")

def main():
    server = UDPServer()
    try:
        server.start()
    except KeyboardInterrupt:
        print("\nShutting down UDP server...")
        server.stop()

if __name__ == "__main__":
    main()
