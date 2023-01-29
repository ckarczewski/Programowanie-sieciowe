import socket
import argparse 
import sys

myHostName = socket.gethostname()
HOST = socket.gethostbyname(myHostName)
buffer_size = 36
def echo_client(port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    except socket.error as e: 
        print ("Error creating socket: %s" % e) 
        sys.exit(1) 

    server_address = (HOST, port)
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
                amount_received = 0 
                amount_expected = len(message) 
                while amount_received < amount_expected:   
                    data_temp, address = sock.recvfrom(buffer_size)
                    data += str(data_temp)
                    if not data: 
                        print("Server disconnected, can not send message")
                        sock.close()
                        break
                    amount_received += len(data) 
                print("GET Data from server")
                print (f"Received: {data}") 
            except socket.error as e: 
                print (f"Socket error: {str(e)}")
                break
            except Exception as e: 
                print (f"Other exception: {str(e)}") 
                break

            
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Socket Server Example') 
    parser.add_argument(
        '--port', action="store", dest="port", type=int, required=True) 
    given_args = parser.parse_args()  
    port = given_args.port 
    echo_client(port)
