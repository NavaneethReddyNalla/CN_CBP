import socket
import threading
from server.handlers import handle_client

class Server:
    def __init__(self, host='0.0.0.0', port=5555):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server.bind((host, port))
        self.server.listen(5)
        print(f"Server listening on {host}:{port}")

    def start(self):
        while True:
            client_socket, client_address = self.server.accept()
            print(f"Accepted connection from {client_address}")
            client_handler = threading.Thread(target=handle_client, args=(client_socket,))
            client_handler.start()

if __name__ == "__main__":
    server = Server()
    server.start()
