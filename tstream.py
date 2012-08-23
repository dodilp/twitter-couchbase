import tweepy
import json
import hashlib
import couchbase
from tweepy.utils import import_simplejson

#Define Database connection creds 
server = "localhost:8091"
admin_username = "Administrator"
admin_password = "zztest"

#Twitter auth stuff
consumer_key = 'Az2MXuoK84LkN8dkYomwnw'
consumer_secret = 'y9qyUHmz5ioRA0ZXJN1j7LD71hG99LoEuvhGu4LDtU'
access_token_key = '227787412-XVyzpZofhDAvXOEd22R7PdSJLxgMKhn0K0ipVzMF'
access_token_secret = 'yQmalsT4Tw2vitT6PKXpLiu6eIBkfLW0NMiEaBNobvg'

#Define filter terms
filterTerms = ['bigdata', 'couchbase', 'nosql', 'DataWeek', 'CouchConf']

json = import_simplejson()
try:
	cbsclient = couchbase.Server(server, admin_username, admin_password); 
except:
	print "Cannot find Couchbase Server ... Exiting\n"
	print "----_Stack Trace_-----\n"
	raise

#Couchbase is found here so now try to create a bucket for twitter
try:
	cbsclient.create('twitter', ram_quota_mb=200, replica=1)
except:
	pass

#Try to use the twitter bucket or else switch to use default bucket
try:
	cbucket = cbsclient['twitter']
	print "Using twitter bucket"
except:
	cbucket = cbsclient['default']
	print "Using default bucket"

auth1 = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth1.set_access_token(access_token_key, access_token_secret)

class StreamListener(tweepy.StreamListener):
    json = import_simplejson()
    
    def on_status(self, tweet):
        print 'Ran on_status'

    def on_error(self, status_code):
        return False

    def on_data(self, data):
        if data[0].isdigit():
            pass
        else:
	    data_md5 = hashlib.md5(json.dumps(data, sort_keys=True)).hexdigest()
	    cbucket.set(data_md5,0,0,data)
            print(json.loads(data))


l = StreamListener()
streamer = tweepy.Stream(auth=auth1, listener=l)
streamer.filter(track = filterTerms)
