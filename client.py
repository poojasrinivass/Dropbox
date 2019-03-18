import socket
import json
import sys

HOST = '127.0.0.1'
PORT = 65432

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))
history = ""

def is_json(myjson):
  try:
    json_object = json.loads(myjson)
  except ValueError, e:
    return False
  return True

def handle_output(client_socket, data, err=0):
	if err == 1:
		for it in data:
			print(it)
			return
	client_socket.send(json.dumps("ACK"))
	data = client_socket.recv(1024)

	if not data:
		print("No Data received!")
		print("Exit...")
		client_socket.close()
		sys.exit()
	else:
		data = json.loads(data)
		for it in data:
			print(it)
	return

def handle_download(client_socket, command):
	client_socket.send(json.dumps("ACK"))

	f = open(command[2], 'wb')

	while True:
		packet = client_socket.recv(1024)
		if not packet or (is_json(packet) and json.loads(packet) == "DONE"):
			handle_output(client_socket, packet)
			break
		f.write(packet)
	f.close()
	return

while True:
	
	try:
		command = raw_input("prompt=> ")
	except KeyboardInterrupt:
		print("Exit...")
		client_socket.close()
		sys.exit()
	
	tokens = command.split()
	
	if len(tokens) == 0:
		continue
	
	if tokens[0] == 'history':
		print history
		continue
	
	if tokens[0] == "exit":
		client_socket.close()
		sys.exit()
	
	history += tokens[0] + "\n"
	
	client_socket.send(json.dumps(tokens))
	data = client_socket.recv(1024)
	
	if not data:
		print("No Data received!")
		print("Exit...")
		client_socket.close()
		sys.exit()
		continue
	
	data = json.loads(data)
	print(data)
	
	if data == "OUTPUT":
		handle_output(client_socket, data)
		
	elif data == "DOWNLOAD":
		handle_download(client_socket, tokens)
	else:
		print("Error Encountered!")
		handle_output(client_socket, data, 1)
		