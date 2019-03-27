import threading
import socket
import os

SERVER_IP = '127.0.0.1'
SERVER_PORT = 9999
BUFFER = 1024

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((SERVER_IP, SERVER_PORT))

print "Server starting up on " , SERVER_IP , " on Port " , SERVER_PORT
sock.listen(1)

class clients:
    def __init__(self,conn):
        self.conn = conn
        self.dir = "./serverfile"
        
    #Handle recieved request
    def handleRequest(self):
        while True:
            self.listFile()
            self.send("[LISTENING] Insert your command below: ")
            data = self.conn.recv(BUFFER)
            sockInfo = self.conn.getsockname()
            if len(data) == 0:
                print "Closing connection with " + str(sockInfo[0]) + ":" + str(sockInfo[1])
                return
            else:
                self.parseRequest(data)
                
    def parseRequest(self, request):
        if request[:3] == "GET":
            self.sendFile(request[4:].rstrip())
        elif request[:3] == "PUT":
            self.recieveFile(request[4:].rstrip())
        else:
            self.send("[ERROR] No matching request")

    #Function to recieve file from client to server   
    def recieveFile(self, fileName):
        filepath = os.path.join("./serverfile/", fileName)
        fp = open(filepath, "wb+")
        self.send("ACK")
        received = 0
        while True:
            data = self.recv()
            if data[:3] == "END":
                fp.close()
                print "End of " + fileName
                break
            else:
                fp.write(data) 
                received += len(data)
                print "Received "+ str(received)

    #Function to send file from server to client       
    def sendFile(self, name):
        fp = None
        try:
            fp = open(self.dir + "/" + name, "rb")
            self.send("ACK")
        except e:
            self.send("[ERROR] " + e)
            return
        files = fp.read()
        sizeSent = 0
        addr = self.conn.getsockname()
        fp.close()
        while True:
            signal = self.recv()
            if signal[:3] == "ACK":
                break
            else:
                return
                
        #Number of iteration is the mutiple of the buffer size, in this case 1024
        iterate=(len(files)/BUFFER)
        for i in range(iterate + 1):
            data = []
            #Check if is the last buffer that will be sent
            if (i+1)*BUFFER > len(files):
                #Set buffer as the last available data
                data = files[i*BUFFER:len(files)]
                sizeSent += len(data)
                #Pad the unnocupied buffer with zeroes
                data.ljust(BUFFER)
            else:
                #Set buffer as the data with the buffer length for every iteration
                data = files[i*BUFFER:(i+1)*BUFFER]
                sizeSent += len(data)
            self.send(data)
            print "Sending "+str(sizeSent) + " OF " + str(len(files)) + " To " + str(addr[0]) + ":" + str(addr[1])
        self.send("END")

    #List all the file int the server directory  
    def listFile(self):
        files = os.listdir(self.dir)
        res = "Files on the server are: \n"
        for file in files:
            res += file + "\n"
        self.send(res)
    
    #Function to handle sending data from server to client
    def send(self, packet):
        self.conn.send(packet.ljust(BUFFER))

    #Function to handle recieving data from server to client
    def recv(self):
        return self.conn.recv(BUFFER)

while True:
    print "Waiting for client connection..."
    conn, addr = sock.accept()
    print 'Incoming connection from', addr
    clients = clients(conn)
    thread = threading.Thread(target=clients.handleRequest)
    thread.start()