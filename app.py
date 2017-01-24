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

from db import user_add, user_remove
from drive import listFiles

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

@app.route('/events/', methods=['post'])
@csrf.exempt
def events():
	content = request.get_json(silent=True, force=True)
	name = content['name']

	if name == "app.install":
		userId = content['userId']
		token = content['token']

		listFiles()
		user_add(userId, token)
		
		return json.dumps({'success':True}), 200, {'ContentType':'application/json'}
	elif name == "app.uninstall":
		userId = content['userId']
		
		user_remove(userId)		
		return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

	return json.dumps({'success':False}), 201, {'ContentType':'application/json'} 

'''
@app.route('/events/app.install', methods=['POST'])
def token_init():
	input_json = request.get_json(force=True)
	print input_json


@app.route('/events/app.uninstall', methods=['POST'])
def token_uninit():
	input_json = request.get_json(force=True)
	print input_json

'''

@app.route('/sample/')
def sample():

	user_id = 'u:yata4oday666otrt'
	
	if tokens:
		user_id = tokens.keys()[0]

	bot_token = ''
	if tokens[user_id]:
		bot_token = tokens[user_id]
	
	user_token = bot_token

	app_id = '7d6ceaa6-21f1-47f5-b3c1-b8ea07313f29'
	app_secret = 'a9c64196-332a-4d8c-8054-8aad6d25a6b2'

	#if verify_event_token()


if __name__ == '__main__':
	signal.signal(signal.SIGINT, signal_handler)
	signal.signal(signal.SIGTERM, signal_handler)
	port = 8080
	if len(sys.argv)>=2:
		port = sys.argv[1]
	app.run(port=port)
	signal.pause()
