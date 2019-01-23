#!/usr/bin/env python
# encoding: utf-8

import tweepy  # https://github.com/tweepy/tweepy
import csv
import logging
import time

# This script was downloaded form : https://gist.github.com/yanofsky/5436496

# Twitter API credentials
'''
consumer_key = "XyFBOTlIM6H7NePkN4TNOvpzy"
consumer_secret = "T7ZuLHZuF5N4U85beQQ633rbwb8cg6ApHK672IGIL2y1sycXQO"
access_key = "1226726778-3284hTJ6sOmD52U08scvj2Z6tJ7paSJnCVVCbnC"
access_secret = "NM4bfDPyH7ovf7aChF3CUzdwFdPs1pPQ8FvGt9UZVYtt4"
'''

class Auth:
	def __init__(self, ck, cs, ak, acs):
		self.ck = ck
		self.cs = cs
		self.ak = ak
		self.acs = acs

class API:
	def __init__(self, key):
		self.key = key
		self.authorize()
		
	def authorize(self):
		auth = tweepy.OAuthHandler(self.key.ck, self.key.cs)
		auth.set_access_token(self.key.ak, self.key.acs)
		self.api = tweepy.API(auth,wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)
	
	def get_all_tweets(self, uid, repeat = True):
		'''
		Collect all tweets of an user.
		'''

		# initialize a list to hold all the tweepy Tweets
		alltweets = []
		
		# make initial request for most recent tweets (200 is the maximum allowed count)
		new_tweets = []
		try:
			new_tweets = self.api.user_timeline(id=uid, count=200)
			alltweets.extend(new_tweets)
		except tweepy.error.TweepError as e:
			print('Exception while collecting tweet: {}'.format(e))
			self.authorize()  
		
		if not repeat:
			return new_tweets
		# save the id of the oldest tweet less one
		oldest = alltweets[-1].id - 1 if alltweets else 0
		
		# keep grabbing tweets until there are no tweets left to grab
		while len(new_tweets) > 0:
			#print "getting tweets before %s, number of tweets retrieved in this request %s." % (oldest, len(new_tweets))
			# print 'first tweet id %s, last tweet id %s' %(new_tweets[0].id, new_tweets[len(new_tweets)-1].id)
			# all subsiquent requests use the max_id param to prevent duplicates
			try:
				new_tweets = self.api.user_timeline(id=uid, count=200, max_id=oldest)
			except tweepy.error.RateLimitError as e:
				raise
			except tweepy.error.TweepError as e:
				print('Exception while collecting tweet: {}'.format(e))
				self.authorize()
			
			# save most recent tweets
			alltweets.extend(new_tweets)
			
			# update the id of the oldest tweet less one
			oldest = alltweets[-1].id - 1
			
			#print "...%s tweets downloaded so far" % (len(alltweets))
		
		return alltweets
	
	def get_user_profiles_from_ids(self, uids):
		'''Collect user profiles given user ids'''
		return self.api.lookup_users(user_ids = uids)
	
	def get_user_profiles_from_names(self, unames):
		'''Collect user profiles given user names'''
		return self.api.lookup_users(screen_names = unames)

	def get_friend_ids(self, uname):
		'''Collect ids of all the friends of an user'''
		ids = []
		try:
			for page in tweepy.Cursor(self.api.friends_ids, screen_name=uname).pages():
			    ids.extend(page)
			    time.sleep(20)
		except Exception as e:
			print('Exception while collecting friends id:',e)
		return ids

	def get_follower_ids(self, uname):
		'''Collect ids of all the followers of an user'''
		ids = []
		try:
			for page in tweepy.Cursor(self.api.followers_ids, screen_name=uname).pages():
			    ids.extend(page)
			    time.sleep(20)
		except Exception as e:
			print('Exception while collecting followers id:',e)
		return ids

	def get_tweets_from_ids(self, tweet_ids):
		'''Get all tweets given the ids'''
		return self.api.statuses_lookup(tweet_ids,include_entities=True, trim_user=False)

	def lists_subscribed(self, uname):
			ids = []
			for page in tweepy.Cursor(self.api.lists_subscriptions, screen_name=uname).pages():
			    ids.extend(page)
			    #time.sleep(20)
			return ids

	def lists_created(self, uname):
			ids = []
			#for page in tweepy.Cursor(self.api.lists_all, screen_name=uname).pages():
			 #   ids.extend(page)
			    #time.sleep(20)
			return self.api.lists_all(uname)
	def lists_member(self, uname):
			ids = []
			for page in tweepy.Cursor(self.api.lists_memberships, screen_name=uname).pages():
			    ids.extend(page)
			    #time.sleep(20)
			return ids

	def search_tweets(self, query, since = None):
		'''
		Search tweets using keyword or hashtags. 
		Parameters:
			query: search query
			since: search tweets posted after 'since'
		'''
		tweets = []
		for page in tweepy.Cursor(self.api.search,q=query,
					count=100, lang="en", since=since).pages():
			tweets.extend(page)
		return tweets

