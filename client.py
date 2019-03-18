import socket
import json
import sys

HOST = '127.0.0.1'
PORT = 65432
UDP_PORT = 9999

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

<<<<<<< HEAD
def handle_download_tcp(client_socket, command):
=======
def handle_download(client_socket, command):
	client_socket.send(json.dumps("ACK"))
>>>>>>> 8f8644c1b763a83fe624fe460019f9853f1aeb72

	f = open(command[2], 'wb')

	while True:
		packet = client_socket.recv(1024)
		if not packet or (is_json(packet) and json.loads(packet) == "DONE"):
<<<<<<< HEAD
			print("File Downloaded")
=======
>>>>>>> 8f8644c1b763a83fe624fe460019f9853f1aeb72
			handle_output(client_socket, packet)
			break
		f.write(packet)
	f.close()
	return

<<<<<<< HEAD
def handle_download_udp(udp_socket, client_socket, command):
	f = open(command[2], 'wb')

	data, addr = udp_socket.recvfrom(1024)
	try:
		while(data):
			print("Receiving...")
			f.write(data)
			udp_socket.settimeout(2)
			data, addr = udp_socket.recvfrom(1024)
	except socket.timeout:
		f.close()
		udp_socket.close()
	data = client_socket.recv(1024)
	if not data:
		print("Error : No acknowledgement received!")
	elif is_json(data) and json.loads(data) == "DONE":
		print("File Downloaded")
		handle_output(client_socket, data)
	return

=======
>>>>>>> 8f8644c1b763a83fe624fe460019f9853f1aeb72
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
<<<<<<< HEAD
		client_socket.send(json.dumps("ACK"))
		if tokens[1] == "TCP":
			handle_download_tcp(client_socket, tokens)
		else:
			udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			udp_socket.bind((HOST, UDP_PORT))

			handle_download_udp(udp_socket, client_socket, tokens)
=======
		handle_download(client_socket, tokens)
>>>>>>> 8f8644c1b763a83fe624fe460019f9853f1aeb72
	else:
		print("Error Encountered!")
		handle_output(client_socket, data, 1)
		