import socket
import sys
import threading as th
import time

# collect all command line arguments
Server_name = sys.argv[1]
Server_port = int(sys.argv[2])
Execution_count = sys.argv[3]
Time_delay = sys.argv[4]
command = sys.argv[5]

# create a few necessary variables for rest of program
HOSTNAME = socket.gethostbyname(Server_name)
message = "Execution Count:" + Execution_count + "Time delay:" + Time_delay + "Command:" + command
message = bytes(message, encoding="utf-8")

check = ''
data = b''

def rcend_thread():
    # thread to check for rcend command
    global check
    check = input()


def TCP_connection():
    th.Thread(target=rcend_thread, args=(), name='key_capture_thread', daemon=True).start()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOSTNAME, Server_port))
    sock.sendall(message)
    end_time = time.time() + int(Execution_count) * int(Time_delay) - 2
    sock.settimeout(5)
    display = ""
    while True:
        if time.time() > end_time:
            break
        if check == "rcend":
            sock.sendall(b'rcend')
            break

    while True:
        try:
            data = sock.recvfrom(1024)
            display = display + data[0].decode("utf-8")
        except socket.timeout:
            break
        except socket.error:
            break
    print(display)
    sock.close()


def UDP_connection():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(message, (HOSTNAME, Server_port))
    sock.close()
    sock_receive = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock_receive.bind((socket.gethostname(), Server_port))
    UDPdata, UDPaddr = sock_receive.recvfrom(1024)
    display = UDPdata.decode("utf-8")
    sock_receive.settimeout(3)
    while True:
        try:
            UDPdata, UDPaddr = sock_receive.recvfrom(1024)
            display = display + UDPdata.decode("utf-8")
        except socket.timeout:
            break
        except socket.error:
            break
    print(display)
    sock_receive.close()

conn_type = input("TCP or UDP?\n")
if conn_type == "TCP":
    TCP_connection()
elif conn_type == "UDP":
    UDP_connection()
else:
    print("Invalid input, please try again")




