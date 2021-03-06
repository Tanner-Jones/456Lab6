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
check = b''

def rcend_thread():
    # thread to handle when something else is received
    global check
    check = TCPconn.recv(1024)

def run_command(count, delay, command, addr):
    # command run
    for i in range(0,int(count)):
        if server_type == "TCP":
            if check.decode('utf-8') == "rcend":
                break
        command_list = command.split(" ")
        if len(command_list) > 1:
            ran = subprocess.Popen([command_list[0], command_list[1]], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        else:
            # loop for execution times
            ran = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, err = ran.communicate()
        output_s = output.decode("utf-8")
        print(time.strftime('%X %x'), output_s)
        output_s = addr + "\n" + output_s + time.strftime('%X %x') + "\n\n"
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
    run_command(count, delay, command, UDPaddr[0])

    UDPsock_send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    f = open("output", 'rb')
    send_message = bytearray(f.read())
    while len(send_message) > 0:
        message = bytes(send_message[0:1024])
        UDPsock_send.sendto(message, (UDPaddr[0], PORT))
        send_message = send_message[1024:]
    # prints message to ask user about acceptance

def TCP_server():
    # block sets up socket and receives command
    TCPsock.listen(5)
    global TCPconn
    global TCPaddr
    TCPconn, TCPaddr = TCPsock.accept()
    th.Thread(target=rcend_thread, args=(), name='key_capture_thread', daemon=True).start()
    print("Waiting for Connection:")
    TCPdata = TCPconn.recv(1024)
    message = TCPdata.decode("utf-8")
    # collects the three relevant details from message and runs the command
    count, delay, command = get_details(message)
    run_command(count, delay, command, TCPaddr[0])

    # reads output and sends back to client
    f = open("output", 'rb')
    send_message = f.read()
    TCPconn.sendall(send_message)
    # prints message to ask user about acceptance


while True:
    f = open("output", 'w')

    server_type = input("UDP Server or TCP Server? UDP/TCP\n")

    if server_type == "UDP":
        UDP_server()
    elif server_type == "TCP":
        TCP_server()
    else:
        print("Invalid Entry, please try again")









