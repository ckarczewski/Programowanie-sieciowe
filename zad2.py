import logging
import threading
from time import sleep
import string
from tkinter import *

# def controller_thread():
# 	message = input(f"> ")
# 	return message

def thread(e):
	for letter in string.ascii_uppercase:
		out = letter + str(e) + " "
		text_output.insert(INSERT, out)
		sleep(1)
	# print("dupa: " + str(e))

def thread_controller():
	input = text_input.get("1.0", "end-1c")
	print(input)

if __name__ == '__main__':

	master = Tk(className="Zad2") # main window
	master.geometry("600x400")
	master.columnconfigure(0, weight=1)
	master.columnconfigure(1, weight=2)


	text_output = Text(master, width=30, height=20)
	text_output.grid(row=0, column=0, columnspan=3, sticky=EW)

	start = Button(master, text="Start", width=5, command = lambda:thread_controller())
	start.grid(row=1, column=0, sticky=NW)

	stop = Button(master, text="Stop", width=5)
	stop.grid(row=1, column=0, sticky=SW)

	text_input = Text(master, width=5, height=5)
	text_input.grid(row=1, column=1, sticky=EW)
	text_output.insert(INSERT, "Test")


	
	for index in range(4):
		t = threading.Thread(target=thread, args=(index,))
		# t.name = index
		# print(t.name)
		t.start()
		# t.join()

	master.mainloop()
	# while 1:	
	# 	t_controller = threading.Thread(target=controller_thread)
	# 	t_controller.start()

	# for index, thread in enumerate(threads):
	# 	print(f"Main: before joining {thread} index: {index}")
	# 	thread.join()
	# 	print(f"Main thread {index} done")

