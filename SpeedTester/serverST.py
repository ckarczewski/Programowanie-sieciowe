import socket
import argparse 
import sys
import threading

connection_count = 0

# class Server(self, port):
#     def __init__(self, port):
#         self.port = port
    
# Listen Thread
# def tcp_listener(sock):
#     global client_socket, address
#     global client_thread
#     try:
#         print("próbuje słuchać")
#         sock.listen()
#     except socket.error as e:
#         print ("Listener error: %s" % e) 
#     while True:
#         try:   
#             print("próbuje zaakceptować")
#             client_socket, address = sock.accept()
#         except socket.error as e:
#             print("cant accept")  
#         print(f"Connected with IP address: {address} ")
        
#         client_thread = threading.Thread(target=tcp_client(client_socket,address))
#         client_thread.start()
#         print("stworzyłem nowy wątek z klientem")
    # return client_socket, address

# Client Thread
def tcp_client(client_socket, address):
    global connection_count
    print("Ready to get message")
    while True:
        data = client_socket.recv(16)
        print("jestem w pętli i otrzymałem dane")
        if not data:
            print("Client disconnected")
            client_socket.close()
            connection_count -= 1
            print("disc cc: ", connection_count)
            break
        if data == "End":
            print ("Closing connection to the server") 
            client_socket.close()
            connection_count -= 1
            print("disc cc: ", connection_count)
            break
        elif data:
            print(f"Message: {data}")
            client_socket.send(data)
            print(f"Send data back to {address}")

# TCP thread
def tcp_server(port):
    global connection_count
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
    try:
        print("próbuje słuchać")
        sock.listen()
    except socket.error as e:
        print ("Listener error: %s" % e) 
    while True:
        try:  
            print("próbuje zaakceptować") 
            client_socket, address = sock.accept()
            connection_count += 1
            print("after 1st con cc: ", connection_count)
        except socket.error as e:
            print("cant accept")
        if connection_count > 1:
            msg = "BUSY"
            client_socket.send(msg.encode('utf-8'))
            client_socket.close()
            connection_count -= 1
            print("after busy cc: ",connection_count)
        else: 
            msg = "Hello!!!"
            client_socket.send(msg.encode('utf-8'))
            print("Wysłałem wiadomość")  
            print(f"Connected with IP address: {address} ")
            client_thread = threading.Thread(target=tcp_client, args=(client_socket,address))
            client_thread.start()
            print("stworzyłem nowy wątek z klientem")



    
            
if __name__ == '__main__':
    while True:
        command = input('Enter a command (start, stop)')
        if command == 'start':
            port = input('Enter a port ')
            port = int(port)
            print('Starting the server')
            # tcp_server(port)
            tcp_ser = threading.Thread(target=tcp_server, args=(port,))
            tcp_ser.start()
            # tcp_ser.join()
        if command == 'stop':
            print('Server stopped')
            sys.exit(1)
    print('Application finished')
