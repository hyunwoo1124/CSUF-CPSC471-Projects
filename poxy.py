import sys
from socket import *



# if len(sys.argv) <= 1:
    # print('Usage : "python ProxyServer.py server_ip"\n[server_ip : It is the IP Address Of Proxy Server')

   # sys.exit(2)
# Create a server socket, bind it to a port and start listening

tcpSerSock = socket(AF_INET, SOCK_STREAM)
# Fill in start.
tcpSerPort = 8888
serverIp = 'localhost'
# prepare a server socket

tcpSerSock.bind((serverIp, tcpSerPort))
tcpSerSock.listen(5)

# Fill in end.
while True:
    # Strat receiving data from the client
    print('Ready to serve...')
    tcpCliSock, addr = tcpSerSock.accept()
    print(('Received a connection from:', addr))
    message = tcpCliSock.recv(1024).decode()  # Fill in start. # Fill in end.

    print(message)
    # Extract the filename from the given message
    print((message.split()[1]))

    filename = message.split()[1].partition("/")[2]

    print(filename)
    fileExist = "false"
    filetouse = "/" + filename
    print(filetouse)
    try:
        # Check wether the file exist in the cache
        f = open(filetouse[1:], "rb")
        outputdata = f.readlines()
        fileExist = "true"
        # ProxyServer finds a cache hit and generates a response message
        tcpCliSock.send('HTTP/1.0 200 OK\r\n\r\n'.encode())
        tcpCliSock.send('Content-Type:text/html\r\n\r\n'.encode())
        # Fill in start.
        # Send the content of the requested file to the connection socket
        for i in range(0, len(outputdata)):
            tcpCliSock.send(outputdata[i])

        # Fill in end.
        print('Read from cache')
    # Error handling for file not found in cache
    except IOError:
        print(('File Exist: ', fileExist))

        if fileExist == "false":
            # Create a socket on the proxyserver
            print('Creating socket on proxyserver')
            c = socket(AF_INET, SOCK_STREAM)  # Fill in start. # Fill in end.
            hostn = filename.replace("www.", '', 1)
            print(hostn)
            print(filename)
            try:
                # Connect to the socket to port 80
                # Fill in start.
                c.connect((hostn, 80))
                print('socket connected to port 80')
                print(('successful connection with', hostn))

                # Fill in end.
                # Create a temporary file on this socket and ask port 80 for the file requested by the client

                fileobj = c.makefile('rwb', 0)

                print(("GET " + "http://" + filename + "/HTTP/1.0\n\n"))
                # error saying it write with out w

                fileobj.write("GET ".encode() + "http://".encode() + filename.encode() + " HTTP/1.0\n\n".encode())

                print(fileobj)
                # Read the response into buffer
                # Fill in start.
                # if i change HTTP/1.0\n\n to HTTP/1.1\n\n it stops at this line
                buff = fileobj.readlines()
                print(buff)

                # Fill in end.
                # Create a new file in the cache for the requested file.
                # Also send the response in the buffer to client socket
                # and the corresponding file in the cache
                tmpFile = open("./" + filename, "wb")
                # Fill in start.
                for i in buff:
                    tmpFile.write(i)
                    tcpCliSock.send(i)

            # Fill in end.
            except Exception as e:
                print(("Illegal request", e))
        else:
            # HTTP response message for file not found
            # Fill in start.
            print('file not found')

    # Fill in end.
    # Close the client and the server sockets
    tcpCliSock.close()
# Fill in start.
tcpSerSock.close()
# Fill in end.
