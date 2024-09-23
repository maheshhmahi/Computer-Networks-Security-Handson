import socket			 

s = socket.socket()		 
print ("Socket successfully created")

port = 12346			

# Next bind to the port 
# we have not typed any ip in the ip field 
# instead we have inputted an empty string 
# this makes the server listen to requests 
# coming from other computers on the network 
s.bind(('', port))		 
print ("socket binded to %s" %(port)) 

# put the socket into listening mode
# 3 specifies the max number of queued connection before server starts rejecting new connections
s.listen(3)	 
print ("socket is listening")		 

# a forever loop until we interrupt it or 
# an error occurs 
connection_count = 0
while True: 

    # Establish connection with client. 
    client, addr = s.accept()	 

    connection_count += 1
    print(f"Got connection from {addr}, Total connections: {connection_count}")

    # send a thank you message to the client. encoding to send byte type. 
    client.send(f'Thank you for connecting! You are client number {connection_count}'.encode())

    # Close the connection with the client 
    client.close()

    if connection_count >= 5:
        print("Reached maximum connections, stopping server.")
        break




# testing: run this code, and from terminal try to run the below command

# telnet localhost 12346
