import cv2
import socket
import struct
import pickle
import numpy as np


def handle_client(client_socket):
    try:
        while True:
            request = client_socket.recv(1024).decode('utf-8')
            if not request:
                break
            print(f"Received: {request}")
            # Handle the request here (to be expanded later)
            response = "ACK"
            client_socket.send(response.encode('utf-8'))
    except socket.error as e:
        print(f"Socket error: {e}")
    finally:
        client_socket.close()


def start_video_stream_server(host='0.0.0.0', port=9999):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Video stream server listening on {host}:{port}")

    conn, addr = server_socket.accept()
    print(f"Accepted connection from {addr}")

    data = b""
    payload_size = struct.calcsize("L")

    while True:
        while len(data) < payload_size:
            packet = conn.recv(4*1024)  # 4K
            if not packet:
                break
            data += packet
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("L", packed_msg_size)[0]

        while len(data) < msg_size:
            data += conn.recv(4*1024)
        frame_data = data[:msg_size]
        data = data[msg_size:]

        frame = pickle.loads(frame_data)
        frame = cv2.imdecode(np.frombuffer(frame, dtype=np.uint8), cv2.IMREAD_COLOR)

        cv2.imshow('Video Stream', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    conn.close()
    server_socket.close()
    cv2.destroyAllWindows()
