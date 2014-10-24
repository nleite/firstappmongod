#!/usr/bin/python
# vim: set fileencoding=utf-8 :
import imaplib
import email

class Gmail(Account):

	def __init__(self, account_details):
		"""
		:account_details - dictionary that contains the internals configuration to connect to gmail account_details
		"""
		super(Gmail, self).__init__(parser)
		self.user = account_details['credentials']['user']
		self.pwd = account_details['credentials']['password']
		
		self.imap = account_details['imap']

		self.tls = account_details['tls']
		self.RFC = "(RFC822)"

		self.excluded_folders = account_details['excluded_folders']

		self.server = None

	def connect(self):
		self.server = imaplib.IMAP4_SSL(self.imap)
		self.server.login(self.user, self.pwd)

	def load_email(self, folder, limit=-1, criterion='ALL',):

		if self.server is None:
			self.connect()

		if folder is None:
			res, folders = self.server.list()
			for element in folders:
				f = element.split(' ')[-1].replace('"', '')
				if f in self.excluded_folders:
					break
				for mail in self.load_email(f, 1):
					yield mail
			return
			
		res, data = self.server.select(folder)

		if res == "NO":
			print "%s folder does not have info" % folder 
			return
		res, data = self.server.search("UTF-8", 'ALL')
		ids = data[0].split()
		for mid in ids[:limit]:
			res, data = self.server.fetch(mid, self.RFC)
			yield email.message_from_string(data[0][1])


