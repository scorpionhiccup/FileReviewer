import psycopg2
from pyflock import FlockClient, verify_event_token

from pyflock import Message, SendAs, Attachment, Views, WidgetView, HtmlView, ImageView, Image, Download, Button, OpenWidgetAction, OpenBrowserAction, SendToAppAction
import jwt

def get_conn():
	conn = psycopg2.connect(
		database='de5neind23v615',
		user='dbmvblmsvjrnzz',
		password='0144a342ab7473f045472d58aacb1e0137763d1acf006e5ba41f3561e6ae787c',
		host='ec2-23-21-76-49.compute-1.amazonaws.com',
		port='5432'

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
	
	return "Successfully registered"
