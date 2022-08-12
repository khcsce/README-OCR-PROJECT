import socket               # Import socket module

s = socket.socket()         # Create a socket object
host = 'localhost'  # Get local machine name
port = 12345                 # Reserve a port for your service.

s.connect((host, port))
#s.send("Hello server!")
f = open('image1.jpg', 'rb')
print('Sending...')
l = f.read(4096)
while (l):
    print('Sending...')
    s.send(l)
    l = f.read(4096)
f.close()
print("Done Sending")
# print(s.recv(4096))
s.close                     # Close the socket when done
