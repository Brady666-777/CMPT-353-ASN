"""
TCP Server for Client-Server Communication Assignment
Port: 53333
Message: "hello TCP" -> "back at you TCP"
"""

import socket
import threading
import time

class TCPServer:
    def __init__(self, host='localhost', port=53333):
        self.host = host
        self.port = port
        self.socket = None
        self.running = False
    
    def start(self):
        """Start the TCP server"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind((self.host, self.port))
            self.socket.listen(5)
            self.running = True
            
            print(f"TCP Server listening on {self.host}:{self.port}")
            
            while self.running:
                try:
                    client_socket, address = self.socket.accept()
                    print(f"Connection from {address}")
                    
                    # Handle client in a separate thread
                    client_thread = threading.Thread(
                        target=self.handle_client, 
                        args=(client_socket, address)
                    )
                    client_thread.daemon = True
                    client_thread.start()
                    
                except socket.error as e:
                    if self.running:
                        print(f"Socket error: {e}")
                    break
                    
        except Exception as e:
            print(f"Server error: {e}")
        finally:
            self.stop()
    
    def handle_client(self, client_socket, address):
        """Handle individual client connections"""
        try:
            while self.running:
                # Receive data from client
                data = client_socket.recv(1024).decode('utf-8')
                if not data:
                    break
                
                print(f"Received from {address}: {data}")
                
                # Process different message types
                if data == "hello TCP":
                    response = "back at you TCP"
                elif data.startswith("hello TCP"):
                    # For bulk messages, only reply to the last one
                    if "1000" in data:
                        response = "back at you TCP"
                    else:
                        continue  # Don't reply to intermediate messages
                else:
                    response = "back at you TCP"  # Default response
                
                # Send response back to client
                client_socket.send(response.encode('utf-8'))
                print(f"Sent to {address}: {response}")
                
        except Exception as e:
            print(f"Error handling client {address}: {e}")
        finally:
            client_socket.close()
            print(f"Connection with {address} closed")
    
    def stop(self):
        """Stop the TCP server"""
        self.running = False
        if self.socket:
            self.socket.close()
        print("TCP Server stopped")

def main():
    server = TCPServer()
    try:
        server.start()
    except KeyboardInterrupt:
        print("\nShutting down TCP server...")
        server.stop()

if __name__ == "__main__":
    main()
