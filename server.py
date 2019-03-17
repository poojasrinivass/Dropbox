import socket
import sys
import json
from datetime import datetime
import os

HOST = '127.0.0.1'
PORT = 65432

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)
client_socket, addr = server_socket.accept()

def get_date(date_string):
	tmp = date_string.split('/')

	tmp = [int(it) for it in tmp]

	return datetime(tmp[2], tmp[1], tmp[0]).strftime('%Y-%m-%d %H:%M:%S')

def index(commands):
	file_list = os.listdir(".")
	print(file_list)
	ret = []
	if commands[1] == "longlist":
		for file in file_list:
			ret.append({
				"name" : file,
				"size" : os.path.getsize(file),
				"timestamp" : datetime.fromtimestamp(os.path.getmtime(file)).strftime('%Y-%m-%d %H:%M:%S')
				})
	elif commands[1] == "shortlist":

		start_time = get_date(commands[2])
		end_time = get_date(commands[3])
		print(start_time)
		print(end_time)

		for file in file_list:
			mtime = datetime.fromtimestamp(os.path.getmtime(file))
			mtime = mtime.strftime('%Y-%m-%d %H:%M:%S')
			print(file, mtime)
			if mtime >= start_time and mtime <= end_time:
				ret.append({
					"name" : file,
					"size" : os.path.getsize(file),
					"timestamp" : mtime
					})
	else:
		ret.append({
			"error" : "index : invalid flag"
			})
	print("RET")
	print(ret)
	client_socket.send(json.dumps(ret))
	return


def process(commands):
	if commands[0] == "index":
		index(commands)

while True:
	data = client_socket.recv(1024)
	if not data:
		break
	data = json.loads(data)
	print("DATA = ", data)
	process(data)