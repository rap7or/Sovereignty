#!/usr/bin/python3
import os, requests, time, socket, json

while True:
	hn = socket.gethostname()
	ip = socket.gethostbyname(hn)
	commands = requests.get('http://localhost/beacon?ip=' + ip) 
	commands = json.loads(str(commands.content, 'utf-8'))
	for cmd in commands:
		print(cmd)
	
	time.sleep(10)