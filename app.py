#!/usr/bin/env python
from __future__ import with_statement
__author__ = 'Sharvil'

import signal
from flask import Flask, request
from flask_wtf.csrf import CSRFProtect
import sys
import os
import json

import logging
logging.basicConfig(level=logging.DEBUG) 

from pyflock import FlockClient, verify_event_token
from pyflock import Message, SendAs, Attachment, Views, WidgetView, HtmlView, ImageView, Image, Download, Button, OpenWidgetAction, OpenBrowserAction, SendToAppAction
#from slashcommands import ndreminder,widgetview,echo

from db import user_add, user_remove, add_files, remove_files, watch_file, watched_files_user
from drive import listFiles, retrieveAllFiles, getUserInfo, fetchFile

from util import send_msg

app = Flask(__name__)
csrf = CSRFProtect(app)

tokens = {}


try:
	with open('./tokens.json') as data_file:    
		tokens = json.load(data_file)
except Exception as e:
	tokens = {}
	#raise e

def signal_handler(signal, frame):
	try:
		sys.exit(0)
	except Exception, e:
		print e
		sys.exit(1)

@app.route('/')
def hello():
	return "Hello World!"

@app.route('/sample/')
def sample():
	userId = ""
	files = watched_files_user(userId)

	for file in files:
		fetchFile(userId, file[0])

	return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

@app.route('/events/', methods=['post'])
@csrf.exempt
def events():
	content = request.get_json(silent=True, force=True)
	name = content['name']

	if name == "app.install":
		userId = content['userId']
		token = content['token']

		#print userId

		email_addr = getUserInfo(userId)
		#listFiles()
		result = retrieveAllFiles(userId)
		
		remove_files(userId)
		user_remove(userId)

		#print result
		add_files(userId, result)

		#print_revision(userId)
		user_add(userId, token, email_addr)
		
		return json.dumps({'success':True}), 200, {'ContentType':'application/json'}
	
	elif name == "app.uninstall":
		userId = content['userId']
		
		remove_files(userId)
		user_remove(userId)		

		return json.dumps({'success':True}), 200, {'ContentType':'application/json'}
	
	elif name == "client.slashCommand":
		userId = content['userId']
		userName = content['userName']
		chat = content['chat']
		chatName = content['chatName']
		command = content['command']
		text = ''
		if content['text']:
			text = content['text']

		try:
			if str(text):
				#print userId
				watch_file(userId, str(text))
				send_msg(userId, "Watching File: " + str(text))
		except Exception as e:
			send_msg(userId, "Unable to Watch File:" + str(text))

		return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

	return json.dumps({'success':False}), 201, {'ContentType':'application/json'} 

if __name__ == '__main__':
	signal.signal(signal.SIGINT, signal_handler)
	signal.signal(signal.SIGTERM, signal_handler)
	port = 8080
	if len(sys.argv)>=2:
		port = sys.argv[1]
	app.run(port=port)
	signal.pause()
