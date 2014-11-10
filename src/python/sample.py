#!/usr/bin/python
# vim: set fileencoding=utf-8 :
from datahub.twitterlib import Tweets
from datahub.maillib import Gmail
from pymongo import MongoClient
from bson import json_util
import simplejson as json
def mail(col):
    account_details = {
        'name': 'norberto@mongodb.com',
        'credentials':{'user': 'norberto@10gen.com', 'password': 'gzauaexxpurufliy'}, 
        'imap': 'imap.gmail.com', 'tls': True,
        'blacklist_folders': [u'\\Noselect'],
        'whitelist_folders': [u'mongodb-user']

    }

    mail = Gmail(account_details)
    mail.connect()


    ubulk = col.initialize_unordered_bulk_op()

    for m in mail.load_email(None, 10):
        try:
            m['account']=account_details['name']
            col.insert(m)
            #j =  json.dumps(m, indent=4 * ' ', default=json_util.default)  
        except Exception, e:
            print "ERROR %s" % e
            print m
    #ubulk.execute()

def tweets(col):
    account_details = {
        'name': 'nleite_twitter',
        'user': 'nleite',
        'credentials': {
            'access_token': '18136342-qx7caFEKr9rGb8yhuxp6gZygszwtm73bmAXG45c07',
            'access_token_secret': '46r0uHrvY7e6OiwxsmNk6m0CqWQS3D3nYMkSUNDlXuOMC',
            'consumer_key': 'pOC3SwyaleFnF7HNiQ4VofXDz',
            'consumer_secret': '9wnavUJlt1wjiPJxhtgElNO5CEsMxKS8M7GgsH7005yJuzsvu3',
        },
        'topics': ['mongodb', 'nsa', 'google']
    }


    t = Tweets(account_details)
    t.connect()
    """
    gevent.spawn(tweets, t).join()
    gevent.joinall([
        gevent.spawn(user_stream, t.queue, t.api),
        gevent.spawn(topic_stream, t.queue, t.api, 'twitter')
    ])
    """
    for tw in t.timeline():
        #doc = json.loads(tw, default=json_util.default)
        col.insert(tw)
    """     
    for tw in t.user_tweets():
        json.dumps(tw, indent=4 * ' ')
    """


col = MongoClient()['firstapp2']['messages']
col.drop()

mail(col)
#tweets(col)
