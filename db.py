import psycopg2
from pyflock import FlockClient, verify_event_token

from pyflock import Message, SendAs, Attachment, Views, WidgetView, HtmlView, ImageView, Image, Download, Button, OpenWidgetAction, OpenBrowserAction, SendToAppAction
import jwt
import json

def get_conn():
	with open('secret.json') as cred_file:
		db_creds = json.load(cred_file)

	#print db_creds
	
	conn = psycopg2.connect(
		database=db_creds["database"],
		user=db_creds["user"],
		password=db_creds["password"],
		host=db_creds["host"],
		port=db_creds["port"]
	)

	return conn

def user_add(userid, token, email_address):
	conn = get_conn()
	cur = conn.cursor()

	#cur.execute("DELETE FROM appusers WHERE userid='" + str(userid) + "'")
	cur.execute("INSERT INTO appusers (userid,email_addr,token) VALUES ('" + str(userid) + "', '" + str(email_address) + "', '" +str(token)+"');")
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
		cur.execute("INSERT INTO userfiles (userid,fileId,filename) VALUES ('"+str(userid)+"', '"+str(item[0])+"', '" + str(item[1]) +"');")
	
	conn.commit()
	conn.close()
	
	return "Successfully added all files of user"

def remove_files(userid, fileId=None):

	conn = get_conn()

	cur = conn.cursor()

	if fileId==None:
		cur.execute("DELETE FROM userfiles WHERE userid='" + str(userid) + "'")
	else:
		for file_item in fileId:
			cur.execute("DELETE FROM userfiles WHERE userid='" + str(userid) + "'" + "AND fileId='" + str(file_item) + "'")
	
	conn.commit()
	conn.close()
	
	return "Successfully unregistered files"

def watched_files_user(userId):
	conn = get_conn()

	cur = conn.cursor()

	cur.execute("SELECT fileid, filename FROM userfiles WHERE userid='" + str(userId) + "'" + "AND iswatched='TRUE';")

	rows = cur.fetchall()

	#print rows

	conn.commit()
	conn.close()
	
	return rows
		
def watch_file(userId, fileName):
	conn = get_conn()

	cur = conn.cursor()

	cur.execute("UPDATE userfiles SET iswatched = TRUE WHERE userid='" + str(userId) + "'" + "AND filename ILIKE '%" + str(fileName) + "%'")

	conn.commit()
	conn.close()
	
	return "Successfully watched files"

