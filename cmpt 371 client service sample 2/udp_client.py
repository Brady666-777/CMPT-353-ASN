import socket, time

HOST = '127.0.0.1'
PORT = 53444

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
    start = time.time()
    sock.sendto(b"Hello UDP", (HOST, PORT))
    data, _ = sock.recvfrom(1024)
    end = time.time()

print("Client received:", data.decode())
print(f"UDP RTT: {(end - start)*1000:.3f} ms")
