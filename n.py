
import socket
import time
from multiprocessing import Process

def server_send(client_socket):
    while True:
        message = input()
        client_socket.send(message.encode())

def server_receive(client_socket):
    while True:
        data = client_socket.recv(1024)
        time.sleep(1)
        print("Client (Received): " + data.decode())

def message(port_no):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('192.168.1.112', port_no))
    server_socket.listen(1)
    print("Server is waiting for a connection...")
    client_socket, addr = server_socket.accept()

    # Create and start server processes
    server_send_process = Process(target=server_send, args=(client_socket,))
    server_receive_process = Process(target=server_receive, args=(client_socket,))
    server_send_process.start()
    server_receive_process.start()

if __name__ == '__main__':
    message(10000)
