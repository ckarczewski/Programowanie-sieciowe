import socket
import argparse 
import sys

def echo_server(port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    except socket.error as e: 
        print ("Error creating socket: %s" % e) 
        sys.exit(1) 

    try:
        sock.bind(("0.0.0.0", port))
    except socket.error as e: 
        print ("Error creating socket: %s" % e) 
        sys.exit(1) 
    
    while True:
        print("Waiting for message")

        data, address = sock.recv(16)
        if not data:
            print("Client disconnected")
            break
        if data == "End":
            print ("Closing connection to the server") 
            sock.close()
            break
        elif data:
            print(f"Message: {data}")
            sock.send(data)
            print(f"Send data back to {address}")
            
if __name__ == '__main__':
    while True:
        command = input('Enter a command (start, stop)')
        if command == 'start':
            port = input('Enter a port ')
            port = int(port)
            print('Starting the server')
            echo_server(port)
        if command == 'stop':
            echo_server.close()
            print('Server stopped')

            break
    print('Application finished')
