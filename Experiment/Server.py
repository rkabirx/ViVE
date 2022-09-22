
import socket


while True:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('0.0.0.0', 5005))
    s.listen(1)
    conn, addr = s.accept()
    while 1:
        data = conn.recv(1024)
        print("received data",list(data))
        if not data:
            break
        conn.sendall(data)
    conn.close()