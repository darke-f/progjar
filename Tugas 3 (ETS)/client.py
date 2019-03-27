import socket
import os

SERVER_IP = '127.0.0.1'
SERVER_PORT = 9999
BUFFER = 1024

class Connect:
    def __init__(self, conn):
        print "Hello, the commands for this program is al follows: "
        print "1. send 'filename'"
        print "2. download 'filename'"
        self.conn = conn
        self.dir = "./clientfile"
        connInfo = conn.getsockname()
        print "Connected to " + str(connInfo[0]) + ":" + str(connInfo[1])
        
        
    def run(self):
        while True:
            request = sock.recv(BUFFER).rstrip()
            print "\n" + request,
            if request[:11] == "[LISTENING]":
                cmd = raw_input()
                self.parseRequest(cmd)
            elif request[:5] == "Files":
                self.listFile()
    
    #Handle Client request        
    def parseRequest(self, request):
        if request[:4] == "send":
            self.sendFile(request[5:])
        elif request[:8] == "download":
            self.recvFile(request[9:])
            print self.recv().rstrip()
        else:
            self.send("!")
            print self.recv().rstrip()

    #Function to recieve file from server to client     
    def recvFile(self, fileName):
        self.send("GET " + fileName)
        ok = self.recv()
        if ok[:3] != "ACK":
            print "[ERROR] Invalid response : " + ok
            return
        self.send("ACK")
        filepath = os.path.join("./clientfile/", fileName)
        fp = open(filepath, "wb+")
        received = 0
        while True:
            data = self.recv()
            if data[:3] == "END":
                fp.close()
                print "End of file: " + fileName
                break
            else:
                fp.write(data) 
                received += len(data)
                print "Received "+ str(received)
    
    #Function to send file from client to server            
    def sendFile(self, name):
        fp = None
        filepath = os.path.join("./clientfile/", name)
        try:
            fp = open(filepath, "rb")
        except:
            print "[ERROR] FILE NOT FOUND"
            return
        files = fp.read()
        sizeSent = 0
        addr = self.conn.getsockname()
        fp.close()
        self.send("PUT "+name)
        signal = self.recv()
        if signal[:3] != "ACK":
            print "[ERROR] Invalid response from server"
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
        
    #List all the file int the client directory    
    def listFile(self):
        files = os.listdir(self.dir)
        result = "\nFiles that you have are: \n"
        for file in files:
            result += file + "\n"
        print result

    #Function to handle sending data from client to server
    def send(self, files):
        self.conn.send(files.ljust(BUFFER))

    #Function to handle recieveing data from server to client
    def recv(self):
        return self.conn.recv(BUFFER)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((SERVER_IP,SERVER_PORT))

#Establish connection to server
conn = Connect(sock)
conn.run()

