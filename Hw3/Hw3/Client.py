import socket
import threading
import os

# Server configuration
HOST = '127.0.0.1'  # Localhost
PORT = 12345        # Arbitrary non-privileged port
BUFFER_SIZE = 1024

# Function to handle server messages
def handle_server(server_socket):
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

# Create client socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))
print(f"Connected to {HOST}:{PORT}")

# Start thread to handle server messages
server_thread = threading.Thread(target=handle_server, args=(client_socket,))
server_thread.start()

while True:
    message = input("Client: ")
    client_socket.send(message.encode())

    # Check if file transfer is requested
    if message.startswith("FILE:"):
        filename = message[5:]
        file_path = os.path.join(os.getcwd(), filename)
        if os.path.exists(file_path):
            with open(file_path, 'rb') as file:
                client_socket.sendfile(file)
            print(f"File {filename} sent to server.")
        else:
            print("File not found.")