# Author:    Hyun Woo Kim
# Class:     CPSC471
# Professor: Alexander Gauf
# OS Used:   Kali Linux,
# IDE Used:  Pycharm (VirtualBox)

import random
from socket import *

serverSocket = socket(AF_INET, SOCK_DGRAM)          # Creating the UDP
serverSocket.bind(('',12000))                # Binding addr 127.0.0.1 and port 12000

while True:
    rand = random.randint(0,10)                     # generate int range of 0 to 10
    message, address = serverSocket.recvfrom(1024)  # receive packet with address of 1024 bytes
    message = message.upper()                       # capitalize the message from the client

    if rand < 4:
        continue
    serverSocket.sendto(message,address)

