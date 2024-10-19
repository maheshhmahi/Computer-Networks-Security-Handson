import socket
import threading
import os

HOST = '127.0.0.1' 
PORT = 6002       
BUFFER_SIZE = 1024

def handle_server(server_socket):
    def receive_messages():
        while True:
            try:
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
                    file_path = message[5:]

                    if os.path.exists(file_path):
                        filename = os.path.basename(file_path)
                        server_socket.send(f"FILE:{filename}".encode())
                        with open(file_path, 'rb') as file:
                            chunk = file.read(BUFFER_SIZE)
                            while chunk:
                                server_socket.send(chunk)
                                chunk = file.read(BUFFER_SIZE)
                        server_socket.send(b'DONE')
                        print(f"File {filename} sent to server.")
                        server_socket.recv(BUFFER_SIZE).decode()  
                    else:
                        print("File not found.")
                else:
                    server_socket.send(message.encode())
                    server_socket.recv(BUFFER_SIZE).decode() 
            except Exception as e:
                print(f"Error: {e}")
                server_socket.close()
                break

    receive_thread = threading.Thread(target=receive_messages)
    send_thread = threading.Thread(target=send_messages)

    receive_thread.start()
    send_thread.start()

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))
print(f"Connected to {HOST}:{PORT}")

handle_server(client_socket)