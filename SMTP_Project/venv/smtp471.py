import socket
import ssl

msg = "\r\n I love computer networks!"
endmsg = "\r\n.\r\n"

# Choose a mail server (e.g. Google mail server) and call it mailserver
mailserver = ("smtp.gmail.com", 587)

# Create socket called clientSocket and establish a TCP connection with mailserver
# Uses 'with' so that the socket will always be closed
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as clientSocket:
    clientSocket.connect(mailserver)

    recv = clientSocket.recv(1024).decode()
    print(recv)
    if recv[:3] != '220':
        print('220 reply not received from server.')

    # Send HELO command and print server response.
    heloCommand = 'HELO Alice\r\n'
    clientSocket.sendall(heloCommand.encode())
    recv1 = clientSocket.recv(1024).decode()
    print(recv1)
    if recv1[:3] != '250':
        print('250 reply not received from server.')

    # Send STARTTLS and print server response
    startTLS = "STARTTLS\r\n"
    clientSocket.sendall(startTLS.encode())
    tlsRecv = clientSocket.recv(1024)
    print(f"Response from server after STARTTLS: {tlsRecv.decode()}")

    # Wrap the socket with ssl
    sslClientSocket = ssl.wrap_socket(clientSocket)

    # Ask to authorize the user and print reply
    authUser = "AUTH LOGIN\r\n"
    sslClientSocket.sendall(authUser.encode())
    authUserRecv = sslClientSocket.recv(1024)
    print(f"Response form server after AUTH LOGIN: {authUserRecv.decode()}") # Looking for a 334 response code

    # Send MAIL FROM command and print server response.
    # mailFrom = "MAIL FROM: <me@test.com>\r\n"
    # sslClientSocket.sendall(mailFrom.encode())
    # mailFromResponse = sslClientSocket.recv(1024)
    # print(f"Response from server after MAIL FROM: {mailFromResponse.decode()}")