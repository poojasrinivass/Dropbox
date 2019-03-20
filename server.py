import socket
import os
import hashlib
from datetime import datetime
import json
import sys

HOST = "127.0.0.1"
PORT = 65432
UDP_PORT = 9999
help_msg = "Use command 'help' or refer to README.md for usage."
usage = ("\n1. index longlist \n" +
		 "2. index longlist *.ext \n" + 
		 "3. index longlist *.ext word \n" +
		 "4. index shortlist dd-mm-yyyy HH:MM:SS dd-mm-yyyy HH:MM:SS \n" + 
		 "5. index shortlist dd-mm-yyyy HH:MM:SS dd-mm-yyyy HH:MM:SS *.ext \n" + 
		 "6. filehash checkall \n" + 
		 "7. filehash verify file_name \n" + 
		 "8. download TCP file_name \n" + 
		 "9. download UDP file_name\n")

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

	date = date_string[0].split('-')

	d = int(date[0])
	m = int(date[1])
	y = int(date[-1])

	time = date_string[-1].split(':')

	H = int(time[0])
	M = int(time[1])
	S = int(time[-1])


	return datetime(y, m, d, H, M, S).strftime('%Y-%m-%d %H:%M:%S')

def extension(ext_string):
	if(ext_string[0] != '*' or ext_string[1] != '.'):
		return "-1"
	return ext_string[2:]

def md5(file):
    md5_hash = hashlib.md5()
    with open(file, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            md5_hash.update(chunk)
    return md5_hash.hexdigest()

def index(commands):
	# file_list = os.listdir(".")
	# print(file_list)
	res = []
	if len(commands) < 2:
		res.append({
			"error": "Not Enough Arguments!"
			})
	elif commands[1] == "longlist":
		ext, word = "", ""
		if(len(commands) > 2):
			if len(commands) == 3:
				ext = extension(commands[-1])
			else:
				ext = extension(commands[-2])
			if len(commands) == 4:
				word = commands[-1]

			if ext == "-1":
				res = []
				res.append({
					"Error" : "Invalid extension!"
					})
				client_socket.send(json.dumps(res))
				return
		file_list = []
		if ext != "":
			for file in os.listdir("."):
				if file[-len(ext):] == ext:
					if word == "":
						file_list.append(file)
					else:
						if os.path.isfile(file):
							with open(file) as f:
								for line in f:
									if word in line:
										file_list.append(file)
		else:
			file_list = os.listdir(".")
		for file in file_list:
			res.append({
				"name" : file,
				"size" : os.path.getsize(file),
				"timestamp" : datetime.fromtimestamp(os.path.getmtime(file)).strftime('%Y-%m-%d %H:%M:%S')
				})
	elif commands[1] == "shortlist":

		if len(commands) < 6:
			res.append({
				"error" : "Not Enough Arguments passed!"
				})
		else:
			start_time = get_date(commands[2:4])
			end_time = get_date(commands[4:6])
			# print(start_time)
			# print(end_time)
			ext = ""
			if(len(commands) > 6):
				ext = extension(commands[-1])
				# print("YOYO", ext)
				if ext == "-1":
					res = []
					res.append({
						"Error" : "Invalid extension!"
						})
					client_socket.send(json.dumps(res))
					return
			file_list = []
			if ext != "":
				for file in os.listdir("."):
					# print(file, file[-len(ext):])
					if file[-len(ext):] == ext:
						file_list.append(file)
			else:
				file_list = os.listdir(".")
			for file in file_list:
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
		print("Connection broken!")
		return
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
		print("Connection broken!")
		return
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
	return

def process(commands):
	res = []
	if commands[0] == "index":
		try:
			index(commands)
		except Exception as e:
			print(str(e))
			print(help_msg)
			res.append({
				"Error" : str(e),
				"Tip-" : help_msg
				})
			client_socket.send(json.dumps("ERR"))
			data = client_socket.recv(1024)
			if not data:
				print("Connection broken!")
				return
			data = json.loads(data)
			if data == "ACK":
				client_socket.send(json.dumps(res))
			else:
				res = []
				res.append({
					"Error" : "No acknowledgement received!"
					})
				client_socket.send(json.dumps(res))

	elif commands[0] == "filehash":
		try:
			filehash(commands)
		except e:
			print(str(e))
			print(help_msg)
			res.append({
				"Error" : str(e),
				"Tip-" : help_msg
				})
			client_socket.send(json.dumps("ERR"))
			data = client_socket.recv(1024)
			if not data:
				print("Connection broken!")
				return
			data = json.loads(data)
			if data == "ACK":
				client_socket.send(json.dumps(res))
			else:
				res = []
				res.append({
					"Error" : "No acknowledgement received!",
					})
				client_socket.send(json.dumps(res))
	elif commands[0] == "download":
		try:
			download(commands)
		except e:
			print(str(e))
			print(help_msg)
			res.append({
				"Error" : str(e),
				"Tip-" : help_msg
				})
			client_socket.send(json.dumps("ERR"))
			data = client_socket.recv(1024)
			if not data:
				print("Connection broken!")
				return
			data = json.loads(data)
			if data == "ACK":
				client_socket.send(json.dumps(res))
			else:
				res = []
				res.append({
					"Error" : "No acknowledgement received!",
					})
				client_socket.send(json.dumps(res))
	elif commands[0] == "help":
		client_socket.send(json.dumps("OUTPUT"))
		data = client_socket.recv(1024)
		if not data:
				print("Connection broken!")
				return
		data = json.loads(data)
		if data == "ACK":
			res = []
			res.append({
				"Usage" : usage
				})
			client_socket.send(json.dumps(res))
		else:
			res = []
			res.append({
				"Error" : "No acknowledgement received!",
				})
			client_socket.send(json.dumps(res))
	else:
		print("Invalid Command Entered!")
		res.append({
			"Error" : "Invalid Command!",
			"Tip-" : help_msg
			})
		client_socket.send(json.dumps("ERR"))
		data = client_socket.recv(1024)
		if not data:
			print("Connection broken!")
			return
		data = json.loads(data)
		if data == "ACK":
			client_socket.send(json.dumps(res))
		else:
			res = []
			res.append({
				"Error" : "No acknowledgement received!"
				})
			client_socket.send(json.dumps(res))
	return

while True:
	data = client_socket.recv(1024)
	if not data:
		print("Disconnecting...")
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