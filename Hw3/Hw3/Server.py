import socket
import threading
import os

HOST = '127.0.0.1'  
PORT = 6002       
BUFFER_SIZE = 1024
FILE_DIRECTORY = 'received_files' 

if not os.path.exists(FILE_DIRECTORY):
    os.makedirs(FILE_DIRECTORY)

def handle_client(client_socket):
    def receive_messages():
        while True:
            try:
                message = client_socket.recv(BUFFER_SIZE).decode()
                if message:
                    print(f"Client: {message}")

                    if message.startswith("FILE:"):
                        filename = message[5:]
                        file_path = os.path.join(FILE_DIRECTORY, filename)

                        with open(file_path, 'wb') as file:
                            while True:
                                chunk = client_socket.recv(BUFFER_SIZE)
                                if chunk == b'DONE':
                                    break
                                file.write(chunk)
                        print(f"File {filename} received from client.")
                        client_socket.send("File received successfully.".encode())
                    else:
                        client_socket.send("Message received.".encode())
            except Exception as e:
                print(f"Error: {e}")
                client_socket.close()
                break

    def send_messages():
        while True:
            try:
                response = input("Server: ")
                if response != "":
                    client_socket.send(response.encode())
            except Exception as e:
                print(f"Error: {e}")
                client_socket.close()
                break

    receive_thread = threading.Thread(target=receive_messages)
    send_thread = threading.Thread(target=send_messages)

    receive_thread.start()
    send_thread.start()


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)
print(f"Server listening on {HOST}:{PORT}")

while True:
    client_socket, address = server_socket.accept()
    print(f"Connected to {address}")
    client_thread = threading.Thread(target=handle_client, args=(client_socket,))
    client_thread.start()