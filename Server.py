import socket
import time
import subprocess
import sys
import threading as th

# Ports and IP initialization
IP = socket.gethostname()
print(IP)
TCP_PORT_RECEIVE = 5005
TCP_PORT_SEND = 4444
UDP_PORT_RECEIVE = 5006
UDP_PORT_SEND = 4445
PORT = int(sys.argv[1])

#creates socket object for TCP
TCPsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
TCPsock.bind((IP, PORT))

# Creates socket for UDP
UDPsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
UDPsock.bind((IP, PORT))

# output file to write to
f = open("output", 'w')
check = b''

def rcend_thread():
    # thread to handle when something else is received
    global check
    check = TCPconn.recv(1024)

def run_command(count, delay, command):
    # command run
    for i in range(0,int(count)):
        if server_type == "TCP":
            if check.decode('utf-8') == "rcend":
                break
        # loop for execution times
        ran = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, err = ran.communicate()
        output_s = output.decode("utf-8")
        print(time.strftime('%X %x'), output_s)
        output_s = output_s + time.strftime('%X %x') + "\n"
        f.write(output_s)
        time.sleep(int(delay))
    f.close()

def get_details(message):
    message = message.replace("Execution Count:", '')
    count = message[0:message.index("Time delay:")]
    message = message[message.index("Time delay:"):]
    message = message.replace("Time delay:", '')
    delay = message[0:message.index("Command")]
    message = message[message.index("Command:"):]
    message = message.replace("Command:", '')
    command = message
    return count, delay, command

def UDP_server():
    print("Waiting for Connection:")
    UDPdata, UDPaddr = UDPsock.recvfrom(1024)
    message = UDPdata.decode("utf-8")
    count, delay, command = get_details(message)
    run_command(count, delay, command)

    f = open("output", 'rb')
    send_message = f.read()

    UDPsock.close()
    UDPsock_send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    UDPsock_send.sendto(send_message, (UDPaddr[0], PORT))
    # prints message to ask user about acceptance

def TCP_server():
    th.Thread(target=rcend_thread, args=(), name='key_capture_thread', daemon=True).start()
    # block sets up socket and receives command
    TCPsock.listen(5)
    global TCPconn
    TCPconn, TCPaddr = TCPsock.accept()
    print("Waiting for Connection:")
    TCPdata = TCPconn.recv(1024)
    message = TCPdata.decode("utf-8")
    # collects the three relevant details from message and runs the command
    count, delay, command = get_details(message)
    run_command(count, delay, command)

    # reads output and sends back to client
    f = open("output", 'rb')
    send_message = f.read()
    TCPconn.sendall(send_message)
    # prints message to ask user about acceptance
    TCPsock.close()


while True:
    server_type = input("UDP Server or TCP Server? UDP/TCP\n")

    if server_type == "UDP":
        UDP_server()
    elif server_type == "TCP":
        TCP_server()
    else:
        print("Invalid Entry, please try again")









