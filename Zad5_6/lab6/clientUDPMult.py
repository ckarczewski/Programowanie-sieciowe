import socket
import argparse 
import sys

myHostName = socket.gethostname()
HOST = socket.gethostbyname(myHostName)
buffer_size = 36
def echo_client(server_address):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32)
    except socket.error as e: 
        print ("Error creating socket: %s" % e) 
        sys.exit(1) 


    
    # server_address = (HOST, port)
    print(server_address)
    data=""
    while True: 
        message = input(f"> ")
        if message:
            try: 
                message_parts = [message[i:i+buffer_size] for i in range(0, len(message), buffer_size)]
                # Send data 
                for part in message_parts:
                    sock.sendto(part.encode('utf-8'), server_address)
                print (f"Sending: {message}") 
                # Look for the response 
                # amount_received = 0 
                # amount_expected = len(message) 
                # while amount_received < amount_expected: 
                #     # data, address = sock.recvfrom(buffer_size)   
                #     data_temp, address = sock.recvfrom(buffer_size)
                #     data += str(data_temp)
                data, address = sock.recvfrom(buffer_size)
                if not data: 
                    print("Server disconnected, can not send message")
                    sock.close()
                    break
                    # amount_received += len(data) 
                print("GET Data from server")
                print (f"Received: {data}") 
            except socket.error as e: 
                print (f"Socket error: {str(e)}")
                break
            except Exception as e: 
                print (f"Other exception: {str(e)}") 
                break
            print("powinno wyjsc z ifa")
            
if __name__ == '__main__':
    # parser = argparse.ArgumentParser(
    #     description='Socket Server Example') 
    # parser.add_argument(
    #     '--port', action="store", dest="port", type=int, required=True) 
    # given_args = parser.parse_args()  
    # port = given_args.port 
    multicast_group = input("Wprowadź adres IP grupy multicast: ")
    server_address = (multicast_group, int(input("Wprowadź numer portu: ")))

    # port = 6699
    # echo_client(port)
    echo_client(server_address)
