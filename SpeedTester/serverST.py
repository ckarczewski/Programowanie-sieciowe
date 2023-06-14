import socket
import argparse 
import sys
import threading
import re
import time

connection_count = 0
buffer_size = 0
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

# TCP Client Thread
def tcp_client(client_socket, address):
    global connection_count
    global buffer_size
    msg_buffer_size = client_socket.recv(16)
    print(msg_buffer_size)
    get_size = re.search("([0-9]+)", msg_buffer_size.decode('utf-8'))
    buffer_size = int(get_size[0])
    print("bufor size: ",buffer_size)
    print("Ready to get message")
    total_data_len = 0
    total_time = 0
    while True:
        data = client_socket.recv(buffer_size)
        start_time = time.time()
        
        # print("poczatku petli while ",data)
        data_len = len(data)
        total_data_len += data_len
        # print(data_len)
        print(f"jestem w pętli i otrzymałem dane: {data}, o długosci: {data_len}")
        if not data:
            print("Client disconnected")
            client_socket.close()
            connection_count -= 1
            print("disc cc: ", connection_count)
            transfer_speed = total_data_len / total_time
            print(f"Otrzymano {total_data_len/1024}kb w czasie {round(total_time,6)}s z prędkością {transfer_speed}kb/sec od {address}")
            
            break
        if data == "b'End'":
            print ("Closing connection to the server") 
            client_socket.close()
            connection_count -= 1
            print("disc cc: ", connection_count)
            break
        elif data:
            # print(f"Message: {data}")
            # client_socket.send(data)
            # print(f"Send data back to {address}")
            pass

        end_time = time.time()
        elapsed_time = end_time - start_time
        # print("czas przesłania jednej paczki w sec ", elapsed_time)
        
        total_time += elapsed_time

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
            msg = "READY"
            client_socket.send(msg.encode('utf-8'))
            print("Wysłałem wiadomość")  
            print(f"Connected with IP address: {address} ")
            client_thread = threading.Thread(target=tcp_client, args=(client_socket,address))
            client_thread.start()
            print("stworzyłem nowy wątek z klientem")

# DUP Client Thread
def udp_client(client_socket):
    global buffer_size
    total_data_len = 0
    total_time = 0
    while True:
        data, address = client_socket.recvfrom(buffer_size)
        if data.startswith("SIZE:"):
            total_data_len = 0
            total_time = 0

        start_time = time.time()
        data_len = len(data)
        total_data_len += data_len
        if not data:
            print(f"Client {address} disconnected")
            break
        elif data:
            print(f"UDP Message {data}")
            client_socket.sendto(data, address)
            print(f"Send data back to: {address}")
        elif data == b'FINE':
            transfer_speed = total_data_len / total_time
            print(f"Otrzymano {total_data_len/1024}kb w czasie {round(total_time,6)}s z prędkością {transfer_speed}kb/sec od {address}") 
            break
        end_time = time.time()
        elapsed_time = end_time - start_time
        print("czas przesłania jednej paczki w sec ", elapsed_time)
        
        total_time += elapsed_time
        



# UDP Thread
def udp_server(port):
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
    
    udp_client_thread = threading.Thread(target=udp_client, args=(sock, ))
    udp_client_thread.start()
    print("Stworzyłem wątek UDP")
    
            
if __name__ == '__main__':
    while True:
        command = input('Enter a command (start, stop)')
        if command == 's':
            # port = input('Enter a port ')
            # port = int(port)
            port = 6969
            print('Starting the server')
            # tcp_server(port)
            tcp_ser = threading.Thread(target=tcp_server, args=(port,))
            udp_ser = threading.Thread(target=udp_server, args=(port,))
            tcp_ser.start()
            udp_ser.start()
            # tcp_ser.join()
        if command == 'stop':
            print('Server stopped')
            sys.exit(1)
    print('Application finished')
