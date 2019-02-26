import sys
import socket

# Create a TCP/IP socket
# SOCK_STREAM = TCP, SOCK_DGRAM = UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip = 'localhost'
port = 10000

# Bind the socket to the port
server_address = (ip, port)
print ('Starting up listener on %s port %s' % server_address)
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

while True:
    # Wait for a connection
    print ('Waiting for incoming connection')
    connection, client_address = sock.accept()
    print ('Incoming connection from', client_address)
    # Receive the data in small chunks and retransmit it
    while True:
        data = connection.recv(32)
        print ('Received data : "%s"' % data)
        if data:
            print ('Sending data back to the client!')
            connection.sendall('-->'+data)
        else:
            print ('No more data from ', client_address)
            break
        # Clean up the connection
    connection.close()