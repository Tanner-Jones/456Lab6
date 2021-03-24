import socket
import time


# Ports and IP initialization
IP = socket.gethostname()
print(IP)
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

def get_details(message):
    message = message.replace("Execution Count:", '')
    count = message[0:message.index("Time delay:")]
    message = message[message.index("Time delay:"):]
    message = message.replace("Time delay:", '')
    delay = message[0:message.index("Command")]
    message = message[message.index("Command:"):]
    message = message.replace("Command", '')
    command = message
    return count, delay, command

def UDP_server():
    #Loop to wait for received messages
    print("Waiting for Connection:")
    UDPdata, UDPaddr = UDPsock.recvfrom(1024)
    message = UDPdata.decode("utf-8")
    count, delay, command = get_details(message)
    print("trimmed message")
    print(count, delay, command)
    # prints message to ask user about acceptance

def TCP_server():
    #Loop to wait for received messages
    TCPsock.listen(5)
    TCPconn, TCPaddr = TCPsock.accept()
    print("Waiting for Connection:")
    TCPdata = TCPconn.recv(1024)

    # prints message to ask user about acceptance

while True:
    server_type = input("UDP Server or TCP Server? UDP/TCP\n")

    if server_type == "UDP":
        UDP_server()
    elif server_type == "TCP":
        TCP_server()
    else:
        print("Invalid Entry, please try again")









