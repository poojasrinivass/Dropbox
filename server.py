import socket
import sys
import json
import datetime
import os

HOST = '127.0.0.1'
PORT = 65432

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)
client_socket, addr = server_socket.accept()

def get_date(date_string):
	tmp = date_string.split('/')
	return datetime.datetime(tmp[0], tmp[1], tmp[2])

def index(commands):
	file_list = os.listdir(".")
	ret = []
	if commands[1] == "longlist":
		for file in file_list:
			ret.append({
				"name" : file,
				"size" : os.path.getsize(file),
				"timestamp" : datetime.datetime.fromtimestamp(os.path.getmtime(file)).strftime('%Y-%m-%d %H:%M:%S')
				})
	elif commands[1] == "shortlist":

		start_time = get_date(commands[2])
		end_time = get_date(commands[3])

		for file in file_list:
			mtime = datetime.datetime.fromtimestamp(os.path.getmtime(file))
			if mtime >= start_time and mtime <= end_time:
				ret.append({
					"name" : file,
					"size" : os.path.getsize(file),
					"timestamp" : mtime.strftime('%Y-%m-%d %H:%M:%S')
					})
	else:
		ret.append({
			"error" : "index : invalid flag"
			})
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