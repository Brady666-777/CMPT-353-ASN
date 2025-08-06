import socket, time

HOST = '127.0.0.1'
PORT = 53333

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((HOST, PORT))
    start = time.time()
    for _ in range(1000):
        sock.sendall(b"hello TCP")
    data = sock.recv(1024)
    end = time.time()

print("Client received:", data.decode())
print(f"TCP batch time: {(end - start)*1000:.3f} ms")
