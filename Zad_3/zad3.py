#import logging # 123
import threading
from time import sleep
import string
from tkinter import *


exit_event = threading.Event()
lock = threading.Lock()

def work_thread():
    with lock:
    	for letter in string.ascii_uppercase:
            print(letter + str(threading.current_thread().name) + " ")
            sleep(1)
         
def start_thread(threads, index):
    get_thread(threads, index).start()
    
def stop_thread(events, index):
    events[int(index)-1].set()
    
def get_thread(threads, index):
    for thread in threads:
        if thread.name == index:
            return thread


if __name__ == '__main__':


	exit_flag = False
	threads = []
	events = []
 
	for index in range(1, 11):
		events.append(threading.Event())
		thread = threading.Thread(target=work_thread, name=index, args=[events[index-1]])
		threads.append(thread)
 
	for thread in threads:
		thread.start()
		# print(i)
		# print(thr)
		# start_thread(thr, i)





