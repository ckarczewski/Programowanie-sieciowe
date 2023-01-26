#import logging # 123
import threading
from time import sleep
import string
from tkinter import *


exit_event = threading.Event()
def f(stop_event):
    for letter in string.ascii_uppercase:
        if not stop_event.is_set():
            out = letter + str(threading.current_thread().name) + " "
            text_output.insert(INSERT, out)
            sleep(1)

def start_thread(threads, index):
    get_thread(threads, index).start()
    
def stop_thread(events, index):
    events[int(index)-1].set()
    
def get_thread(threads, index):
    for thread in threads:
        if thread.name == index:
            return thread

def thread(e):
	for letter in string.ascii_uppercase:
		out = letter + str(e) + " "
		text_output.insert(INSERT, out)
		sleep(1)

def thread_starter():
	input = text_input.get("1.0", "end-1c")
	start_thread(threads, input)
	# print(input)
 
def thread_stopper():
    input = text_input.get("1.0", "end-1c")
    stop_thread(events, input)

if __name__ == '__main__':

	master = Tk(className="Zad2") # main window
	master.geometry("600x400")
	master.columnconfigure(0, weight=1)
	master.columnconfigure(1, weight=2)


	text_output = Text(master, width=30, height=20)
	text_output.grid(row=0, column=0, columnspan=3, sticky=EW)

	start = Button(master, text="Start", width=5, command = lambda:thread_starter())
	start.grid(row=1, column=0, sticky=NW)

	stop = Button(master, text="Stop", width=5, command=lambda:thread_stopper())
	stop.grid(row=1, column=0, sticky=SW)

	text_input = Text(master, width=5, height=5)
	text_input.grid(row=1, column=1, sticky=EW)
	Label(master, text="Wpisz liczbę od 1-10 i naciśnij przycisk.").grid(row=2, column=1, sticky=EW)


	exit_flag = False
	threads = []
	events = []
 
	for index in range(1, 11):
		events.append(threading.Event())
		thread = threading.Thread(target=f, name=index, args=[events[index-1]])
		threads.append(thread)


	master.mainloop()


