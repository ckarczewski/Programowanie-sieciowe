import socket
import argparse 
import sys

myHostName = socket.gethostname()
HOST = socket.gethostbyname(myHostName)

def echo_client(port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    except socket.error as e: 
        print ("Error creating socket: %s" % e) 
        sys.exit(1) 

    try:
        sock.connect((HOST, port))
    except socket.error as e:
        print (f"Can not connect: {str(e)}")
        sys.exit(1)
    
    while True: 
        message = input(f"> ")
        if message:
            try: 
                # Send data 
                print (f"Sending: {message}") 
                sock.sendall(message.encode('utf-8')) 
                # Look for the response 
                amount_received = 0 
                amount_expected = len(message) 
                while amount_received < amount_expected: 
                    data = sock.recv(24)
                    if not data: 
                        print("Server disconnected, can not send message")
                        sock.close()
                        break
                    amount_received += len(data) 
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
