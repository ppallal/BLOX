import socket               # Import socket module

s = socket.socket()
host = "192.168.1.3"        # Create a socket object
# host = socket.gethostname() # Get local machine name
port = 12121                # Reserve a port for your service.

s.connect((host, port))
print s.recv(1024)
s.close                     # Close the socket when done
