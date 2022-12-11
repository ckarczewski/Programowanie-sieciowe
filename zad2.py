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
	threads = list()
	for index in range(4):
		t = threading.Thread(target=thread, args=(index,))
		threads.append(t)
		t.start()
		print('Waiting for the thread...')
		# t.join()

	for index, thread in enumerate(threads):
		print(f"Main: before joining {thread} index: {index}")
		thread.join()
		print(f"Main thread {index} done")

