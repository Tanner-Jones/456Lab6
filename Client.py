import socket
import sys

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

def TCP_connection():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOSTNAME, Server_port))
    sock.sendall(message)
    sock.close()


def UDP_connection():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(message, (HOSTNAME, Server_port))
    sock.close()



while True:
    conn_type = input("TCP or UDP?")
    if conn_type == "TCP":
        TCP_connection()
    elif conn_type == "UDP":
        UDP_connection()
    else:
        print("Invalid input, please try again")




