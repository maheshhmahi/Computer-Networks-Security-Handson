import socket
import threading
import os

# Server configuration
HOST = '127.0.0.1'  # Localhost
PORT = 6000        # Arbitrary non-privileged port
BUFFER_SIZE = 1024

# Function to handle server messages
def handle_server(server_socket):
    def receive_messages():
        while True:
            try:
                # Receive message from server
                message = server_socket.recv(BUFFER_SIZE).decode()
                if message:
                    print(f"Server: {message}")
            except Exception as e:
                print(f"Error: {e}")
                server_socket.close()
                break

    def send_messages():
        while True:
            try:
                message = input("Client: ")
                if message == "EXIT":
                    break
                elif message.startswith("FILE:"):
                    filename = message[5:]
                    file_path = input("Enter file path: ")

                    if os.path.exists(file_path):
                        server_socket.send(f"FILE:{os.path.basename(filename)}".encode())
                        with open(file_path, 'rb') as file:
                            chunk = file.read(BUFFER_SIZE)
                            while chunk:
                                server_socket.send(chunk)
                                chunk = file.read(BUFFER_SIZE)
                        server_socket.send(b'DONE')
                        print(f"File {filename} sent to server.")
                        server_socket.recv(BUFFER_SIZE).decode()  # Wait for server response
                    else:
                        print("File not found.")
                else:
                    server_socket.send(message.encode())
                    server_socket.recv(BUFFER_SIZE).decode()  # Wait for server response
            except Exception as e:
                print(f"Error: {e}")
                server_socket.close()
                break

    receive_thread = threading.Thread(target=receive_messages)
    send_thread = threading.Thread(target=send_messages)

    receive_thread.start()
    send_thread.start()

# Create client socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))
print(f"Connected to {HOST}:{PORT}")

handle_server(client_socket)