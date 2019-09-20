# Author:    Hyun Woo Kim
# Class:     CPSC471
# Professor: Alexander Gauf
# OS Used:   Kali Linux,
# IDE Used:  Pycharm (VirtualBox)

from datetime import *
from socket import*

serverAddress = 'Localhost'
port = 12000                                                # using the same port number mentioned in server.py
clientSocket = socket(AF_INET,SOCK_DGRAM)                   # Initializing socket
clientMessage = "Ping"

for x in range(10):                                          # Using for loop to run 10 randomly generated num
    print ("Ping attempt: ", x, " running.\n")
    dateTime = datetime.now()                               # using variable to store the exact time of the moment
    clientSocket.sendto(clientMessage.encode(),(serverAddress, port))      # sending the message to this server and port
    clientSocket.settimeout(1)                              # time out 1 sec. If more than 1 second it will be considered lost
    try:
        serverMessage, receivedAddress = clientSocket.recvfrom(1024)  # receiving message with max 1024 bytes
        dateTimeFinal = datetime.now()
        RTT = dateTimeFinal - dateTime
        print(serverMessage)
        print("Time elapsed: ", RTT.microseconds, "microseconds\n")
    except timeout:
        print ("Sorry it took more than a second... time out...")
clientSocket.close()                                            #closing the socket


