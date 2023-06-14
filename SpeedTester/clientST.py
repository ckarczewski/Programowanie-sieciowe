import socket
import argparse 
import sys
import re
import time
import threading

myHostName = socket.gethostname()
HOST = socket.gethostbyname(myHostName)
buffer_size = 10
off_flag = False
close_program_flag = False
          
# TCP
def tcp_connection(port, buffer_size):
    global off_flag
    global HOST
    global close_program_flag
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as e: 
        print ("Error creating socket: %s" % e) 
        sys.exit(1) 

    try:
        sock.connect((HOST, port))
    except socket.error as e:
        print (f"Can not connect: {str(e)}")
        sys.exit(1)
    
    status_msg = sock.recv(24).decode('utf-8')
    print (f"Status: {status_msg}")
    if status_msg == "BUSY":
        print("Server is BUSY")
        off_flag = True
        sys.exit()
    elif status_msg == "READY":
        data_size_msg = "SIZE:"+buffer_size
        sock.sendall(data_size_msg.encode('utf-8'))
        message = fill_array(buffer_size)
        while True:
            if message:
                if close_program_flag:
                    print("Disconect")
                    sock.close()
                    sys.exit()
                try: 
                    # Send data 
                    print (f"Sending: {message}") 
                    sock.sendall(message.encode('utf-8')) 
                    # # Look for the response 
                    # amount_received = 0 
                    # amount_expected = len(message) 
                    # while amount_received < amount_expected: 
                    #     data = sock.recv(24)
                    #     if not data: 
                    #         print("Server disconnected, can not send message")
                    #         sock.close()
                    #         break
                    #     amount_received += len(data) 
                    #     print (f"Received: {data}") 
                except socket.error as e: 
                    print (f"Socket error: {str(e)}")
                    break
                except Exception as e: 
                    print (f"Other exception: {str(e)}") 
                    break
            time.sleep(3)
            

# UDP
def udp_connection(port, buffer_size):
    global off_flag
    global HOST
    global close_program_flag
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    except socket.error as e: 
        print ("Error creating socket: %s" % e) 
        sys.exit(1) 
    server_address = (HOST, port)
    message = fill_array(buffer_size)
    data_size_msg = "SIZE:"+buffer_size
    sock.sendto(data_size_msg.encode('utf-8'), server_address)
    while True:
        if off_flag == True or close_program_flag == True:
            sock.close()
            sys.exit()     
        if message:
            try: 
                # Send data 
                sock.sendto(message.encode('utf-8'), server_address)
                print (f"Sending: {message}") 
            except socket.error as e: 
                print (f"Socket error: {str(e)}")
                break
            except Exception as e: 
                print (f"Other exception: {str(e)}") 
                break
        time.sleep(2)

# data array
def fill_array(n):
    data = ""
    for i in range(n):
        data += str(i)
    return data

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Socket Server Example') 
    parser.add_argument(
        '--port', action="store", dest="port", type=int, required=True) 
    given_args = parser.parse_args()  
    port = given_args.port 
# #####
    AddressRegex ="[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}"
    while True:
        command = input('Enter a command (start, stop)')
        if command == 'start':
            address = input('Enter a address ')
            # res = re.search(AddressRegex, address)
            address = address
            port = input('Enter a port ')
            port = int(port)
            package_size = input('Enter a buffer size B')
            package_size = int(package_size)
            nagle_flag = input('Enter a nagle flag y/n ')
            nagle_flag = nagle_flag
            print('Starting the server')
            tcp_thread = threading.Thread(target=tcp_connection, args=(port,buffer_size))
            # udp_thread = threading.Thread(target=udp_connection, args=(port,buffer_size))
            tcp_thread.start()
            # udp_thread.start()
            close_program = input("Type x to close program")
            if close_program == "x":
                close_program_flag = True
                sys.exit()
            
        if command == 'stop':
            # echo_server.close()
            print('Server stopped')

            break
    print('Application finished')
