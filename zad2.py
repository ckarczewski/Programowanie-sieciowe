import logging
import threading
from time import sleep
import string

def thread(e):
	for letter in string.ascii_uppercase:
		print(letter + str(e))
		sleep(1)
	# print("dupa: " + str(e))


if __name__ == '__main__':

	for index in range(4):
		t = threading.Thread(target=thread, args=(index,))
		t.name = index
		print(t.name)
		t.start()
		# t.join()

	while 1:	
		message = input(f"> ")

	# for index, thread in enumerate(threads):
	# 	print(f"Main: before joining {thread} index: {index}")
	# 	thread.join()
	# 	print(f"Main thread {index} done")

