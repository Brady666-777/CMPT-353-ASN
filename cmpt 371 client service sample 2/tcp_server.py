import socket

HOST = ''             # bind to all interfaces
PORT = 53333

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind((HOST, PORT))
    srv.listen(1)
    print(f"TCP server listening on port {PORT}...")
    conn, addr = srv.accept()
    with conn:
        print("Connected by", addr)
        data = conn.recv(1024)
        print("Server received:", data.decode())
        conn.sendall(b"back at you TCP")
        print("Server replied and closing.")
