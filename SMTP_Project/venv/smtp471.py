import socket
import ssl
import base64

# To send email with Google's SMTP server, you have to login using
# a gmail account. The account with the credentials below was made
# for this assignment.
username = "mr6network9@gmail.com"
password = "cpsc471project"

# Email address to send the email to.
sentTo = "zvongrote@csu.fullerton.edu"

msg = "I love computer networks!"
endmsg = "\r\n.\r\n"

# Choose a mail server (e.g. Google mail server) and call it mailserver
mailserver = ("smtp.gmail.com", 587)

# Create socket called clientSocket and establish a TCP connection with mailserver.
# The socket is used as a context manager inside the 'with' statement.
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as clientSocket:

    # Try to connect with the mail server
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
    authUserRecv = sslClientSocket.recv(1024).decode()
    print(f"Response form server after AUTH LOGIN: {authUserRecv}")  # Expecting a 334 response code

    # Encode and send the username
    encodedUsername = base64.b64encode(username.encode())
    sslClientSocket.sendall(encodedUsername + "\r\n".encode())
    recv_auth_username = sslClientSocket.recv(1024).decode()
    print(f"Response after sending username: {recv_auth_username}")  # Expecting a 334 response code

    # Encode and send the password
    encodedPassword = base64.b64encode(password.encode())
    sslClientSocket.sendall(encodedPassword + "\r\n".encode())
    recv_auth_password = sslClientSocket.recv(1024).decode()
    print(f"Response after sending password: {recv_auth_password}")  # Expecting a 235 response code

    # Send MAIL FROM command with the name of the email address
    # sending the email, then print server response.
    mailFrom = f"MAIL FROM: <{username}>\r\n"
    sslClientSocket.sendall(mailFrom.encode())
    mailFromResponse = sslClientSocket.recv(1024).decode()
    print(f"Response from server after MAIL FROM: {mailFromResponse}")

    # Send RCPT TO command with the email address to send the email to,
    # then print server response.
    rcptTo = f"RCPT TO: <{sentTo}>\r\n"
    sslClientSocket.sendall(rcptTo.encode())
    rcptToResponse = sslClientSocket.recv(1024).decode()
    print(f"Response from server after RCPT TO: {rcptToResponse}")

    # Send DATA command with message body with terminating sequence,
    # then print server response.
    sslClientSocket.sendall("DATA\r\n".encode())
    sslClientSocket.sendall(f"{msg}{endmsg}".encode())
    dataResponse = sslClientSocket.recv(1024).decode()
    print(f"Response from server after DATA: {dataResponse}")

    # Terminate the connection to the SMTP ser by
    # sending the quit message, and print server response
    sslClientSocket.sendall("QUIT \r\n".encode())
    quitResponse = sslClientSocket.recv(1024).decode()
    print(f"Response form server after QUIT: {quitResponse}")
