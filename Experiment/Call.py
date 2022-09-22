import threading
import socket
import time

stream_lock = threading.Lock()


def server_func():
    import Server
    Server
def client_func():
    import Client
    Client

t_server = threading.Thread(target=server_func).start()
time.sleep(3)
t_client = threading.Thread(target=client_func).start()

# Output:
# received data [1, 2, 3]
# Received b'\x01\x02\x03'