#!/usr/bin/python
# vim: set fileencoding=utf-8 :
from birdy.twitter import StreamClient, UserClient
from gevent.queue import Queue
import gevent
import simplejson as json

class Tweets(object):

	def __init__(self, account_details):
		self.name = account_details['name']
		self.user = account_details['user']
		self.access_token = account_details['credentials']['access_token']
		self.access_token_secret = account_details['credentials']['access_token_secret']

		self.consumer_key = account_details['credentials']['consumer_key']
		self.consumer_secret = account_details['credentials']['consumer_secret']
		self.topics = ",".join(account_details['topics'])

		self.api = None
		self.clientapi = None

	def connect(self):
		self.api = StreamClient(self.consumer_key, self.consumer_secret, self.access_token, self.access_token_secret)
		self.clientapi = UserClient(self.consumer_key, self.consumer_secret, self.access_token, self.access_token_secret)
	

	def _tweets(self, stream):
		for tw in stream.stream():
			yield tw

	def topic_tweets(self):
		if self.api is None: 
			self.connect()
		for tw in self._tweets(self.api.stream.statuses.filter.post(track=self.topics)):
			yield tw

	def timeline(self):
		response = self.clientapi.api.statuses.user_timeline.get()
		for tw in response.data:
			yield tw

	def user_tweets(self, limit=-1):
		if self.clientapi is None: 
			self.connect()

		resource = self.api.userstream.user.get()
		for tw in resource.stream():
			yield tw

	def firehose(self):
		pass
		


