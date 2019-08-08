#!/usr/bin/python3
import os, requests, time

while True:
	ip = os.popen(str("ip a")).read().split('inet')[4].split('/')[0].strip()

	commands = requests.get('http://localhost/beacon?ip=' + ip) 

	print (commands.content)
	
	time.sleep(10)