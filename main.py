

import socket
import cv2
import pickle
import struct
import time
from multiprocessing import Process
import threading
import psutil

def send_frames(port_no, cam):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host_ip = '192.168.1.112'  # Server's IP address
    port = port_no
    socket_address = (host_ip, port)

    try:
        server_socket.bind(socket_address)
        server_socket.listen(5)
        print(f"Listening on {socket_address}")

        client_socket, addr = server_socket.accept()
        print(f"Connection from: {addr}")

        cap = cv2.VideoCapture(cam)
        cv2.namedWindow(f"Camera {port_no}", cv2.WINDOW_NORMAL)

        start_time = time.time()
        frame_count = 0

        while True:
            ret, frame = cap.read()
            cv2.imshow(f"Camera {port_no}", frame)

            data = pickle.dumps(frame)
            msg_size = struct.pack("Q", len(data))
            client_socket.sendall(msg_size)
            client_socket.sendall(data)

            frame_count += 1
            if frame_count >= 10:
                end_time = time.time()
                fps = frame_count / (end_time - start_time)
                print(f"Camera {port_no} - FPS: {fps:.2f}")
                frame_count = 0
                start_time = end_time

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cap.release()
        cv2.destroyAllWindows()
        client_socket.close()
        server_socket.close()

def message(port_no):
    def server_send(client_socket):
        while True:
            message = input()
            client_socket.send(message.encode())

    def server_receive(client_socket):
        while True:
            data = client_socket.recv(1024)
            print("Client (Received): " + data.decode())

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('192.168.137.40', port_no))
    server_socket.listen(1)
    print("Server is waiting for a connection...")
    client_socket, addr = server_socket.accept()

    # Create and start server threads for messaging
    server_send_thread = threading.Thread(target=server_send, args=(client_socket,))
    server_receive_thread = threading.Thread(target=server_receive, args=(client_socket,))
    server_send_thread.start()
    server_receive_thread.start()

if __name__ == '__main__':
    camera_threads = {
        9998: 0,
        9999: 1,
    }

    processes = {}

    for port, cam in camera_threads.items():
        process = Process(target=send_frames, args=(port, cam))
        processes[process] = processes.get(process,0)
        process.start()
        process_id = process.pid
        process = psutil.Process(process_id)
        process.nice(1)


    process = Process(target=message, args=(10000,))
    processes[process] = processes.get(process,0)
    process.start()
    process_id = process.pid
    process = psutil.Process(process_id)

    process.nice(10)   
    

    for process in processes.keys():
        process.join()
