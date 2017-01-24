import psycopg2
from pyflock import FlockClient, verify_event_token

from pyflock import Message, SendAs, Attachment, Views, WidgetView, HtmlView, ImageView, Image, Download, Button, OpenWidgetAction, OpenBrowserAction, SendToAppAction
import jwt
import json

def get_conn():
	with open('secret.json') as cred_file:
		db_creds = json.load(cred_file)

	print db_creds
	
	conn = psycopg2.connect(
		database=db_creds["database"],
		user=db_creds["user"],
		password=db_creds["password"],
		host=db_creds["host"],
		port=db_creds["port"]
	)

	return conn

def user_add(userid, token):
	conn = get_conn()
	cur = conn.cursor()

	#cur.execute("DELETE FROM appusers WHERE userid='" + str(userid) + "'")
	cur.execute("INSERT INTO appusers (userid,token) VALUES ('"+str(userid)+"', '"+str(token)+"');")
	conn.commit()
	conn.close()
	
	return "Successfully registered"

def user_remove(userid):
	conn = get_conn()

	cur = conn.cursor()

	cur.execute("DELETE FROM appusers WHERE userid='" + str(userid) + "'")
	conn.commit()
	conn.close()
	
	return "Successfully unregistered"

def add_files(userid, result):
	conn = get_conn()

	cur = conn.cursor()

	for item in result:
		cur.execute("INSERT INTO userfiles (userid,token) VALUES ('"+str(userid)+"', '"+str(item)+"');")
		cur.execute("INSERT INTO userfiles (userid,fileId) VALUES ('"+str(userid)+"', '"+str(item)+"');")
	
	conn.commit()
	conn.close()
	
	return "Successfully added all files of user"
