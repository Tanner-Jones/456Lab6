import socket
import time


# Ports and IP initialization
IP = socket.gethostname()
TCP_PORT_RECEIVE = 5005
TCP_PORT_SEND = 4444
UDP_PORT_RECEIVE = 5006
UDP_PORT_SEND = 4445

#creates socket object for TCP
TCPsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
TCPsock.bind((IP, TCP_PORT_RECEIVE))

# Creates socket for UDP
UDPsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
UDPsock.bind((IP, UDP_PORT_RECEIVE))


while True:
    #Loop to wait for received messages
    TCPsock.listen(5)
    TCPconn, TCPaddr = TCPsock.accept()
    UDPconn, UDPaddr = UDPsock.accept()
    print("Waiting for Connection:")
    TCPdata = TCPconn.recv(1024)
    UDPdata = UDPconn.recv(1024)
    print(UDPdata)
    print(TCPdata)
    # prints message to ask user about acceptance










