import socket

HOST = ''
PORT = 53444

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as srv:
    srv.bind((HOST, PORT))
    print(f"UDP server listening on port {PORT}...")
    data, addr = srv.recvfrom(1024)
    print("Server received:", data.decode(), "from", addr)
    srv.sendto(b"back at you UDP", addr)
    print("Server replied and exiting.")
