import socket

HOST = ''
PORT = 53333

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind((HOST, PORT))
    srv.listen(1)
    print(f"Batch TCP server listening on port {PORT}...")
    conn, addr = srv.accept()
    with conn:
        count = 0
        while count < 1000:
            data = conn.recv(1024)
            if not data:
                break
            count += 1
        conn.sendall(b"back at you TCP")
        print("Server: received 1000 messages, replied.")
