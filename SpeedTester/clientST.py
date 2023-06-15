import socket
import argparse 
import sys
import re
import time
import threading

myHostName = socket.gethostname()
HOST = socket.gethostbyname(myHostName)
# buffer_size = 10
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
        message = "SIZE:"+str(buffer_size)
        # print("buffer size: ",buffer_size)
        
        print("message is:", message)
        while True:
            if message:
                try: 
                    # Send data 
                    if message.startswith("SIZE:"):
                        sock.sendall(message.encode('utf-8'))
                        message = fill_array(buffer_size)
                    else:
                        # print (f"TCP Sending: {message}") 
                        sock.sendall(message.encode('utf-8')) 
                except socket.error as e: 
                    print (f"Socket error: {str(e)}")
                    break
                except Exception as e: 
                    print (f"Other exception: {str(e)}") 
                    break
            if close_program_flag:
                    print("Disconnect")
                    sock.close()
                    sys.exit()
            time.sleep(0)
            

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
    data_size_msg = "SIZE:"+str(buffer_size)
    sock.sendto(data_size_msg.encode('utf-8'), server_address)
    while True:
            
        if message:
            try: 
                # Send data 
                sock.sendto(message.encode('utf-8'), server_address)
                # print (f"UDP Sending: {message}") 
            except socket.error as e: 
                print (f"Socket error: {str(e)}")
                break
            except Exception as e: 
                print (f"Other exception: {str(e)}") 
                break
            
        if off_flag == True or close_program_flag == True:
            message = "FINE"
            sock.sendto(message.encode('utf-8'), server_address)
            sock.close()
            print("UDP close")
            sys.exit() 
        time.sleep(0)

# data array
def fill_array(n):
    data = ""
    for i in range(n):
        data += "X"
    return data

if __name__ == '__main__':

    AddressRegex ="[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}"
    while True:
        command = input('Enter a command (start, stop)')
        if command == 'start':
            # address = input('Enter a address ')
            # res = re.search(AddressRegex, address)
            # address = address
            port = input('Enter a port ')
            port = int(port)
            package_size = input('Enter a buffer size B: ')
            package_size = int(package_size)
            # nagle_flag = input('Enter a nagle flag y/n ')
            # nagle_flag = nagle_flag
            print('Starting the server')
            tcp_thread = threading.Thread(target=tcp_connection, args=(port,package_size))
            udp_thread = threading.Thread(target=udp_connection, args=(port,package_size))
            tcp_thread.start()
            udp_thread.start()
            close_program = input("Type x to close program")
            if close_program == "x":
                close_program_flag = True
                sys.exit()
            
        if command == 'stop':
            # echo_server.close()
            print('Server stopped')

            break
    print('Application finished')
