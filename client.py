import socket
import json
import sys

HOST = '127.0.0.1'
PORT = 65432

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))
history = ""

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
		continue
	data = json.loads(data)
	for it in data:
		print(it)
