import time
import subprocess
import os
import urllib2
import re
from datetime import datetime

from db import watched_files_user, get_all_users, get_email, get_userId
from drive import fetchFile
from util import send_msg


def gitDiff(dir_addr):
	cwd = os.getcwd()
	os.chdir(dir_addr)
	out = subprocess.Popen(['git', 'diff'], stdout=subprocess.PIPE)
	os.chdir(cwd)
	return out.stdout.read()

def gitCommit(dir_addr, email):
	cwd = os.getcwd()
	os.chdir(dir_addr)
	subprocess.Popen(['git', 'add', 'content'], stdout=subprocess.PIPE)
	subprocess.Popen(['git', 'commit', '-m', 'data updated at %s' % (str(datetime.now())), '--author="User <%s>"' % (email)])
	os.chdir(cwd)

def initializeGitRepo(dir_addr, email_addr):
	os.mkdir(dir_addr)
	file_addr = os.path.join(dir_addr, 'content')
	# Create a file named content
	open(file_addr, 'a').close()

	cwd = os.getcwd()
	os.chdir(dir_addr)
	subprocess.Popen(['git', 'init'], stdout=subprocess.PIPE)
	os.chdir(cwd)

	#print "init"
	gitCommit(dir_addr, email_addr)
	#print "init commit done"


def sendNotification(email_addr, fileName):
	userId = get_userId(email_addr)

	send_msg(userId, "Review Changes in the file:" + str(fileName))
	send_msg(userId, "https://docs.google.com/document/d/1Wnm0NiQ6jP-72shMfZKr53stuh5wjnVtVbQUn3PHmgI/edit?usp=sharing")

	pass

def main():
	if not os.path.exists('data'):
		os.mkdir('data')

	while True:
		for userId in get_all_users():
			userId="u:yata4oday666otrt"
			# List of files being watched
			files = watched_files_user(userId)
			
			for f in files:
				url, email_addr = fetchFile(userId, f[0])

				content = urllib2.urlopen(url).read()

				dir_addr = os.path.join('data', f[0])

				if not os.path.exists(dir_addr):
					initializeGitRepo(dir_addr, email_addr)

				file_addr = os.path.join(dir_addr, 'content')
				with open(file_addr, 'w') as f:
					f.write(content)

				diff = gitDiff(dir_addr)
				if not diff:
					continue

				gitCommit(dir_addr, email_addr)
				reviewers = findReviewers(dir_addr, diff)
				for r in reviewers:
					sendNotification(r, f[1])

		time.sleep(1000)

def isMeta(line):
	return (line.startswith("@@") or line.startswith('+++')
			or line.startswith('---'))

def getImpLines(diff):
	diff = diff.strip().split("\n")[2:]
	ans = []
	if not diff:
		return ans

	for i, l in enumerate(diff):
		if isMeta(l):
			continue
		
		if l[0] != " ":
			if l[0] == "-":
				line = l
			else:
				j = i
				while j >= 0:
					j -= 1
					if isMeta(diff[j]):
						break
					if diff[j][0] == '+':
						continue
					line = diff[j]
					break
			try:
				ans.append(line[1:])
			except UnboundLocalError:
				pass
	return ans

def getEmailFromLog(dir_addr, line):
	cwd = os.getcwd()
	os.chdir(dir_addr)
	out = subprocess.Popen(['git', 'log', '-S', line, 'content'], stdout=subprocess.PIPE)
	out = out.stdout.read()
	os.chdir(cwd)

	try:
		out = out.split("\n")[1]
		return re.findall(r'^Author: .* <(.*)>$', out)[0]
	except IndexError:
		return ''

def findReviewers(dir_addr, diff):
	lines = getImpLines(diff)
	#print lines
	reviewers = set([])
	for line in lines:
		email = getEmailFromLog(dir_addr, line)
		reviewers.add(email)

	return list(reviewers)


if __name__ == "__main__":
	main()
	# initializeGitRepo('abcd')
	# gitCommit('abcd')