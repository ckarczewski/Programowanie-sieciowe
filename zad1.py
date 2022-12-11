import logging
import threading
from time import sleep

def thread():
	sleep(1)
	print("hello world")



if __name__ == '__main__':
	t = threading.Thread(target=thread)
	t.start()
	print('Waiting for the thread...')
	t.join()