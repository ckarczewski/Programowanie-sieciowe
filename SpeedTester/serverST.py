import socket
import argparse 
import sys, os
import threading
import re
import time

connection_count = 0
buffer_size = 0

# TCP Client Thread
def tcp_client(client_socket, address):
    print("Create new TCP thread")
    global connection_count
    global buffer_size
    msg_buffer_size = client_socket.recv(16)
    get_size = re.search("([0-9]+)", msg_buffer_size.decode('utf-8'))
    buffer_size = int(get_size[0])
    
    print("TCP Buffer size: ",buffer_size)
    print("Ready to get message")

    total_data_len = 0
    total_time = 0
    start_time = time.perf_counter()
    while True:
        data = client_socket.recv(buffer_size)
        # start_time = time.perf_counter()
        data_len = len(data)
        total_data_len += data_len
     
        if not data:
            print(f"TCP Client {address} disconnected")
            client_socket.close()
            connection_count -= 1
            print("Disconnect  C-count: ", connection_count)
            
            end_time = time.perf_counter()
            elapsed_time = end_time - start_time      
            total_time = elapsed_time
            
            transfer_speed = total_data_len/1024 / total_time
            print(f"TCP Otrzymano {round(total_data_len/1024)}kb w czasie {round(total_time,1)}s z prędkością {round(transfer_speed,1)}kb/sec od {address}")
            break
        # elif data:
        #     print(f"TCP Message: {data.decode('utf-8')}, len: {data_len}, from {address}")


        # end_time = time.perf_counter()
        # elapsed_time = end_time - start_time      
        # total_time += elapsed_time

# TCP thread
def tcp_server(port):
    global connection_count
    try:
        print("tcp: create sock")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as e: 
        print ("Error creating socket: %s" % e) 
        sys.exit(1) 
        
    try:
        print("tcp: bind sock")
        
        sock.bind(("0.0.0.0", port))
    except socket.error as e: 
        print ("Error creating socket: %s" % e) 
        sys.exit(1) 
    try:
        print("tcp: listen")
        sock.listen()
    except socket.error as e:
        print ("Listener error: %s" % e) 
    while True:
        try:
            client_socket, address = sock.accept()
            connection_count += 1
            # print("After 1st con cc: ", connection_count)
        except socket.error as e:
            print("cant accept", e)
        if connection_count > 1:
            msg = "BUSY"
            client_socket.send(msg.encode('utf-8'))
            client_socket.close()
            connection_count -= 1
            # print("after busy cc: ",connection_count)
        else: 
            msg = "READY"
            client_socket.send(msg.encode('utf-8'))
            print("Wysłałem wiadomość READY")  
            print(f"TCP Connected with IP address: {address} ")
            client_thread = threading.Thread(target=tcp_client, args=(client_socket,address))
            client_thread.start()

# UDP Client Thread
def udp_client(client_socket):
    print("Create new UDP thread")
    global buffer_size
    total_data_len = 0
    total_time = 0
    buffer_size = 14

    while True:
        data, address = client_socket.recvfrom(buffer_size)
        if data.startswith(("SIZE:").encode("utf-8")):
            get_size = re.search("([0-9]+)", data.decode('utf-8'))
            buffer_size = int(get_size[0])
            print("buffer size=", buffer_size)
            total_data_len = 0
            total_time = 0
            start_time = time.perf_counter()

        
        data_len = len(data)
        total_data_len += data_len
        
        if data.decode('utf-8') == "FINE":
            end_time = time.perf_counter()
            elapsed_time = end_time - start_time
            total_time = elapsed_time
            transfer_speed = total_data_len/1024 / total_time
            print(f"UDP Otrzymano {round(total_data_len/1024)}kb w czasie {round(total_time,1)}s z prędkością {round(transfer_speed,1)}kb/sec od {address}") 
            buffer_size = 14
        if not data:
            print(f"UDP Client {address} disconnected")
            break
        # elif data:
        #     print(f"UDP Message: {data.decode('utf-8')}, len: {data_len}, from {address}")
        
        # end_time = time.perf_counter()
        # elapsed_time = end_time - start_time
        # total_time += elapsed_time
        



# UDP Thread
def udp_server(port):
    try:
        print("udp: create sock")
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    except socket.error as e: 
        print ("Error creating socket: %s" % e) 
        sys.exit(1) 

    try:
        print("udp: bind sock")
        sock.bind(("0.0.0.0", port))
    except socket.error as e: 
        print ("Error creating socket: %s" % e) 
        sys.exit(1)
    
    udp_client_thread = threading.Thread(target=udp_client, args=(sock, ))
    udp_client_thread.start()
    
            
if __name__ == '__main__':
    while True:
        command = input('Enter a command (start, stop)')
        if command == 'start':
            while True:
                port = input('Enter a port ')
                if len(port) == 4:
                    try:
                        port = int(port)
                        break
                    except:
                        print("Port should be Int")
                else:
                   print("Port should contain 4 numbers") 

            # port = 6969
            print('Starting the server')

            tcp_ser = threading.Thread(target=tcp_server, args=(port,))
            udp_ser = threading.Thread(target=udp_server, args=(port,))
            tcp_ser.start()
            udp_ser.start()

        if command == 'stop':
            print('Server stopped')
            os._exit(1)

            
    print('Application finished')
