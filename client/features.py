import cv2
import socket
import pickle
import struct
import pyautogui
import numpy as np


def interact_with_server(client_socket):
    try:
        while True:
            message = input("Enter message to send to server: ")
            client_socket.send(message.encode('utf-8'))
            response = client_socket.recv(1024).decode('utf-8')
            print(f"Received from server: {response}")
            if message.lower() == 'exit':
                break
    except socket.error as e:
        print(f"Socket error: {e}")
    finally:
        client_socket.close()


def start_video_stream_client(host='127.0.0.1', port=9999):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    print(f"Connected to video stream server at {host}:{port}")

    while True:
        # Capture the screen
        screenshot = pyautogui.screenshot()
        frame = np.array(screenshot)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Encode the frame
        encoded, buffer = cv2.imencode('.jpg', frame)
        data = pickle.dumps(buffer)
        message_size = struct.pack("L", len(data))
        
        client_socket.sendall(message_size + data)


if __name__ == "__main__":
    start_video_stream_client()
