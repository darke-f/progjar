import socket
import os

TARGET_IP = "127.0.0.1"
TARGET_PORT = 9000
BUFFER = 1024
savefolder ="./Client_3/"

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

fp = None
fileName = None
received = 0

print "Sending Request"
sock.sendto("Request", (TARGET_IP, TARGET_PORT))

while True:
    data, addr = sock.recvfrom(BUFFER)
    #Check if server starts sending data
    if data[:5] == "START":
        #print (data)
        #remove padded spaces from filename
        filename = data[6:].replace(" ", "")
        received = 0
        #Set save folder for client
        savepath = os.path.join(savefolder, filename)
        fp = open(filename, "wb+")
        print "Start recieving : " + filename
    #Check if the data transfer is finished
    elif data[:8] == "FINISHED":
        fp.close()
        print "Finished recieving : " + filename
    #Check if the process if finished
    elif data[:4] == "EXIT":
        print "Closing connection"
        break
    else:
        fp.write(data)
        received += len(data)
        print "Received " + str(received) + "bytes of data"
        
print "Operation Finished Successfully"