from pyflock import FlockClient, verify_event_token
from pyflock import Message, SendAs, Attachment, Views, WidgetView, HtmlView, ImageView, Image, Download, Button, OpenWidgetAction, OpenBrowserAction, SendToAppAction

def send_msg(userId, text):
	app_id = '3634e691-a7e4-45be-a42a-ae1155073d74'
	bot_token = '44cd66c1-5e89-4b09-98a6-c81e1e4ca33d'

	flock_client = FlockClient(token=bot_token, app_id=app_id)

	msg = Message(to=userId, text=text)

	# returns a message id
	res = flock_client.send_chat(msg)
	print(res)


if __name__ == '__main__':
	#send_msg(userId, "Review Changes in the file:" + str(fileName))