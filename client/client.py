import socket
from client.features import interact_with_server


class Client:
    def __init__(self, host='127.0.0.1', port=5555):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))
        print(f"Connected to server at {host}:{port}")

    def start(self):
        interact_with_server(self.client)


if __name__ == "__main__":
    client = Client()
    client.start()
