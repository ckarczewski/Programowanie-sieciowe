import socket
import argparse 
import sys
import threading

# class Server(self, port):
#     def __init__(self, port):
#         self.port = port
    
# Listen Thread
def tcp_listener(sock):
    global client_socket, address
    try:
        sock.listen()
    except socket.error as e:
        print ("Listener error: %s" % e) 
    while True:   
        client_socket, address = sock.accept()
    # return client_socket, address

# Client Thread
def tcp_client(client_socket, address):
    data = client_socket.recv(16)
    if not data:
        print("Client disconnected")
    if data == "End":
        print ("Closing connection to the server") 
        client_socket.close()
    elif data:
        print(f"Message: {data}")
        client_socket.send(data)
        print(f"Send data back to {address}")
    
def tcp_server(port):
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as e: 
        print ("Error creating socket: %s" % e) 
        sys.exit(1) 
        
    try:
        sock.bind(("0.0.0.0", port))
    except socket.error as e: 
        print ("Error creating socket: %s" % e) 
        sys.exit(1) 
    

    
            
if __name__ == '__main__':
    while True:
        command = input('Enter a command (start, stop)')
        if command == 'start':
            port = input('Enter a port ')
            port = int(port)
            print('Starting the server')
            tcp_server(port)
            listen_thread = threading.Thread(target=tcp_listener)
            client_thread = threading.Thread(target=tcp_client)
        if command == 'stop':
            tcp_server.close()
            print('Server stopped')

            break
    print('Application finished')
