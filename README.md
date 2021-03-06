# Communication Networks - Assignment
- A client-server pipeline for file sharing and indexed searching.

#### Swapnil Pakhare - 20161199
#### Pooja Srinivas - 20171403

## REQUIREMENTS:
- To run this project, python version "2.7" is needed.
- Needed python libraries:
	- socket
	- datetime
	- sys
	- os
	- json
	- hashlib

## RUN:
- First run server and then, in another window, start client using:

```bash
python server.py
python client.py
```

## Functionality:

### Commands Implemented:
- index flag(args)
	- flag is "longlist" with args[0] being an extension of format "\*.ext" and args[1] being a string keyword
	- flag is "shortlist" with args being an extension of format "\*.ext"
- filehash flag(args)
	- flag is checkall with no args
	- flag is verify with args being file_name
- download flag(args)
	- flag is "TCP" with args being file_name
	- flag is "UDP" with args being file_name

- See ![here](./problem_statement.pdf) for full description of commands.

## Usage:

#### 1. Index Longlist Examples:
```bash
prompt=> index longlist
prompt=> index longlist *.pdf
prompt=> index longlist *.pdf apples
prompt=> index longlist *.txt programmer
```
Note:
- Extensions have to be in the format - \*.extension.
- Word at the end need to be without quotes.
- Returns a list of files that adhere to arguments passed alongwith file_name, timestamp and file_size.

#### 2. Index Shortlist Examples:
```bash
prompt=> index shortlist timestamp1 timestamp2
prompt=> index shortlist timestamp1 timestamp2 *.pdf
prompt=> index shortlist timestamp1 timestamp2 *.txt
prompt=> index shortlist 19-03-2019 13:05:45 20-03-2019 00:00:00
prompt=> index shortlist 19-03-2019 13:05:45 22-03-2019 13:59:05 *.py
```

Note:
- timestamp has to be in the format - DD-MM-YYYY hh:mm:ss
- Extensions have to be in the format - \*.extension.
- Returns a list of files in current directory that adhere to arguments passed alongwith file_name, timestamp and file_size.

#### 3. FileHash Checkall Examples:
```bash
prompt=> filehash checkall
```
Note:
- Returns a list of all files in current directory alongwith checksum, file_name and timestamp.

#### 4. FileHash Verify Examples:
```bash
prompt=> filehash verify file_name
```
Note:
- Returns the name, checksum and timestamp of the file with name 'file_name' in current directory.

#### 5. Download TCP Examples:
```bash
prompt=> download TCP file_name
```

Note:
- Returns the file_name, checksum, timestamp and file_size of the file in current directory and also downloads the file from server to client using TCP.

#### 6. Download UDP Examples:
```bash
prompt=> download UDP file_name
```

Note:
- Returns the file_name, checksum, timestamp and file_size of the file in current directory and also downloads the file from server to client using UDP.

## Implementation:

- There is a single client and a single server. By default, both of these run on localhost and implement the loopback interface.

- Persistent connection has been used for TCP socket and non-persistent has been used for UDP. All commands except file sharing through UDP have been implemented using TCP.

- A "handshake" has been implemented wherein server sends message "OUTPUT" or "DOWNLOAD" to relay type of command provided. Then client sends "ACK" to acknowledge this and handles commands on it's end. Server receives this "ACK" and then proceeds with it's task. File transfer is a special case. At the end of file transfer using TCP, a "DONE" is also send to signify end of transfer. This wouldn't have been necessary in case of non-persistent connection as socket could've simply been closed at the end of file transfer from server but in our case, we need to signify end of transfer in some manner and hence this system is used. File transfer using UDP employs a timeout to end connection.

### 1. index
- Arguments are checked and required action is taken. Ex. Shortlist needs timestamps but not longlist.
- Extensions (if any) are retreived and then files fitting extension (and contain keyword if needed) are collected.
- Required fields of all these files are appended to a list and returned.

### 2. filehash
- Arguments are checked and required action is taken. Ex. checkall needs no more args whereas verify needs file_name as well.
- In case of checkall, all files are collected and required fields are returned.
- In case of verify, file is searched for in current directory and if found, required fields are returned.

### 3. download
- As mentioned earlier, initial handshake takes place.
- server receives acknowledgement and proceeds with file transfer.
- In case of TCP, file is found and sent using existing socket.
- In case of UDP, socket for UDP is first created and then file is sent using this new socket. As soon as file transfer is over, socket is destroyed.
- Await acknowledgement of receiving file from client and then sent required fields related to file.

## Scope for Improvement:
- Better error handling can be implemented
- Code can be restructured to be cleaner
- File manipulations can be implemented
- Threading can be used to run multiple clients/servers.
- Log of actions of each side can be improved.
