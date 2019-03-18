import socket
import os
import hashlib
from datetime import datetime
import json
<<<<<<< HEAD
import sys
=======
>>>>>>> 8f8644c1b763a83fe624fe460019f9853f1aeb72

HOST = "127.0.0.1"
PORT = 65432
UDP_PORT = 9999

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)
client_socket, addr = server_socket.accept()

def is_json(myjson):
  try:
    json_object = json.loads(myjson)
  except ValueError, e:
    return False
  return True

def get_date(date_string):
	tmp = date_string.split('/')

	tmp = [int(it) for it in tmp]

	return datetime(tmp[2], tmp[1], tmp[0]).strftime('%Y-%m-%d %H:%M:%S')

def extension(ext_string):
	if(ext_string[1] != '.'):
		raise Exception("Invalid Extension!")
	return ext_string[2:]

def md5(file):
    md5_hash = hashlib.md5()
    with open(file, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            md5_hash.update(chunk)
    return md5_hash.hexdigest()

def index(commands):
	file_list = os.listdir(".")
	# print(file_list)
	res = []
	if len(commands) < 2:
		res.append({
			"error": "Not Enough Arguments!"
			})
	elif commands[1] == "longlist":
		ext = ""
		if(len(commands) == 3):
			ext = extension(commands[-1])
		for file in file_list:
			if ext == "" or file[-3:] == ext:
				res.append({
					"name" : file,
					"size" : os.path.getsize(file),
					"timestamp" : datetime.fromtimestamp(os.path.getmtime(file)).strftime('%Y-%m-%d %H:%M:%S')
					})
	elif commands[1] == "shortlist":

		if len(commands) < 4:
			res.append({
				"error" : "Not Enough Arguments passed!"
				})
		else:
			start_time = get_date(commands[2])
			end_time = get_date(commands[3])
			# print(start_time)
			# print(end_time)
			ext = ""
			if(len(commands) == 5):
				ext = extension(commands[-1])

			for file in file_list:
				if ext == "" or file[-3:] == ext:
					mtime = datetime.fromtimestamp(os.path.getmtime(file))
					mtime = mtime.strftime('%Y-%m-%d %H:%M:%S')
					# print(file, mtime)
					if mtime >= start_time and mtime <= end_time:
						res.append({
							"name" : file,
							"size" : os.path.getsize(file),
							"timestamp" : mtime
							})
	else:
		res.append({
			"error" : "index : invalid flag"
			})
	# print("res")
	# print(res)
	client_socket.send(json.dumps("OUTPUT"))
	data = client_socket.recv(1024)
	if not data:
		res = []
		res.append({
			"error" : "Connection broken!"
			})
	data = json.loads(data)
	if data == "ACK":
		client_socket.send(json.dumps(res))
	else:
		res = []
		res.append({
			"Transmission not acknowledged!"
			})
		client_socket.send(json.dumps(res))
	return

def filehash(commands):
	res = []

	if len(commands) < 2:
		res.append({
			"error": "Not Enough Arguments!"
			})

	elif commands[1] == "verify":
		if len(commands) != 3:
			res.append({
				"error": "Improper Arguments passed!"
				})
		else:
			file = commands[2]

			if not os.path.isfile(file):
				res.append({
					"error" : "File does not exist!"
					})
			else:
				if os.path.isfile(file):

					res.append({
						"name" : file,
						"checksum" : md5(file),
						"timestamp" : datetime.fromtimestamp(os.path.getmtime(file)).strftime('%Y-%m-%d %H:%M:%S')
						})
	elif commands[1] == "checkall":
		file_list = os.listdir(".")
		for file in file_list:
			if os.path.isfile(file):
				res.append({
					"name" : file,
					"checksum" : md5(file),
					"timestamp" : datetime.fromtimestamp(os.path.getmtime(file)).strftime('%Y-%m-%d %H:%M:%S')
					})
	else:
		res.append({
			"error" : "index : invalid flag"
			})
	
	client_socket.send(json.dumps("OUTPUT"))
	data = client_socket.recv(1024)
	if not data:
		res = []
		res.append({
			"error" : "Connection broken!"
			})
	data = json.loads(data)
	if data == "ACK":
		client_socket.send(json.dumps(res))
	else:
		res = []
		res.append({
			"Transmission not acknowledged!"
			})
		client_socket.send(json.dumps(res))
	return


def download(commands):
	res = []
<<<<<<< HEAD
	client_socket.send(json.dumps("DOWNLOAD"))
	data = client_socket.recv(1024)
	if not data:
		print("Error : Connection broken!")
		return
	elif is_json(data) and json.loads(data) != "ACK":
		res.append({
			"error" : "No acknowledgement received!"
			})
	else:
		if len(commands) < 3:
			res.append({
				"error": "Not Enough Arguments!"
				})
			client_socket.send(json.dumps(res))
			return
		elif commands[1] == "TCP":
			file = commands[2]
			if not os.path.isfile(file):
				res.append({
					"error" : "File does not exist!"
					})
				client_socket.send(json.dumps(res))
				return
			else:
				data = client_socket.recv(1024)
=======
	if len(commands) < 3:
		res.append({
			"error": "Not Enough Arguments!"
			})
		client_socket.send(json.dumps(res))
		return
	elif commands[1] == "TCP":
		file = commands[2]
		if not os.path.isfile(file):
			res.append({
				"error" : "File does not exist!"
				})
			client_socket.send(json.dumps(res))
			return
		else:
			client_socket.send(json.dumps("DOWNLOAD"))
			data = client_socket.recv(1024)
			if not data:
				res.append({
					"error" : "Connection broken!"
					})
			data = json.loads(data)
			if data == "ACK":
>>>>>>> 8f8644c1b763a83fe624fe460019f9853f1aeb72
				f = open(file, 'rb')
				packet = f.read(1024)
				while packet:
					print("Sending..")
					client_socket.send(packet)
					packet = f.read(1024)
				f.close()
				client_socket.send(json.dumps("DONE"))
				res.append({
					"name" : file,
					"size" : os.path.getsize(file),
					"checksum" : md5(file),
					"timestamp" : datetime.fromtimestamp(os.path.getmtime(file)).strftime('%Y-%m-%d %H:%M:%S')
					})
				data = client_socket.recv(1024)
				if not data or json.loads(data) != "ACK":
					res = []
					res.append({
						"error" : "No acknowledgement received!"
						})
				client_socket.send(json.dumps(res))
<<<<<<< HEAD
		elif commands[1] == "UDP":
			udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			dest = (HOST, UDP_PORT)

			res = []
			file = commands[2]
			if not os.path.isfile(file):
				res.append({
					"error" : "File does not exist!"
					})
				udp_socket.sendto(res, dest)
				return
			else:
				f = open(file, 'rb')
				packet = f.read(1024)
				while packet:
					print("Sending..")
					udp_socket.sendto(packet, dest)
					packet = f.read(1024)
				udp_socket.close()
				f.close()
				res.append({
					"name" : file,
					"size" : os.path.getsize(file),
					"checksum" : md5(file),
					"timestamp" : datetime.fromtimestamp(os.path.getmtime(file)).strftime('%Y-%m-%d %H:%M:%S')
					})
				client_socket.send(json.dumps("DONE"))
				data = client_socket.recv(1024)
				if not data:
					print("Error : Connection broken!")
					return
				elif is_json(data) and json.loads(data) == "ACK":
					client_socket.send(json.dumps(res))
				else:
					res = []
					res.append({
						"error" : "No acknowledgement received!"
						})
					client_socket.send(json.dumps(res))
=======
			else:
				res = []
				res.append({
					"error" : "Transmission not acknowledged!"
					})
				client_socket.send(json.dumps(res))
	# elif commands[1] == "UDP":
>>>>>>> 8f8644c1b763a83fe624fe460019f9853f1aeb72
	return

def process(commands):
	if commands[0] == "index":
		index(commands)
	elif commands[0] == "filehash":
		filehash(commands)
	elif commands[0] == "download":
		download(commands)

while True:
	data = client_socket.recv(1024)
	if not data:
		break
	data = json.loads(data)
	if data == "ACK":
		continue
	try:
		process(data)
	except Exception as e:
		print(str(e))
		server_socket.close()
		client_socket.close()
		sys.exit()