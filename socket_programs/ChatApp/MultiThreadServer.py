import socket
import threading

# Function to handle individual client connections
def handle_client(conn, address):
    print(f"Connection from: {address}")
    while True:
        try:
            # Receive data from the client
            data = conn.recv(1024).decode()
            if not data:
                # If no data is received, client has disconnected
                break
            print(f"From connected user {address}: {data}")
            
            # Input response from the server (for demonstration purposes)
            data_to_send = input(' -> ')
            conn.send(data_to_send.encode())  # Send response to the client
        except:
            # Handle any connection errors
            break
    
    # Close the connection when done
    conn.close()
    print(f"Connection closed for {address}")

# Main server program
def server_program():
    host = socket.gethostname()  # Get the hostname
    port = 5000  # Port to listen on

    server_socket = socket.socket()  # Create socket instance
    server_socket.bind((host, port))  # Bind the socket to host and port
    server_socket.listen(5)  # Listen for up to 5 connections

    print(f"Server is listening on port {port}")

    # Accept multiple connections in a loop
    while True:
        conn, address = server_socket.accept()  # Accept new connection
        # Create a new thread for each client connection
        client_thread = threading.Thread(target=handle_client, args=(conn, address))
        client_thread.start()  # Start the thread for the client

# Run the server program
if __name__ == '__main__':
    server_program()
