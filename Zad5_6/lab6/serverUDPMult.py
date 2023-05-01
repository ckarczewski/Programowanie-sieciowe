import socket
import argparse 
import sys
import struct

def echo_server(port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    except socket.error as e: 
        print ("Error creating socket: %s" % e) 
        sys.exit(1) 

    try:
        sock.bind(("0.0.0.0", port))
        
    except socket.error as e: 
        print ("Error creating socket: %s" % e) 
        sys.exit(1) 
        
    mreq = struct.pack("4sl", socket.inet_aton("0.0.0.0"), socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    return sock



def receive(sock):
    while True:
        print("Waiting for message")
        data, address = sock.recvfrom(48)
        if not data:
            print("Client disconnected")
            break
        if data == "End":
            print ("Closing connection to the server") 
            sock.close()
            break
        elif data:
            print(f"Message: {data}")
            sock.sendto(data, address)
            print(f"Send data back to {address}")
if __name__ == '__main__':
    while True:
        command = input('Enter a command (start, stop)')
        if command == 'start':
            port = input('Enter a port ')
            port = int(port)
            print('Starting the server')
            addr = echo_server(port)
            receive(addr)
        if command == 'stop':
            echo_server.close()
            print('Server stopped')

            break
    print('Application finished')
