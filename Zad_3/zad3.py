#import logging # 123
import threading
from time import sleep
import string
from tkinter import *


lock = threading.Lock()

def work_thread(e):
    with lock:
    	for letter in string.ascii_uppercase:
            print(letter + str(e) + " ")
            sleep(1)
         
if __name__ == '__main__':


	threads = []

 
	for index in range(1, 11):
		thread = threading.Thread(target=work_thread, name=index, args=(index,))
		threads.append(thread)

	for thread in threads:
		thread.start()
		sleep(1)





