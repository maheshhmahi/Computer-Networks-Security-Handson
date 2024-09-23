# An example script to connect to Google using socket 
# programming in Python 
import socket # for socket 
import sys 

try: 
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
	print ("Socket successfully created")
except socket.error as err: 
	print ("socket creation failed with error %s" %(err))

port = 80

try: 
	host_ip = socket.gethostbyname('www.google.com') 
except socket.gaierror: 

	print ("there was an error resolving the host")
	sys.exit() 

s.connect((host_ip, port)) 

print ("the socket has successfully connected to google") 
