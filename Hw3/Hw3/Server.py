import socket
import threading
import os

# Server configuration
HOST = '127.0.0.1'  # Localhost
PORT = 12345        # Arbitrary non-privileged port
BUFFER_SIZE = 1024

# Function to handle client connections
def handle_client(client_socket):
    while True:
        try:
            # Receive message from client
            message = client_socket.recv(BUFFER_SIZE).decode()
            if message:
                print(f"Client: {message}")

                # Check if file transfer is requested
                if message.startswith("FILE:"):
                    filename = message[5:]
                    file_path = os.path.join(os.getcwd(), filename)
                    if os.path.exists(file_path):
                        with open(file_path, 'rb') as file:
                            client_socket.sendfile(file)
                        print(f"File {filename} sent to client.")
                    else:
                        client_socket.send("File not found.".encode())
                else:
                    # Send response back to client
                    response = input("Server: ")
                    client_socket.send(response.encode())
        except Exception as e:
            print(f"Error: {e}")
            client_socket.close()
            break

# Create server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)
print(f"Server listening on {HOST}:{PORT}")

while True:
    client_socket, address = server_socket.accept()
    print(f"Connected to {address}")
    client_thread = threading.Thread(target=handle_client, args=(client_socket,))
    client_thread.start()