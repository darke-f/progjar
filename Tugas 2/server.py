from threading import Thread
import socket
import os
import time

SERVER_IP = '127.0.0.1'
SERVER_PORT = 9000
BUFFER = 1024

images = ["darkrai.jpg","groudon.jpg","rayquaza.jpg","kyogre.jpg","giratina.jpg","arceus.jpg"]

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((SERVER_IP, SERVER_PORT))

def init():
    while True:
        print "Waiting for client..."
        data, addr = sock.recvfrom(BUFFER)
        #print "Get Command : " + str(data)
        if str(data) == "Request":
            #Create thread for every client that connects to the port
            thread = Thread(target=processImage, args=(addr))
            thread.start()

       
def processImage(ip, port):
    addr = (ip, port)
    #Iterate for every image in the array
    for x in images:
        #Image send delay
        time.sleep(10)
        sendFile(x,addr)
    sock.sendto("EXIT".ljust(BUFFER), addr)

def sendFile(imgname, addr):
    imagepath = os.path.join("./img/", imgname)
    
    fp = open(imagepath, "rb")
    files = fp.read()
    sizeSent = 0
    fp.close()
    
    sock.sendto(("START " + imgname).ljust(BUFFER), addr)
    
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
        sock.sendto(data, addr)
        print "Sending "+str(sizeSent) + "/" + str(len(files)) + " bytes To " + str(addr[0]) + ":" + str(addr[1])
    sock.sendto(("FINISHED " + imgname).ljust(1024), addr)
    
while True:
    init()