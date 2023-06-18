# import logging
# import threading
# from time import sleep

# def thread():
# 	sleep(1)
# 	print("hello world")



# if __name__ == '__main__':
# 	t = threading.Thread(target=thread)
# 	t.start()
# 	print('Waiting for the thread...')
# 	t.join()

# import threading
# import time
# import sys, os
# msg = "zzz"
# # task function
# def task1():
#     global msg
#     while True:
#         print("task 1: "+msg)
#         time.sleep(3)
#         # if msg == "wait":
#             # sys.exit()

# def task2():
#     global msg
#     while True:
#         print("task 2 "+msg)
#         time.sleep(3)
#         # if msg == "wait":
#         #     return
        
# # create a new thread to run a custom function

# if __name__ == '__main__':
#     thread1 = threading.Thread(target=task1)
#     thread2 = threading.Thread(target=task2)
#     # start the thread
#     thread1.start()
#     thread2.start()
#     msg = input('enter msg >')
#     if msg == "x":
#         os._exit(1)
#         print("threads exit succesfuly")

import socket

myHostName = socket.gethostname()
HOST = socket.gethostbyname(myHostName)

print("HOST name: ", myHostName)
print("HOST: ", HOST)
        