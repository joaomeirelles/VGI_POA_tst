#!/usr/bin/python

#import libraries
import sys
import tweepy
import csv
import datetime

#pass API parameters, can be generated here: https://dev.twitter.com/oauth/overview/application-owner-access-tokens
consumer_key = ""
consumer_secret = ""
access_token = ""
access_secret = ""

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)

#define function to collect tweets
class CustomStreamListener(tweepy.StreamListener):
	def on_status(self, status):
		if status.geo != None:
			with open('poa_tst.csv', 'a') as f:
				writer = csv.writer(f)
				writer.writerow([status.user.id_str, status.lang, status.text, status.created_at + datetime.timedelta(hours = -2), status.geo['coordinates'][0], status.geo['coordinates'][1]])
	def on_error(self, status_code):
		print(sys.stderr, 'Encountered error with status code:', status_code)
		return True # Don't kill the stream
	def on_timeout(self):
		print(sys.stderr, 'Timeout...')
		return True # Don't kill the stream

#dump data to a CSV. this should be further dumped into a DB
# open a file to write (mode "w"), and create a CSV writer object
csvfile = open("poa_tst_plot.csv", "w")
csvwriter = csv.writer(csvfile)

# add headings to our CSV file
#row = [ "user", "source", "lang", "datatime", "lat", "lon" ]
row = [ "user", "lang", "text","datatime", "lat", "lon" ]
csvwriter.writerow(row)

poa_geobox = [-51.6632,-30.4569,-50.7005,-29.7715]
sapi = tweepy.streaming.Stream(auth, CustomStreamListener()).filter(locations=poa_geobox)

#sapi.filter(track=['Rio']) ##example of filtering by term

