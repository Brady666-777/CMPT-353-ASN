import socket

HOST = ''
PORT = 53333

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as srv:
    srv.bind((HOST, PORT))
    print(f"Batch UDP server listening on port {PORT}...")
    count = 0
    addr = None
    while count < 1000:
        data, addr = srv.recvfrom(1024)
        count += 1
    srv.sendto(b"back at you UDP", addr)
    print("Server: received 1000 messages, replied.")
