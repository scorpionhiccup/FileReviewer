#from __future__ import print_function
import httplib2
import os
import pprint

from apiclient import discovery
from apiclient import errors
from apiclient import http
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

SCOPES = 'https://www.googleapis.com/auth/drive https://www.googleapis.com/auth/userinfo.email'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Drive API Python Quickstart'


def get_credentials(userID):
	"""Gets valid user credentials from storage.

	If nothing has been stored, or if the stored credentials are invalid,
	the OAuth2 flow is completed to obtain the new credentials.

	Returns:
		Credentials, the obtained credential.
	"""
	home_dir = os.path.expanduser('~')

	#credential_dir = os.path.join(home_dir, userID, '.credentials')
	credential_dir = os.path.join(home_dir, '.credentials')
	if not os.path.exists(credential_dir):
		os.makedirs(credential_dir)
	credential_path = os.path.join(credential_dir,
								   'drive-python-quickstart.json')

	store = Storage(credential_path)
	credentials = store.get()
	if not credentials or credentials.invalid:
		flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
		flow.user_agent = APPLICATION_NAME
		#if flags:
		credentials = tools.run_flow(flow, store, None)
		#else: # Needed only for compatibility with Python 2.6
		#	credentials = tools.run(flow, store)
		print('Storing credentials to ' + credential_path)
	return credentials


def getUserInfo(userID):
	service = getService(userID)
	try:
		about = service.about().get().execute()

		#print 'Current user name: %s' % about['name']
		#print about['user']
		
		return about['user']['emailAddress']	
	except errors.HttpError, error:
		print 'An error occurred: %s' % error

def getService(userID):
	credentials = get_credentials(userID)
	http = credentials.authorize(httplib2.Http())
	service = discovery.build('drive', 'v2', http=http, cache_discovery=False)
	return service

def retrieveAllFiles(userID):
	"""Retrieve a list of File resources.

	Args:
	service: Drive API service instance.
	Returns:
	List of File resources.
	"""
	service = getService(userID)

	result = []
	page_token = None
	#pp = pprint.PrettyPrinter(indent=4)

	while True:
		try:
			param = {'maxResults': 5, 'orderBy': "modifiedByMeDate desc, title"}
			if page_token:
				param['pageToken'] = page_token
			files = service.files().list(**param).execute()


			for item in files['items']:
				result.append([item['id'], item['title']])
				#print result[-1]

			#result.extend(files['items'])
			#pp.pprint(files['items'])
			#print json.dumpfiles['items']
			page_token = files.get('nextPageToken')
			if not page_token:
				break
			break
		except errors.HttpError, error:
			print 'An error occurred: %s' % error
			break
	return result

def fetchFile(userID, file_id):
	service = getService(userID)

	try:
		file = service.files().get(fileId=file_id).execute()

		print 'Title: %s' % file['title']
		print 'URL: %s' % file['exportLinks']['text/plain']
		print file
	except errors.HttpError, error:
		print 'An error occurred: %s' % error


def listFiles(userID):
	"""Shows basic usage of the Google Drive API.

	Creates a Google Drive API service object and outputs the names and IDs
	for up to 10 files.
	"""
	
	service = getService(userID)

	results = service.files().list(
		pageSize=10, fields="nextPageToken, files(id, name)").execute()
	items = results.get('files', [])
	if not items:
		print('No files found.')
	else:
		print('Files:')
		for item in items:
			print('{0} ({1})'.format(item['name'], item['id']))

def print_revision(userID):
	"""Print information about the specified revision.

	Args:
	service: Drive API service instance.
	file_id: ID of the file to print revision for.
	revision_id: ID of the revision to print.
	"""
	service = getService(userID)
	fileId = "1w9-k8LZFc_U7iEu1MEvfVN8fi_oR5b7uKIl8WGrY240"
	revision_id = 12605

	try:
		revision = service.revisions().get(
			fileId=fileId, revisionId=revision_id).execute()

		#print 'Revision ID: %s' % revision['id']
		#print 'Modified Date: %s' % revision['modifiedDate']
		#print revision['selfLink']
		print revision
		resp, content = service._http.request(revision['selfLink'])
		print resp
		print content
		if revision.get('pinned'):
		  print 'This revision is pinned'
	except Exception, error:
		print 'An error occurred: %s' % error


if __name__ == '__main__':
	#getUserInfo()
	#print listFiles()
	#print retrieve_all_files()
	#print_revision(userID)
	pass