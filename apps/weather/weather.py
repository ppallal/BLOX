# -*- coding: utf-8 -*-
import sys
sys.path.append('../..')
from blox import BLOX
import feedparser
import time
import urllib2, urllib,json


# TO INSTALL DEPENDENCIES #
# pip install TwitterAPI #

class weather(BLOX):
	def __init__(self):
		BLOX.__init__(self)

	def start(self):
		BLOX.start(self)
		# Register all the shit like the layouts and the callbacks
		self.newLayout("Layout","welcome.xml")

		
		
		
		#feed = feedparser.parse('http://www.news.yahoo.com/rss')
		# r = api.request('statuses/home_timeline')
		# #self.titles = map(lambda x:x.title,feed.entries)
		# # print r#response._content['user']['name']#.__dict__.keys()
		# # print r.json()[0]['user']['name']
		# self.tweets = map(lambda x:x['text'],r)
		# self.tweetnames = map(lambda x:x['user']['name'],r.json())
		# # Call layouts 
		# #self.registerCommand("next",self.next,parellel=True)
		self.renderLayout("Layout")
		# self.i = 0
		self.postWeatherFeed()

	def getCurrentTemp(self,location = "Bangalore"):
		self.baseurl = "https://query.yahooapis.com/v1/public/yql?"
		self.location = location
		self.yql_query = "select item from weather.forecast where woeid in (select woeid from geo.places where text='"+location+"') and u='c'"
		self.yql_url = self.baseurl + urllib.urlencode({'q':self.yql_query}) + "&format=json"
		self.result = urllib2.urlopen(self.yql_url).read()
		self.data = json.loads(self.result)
		self.current_temp = self.data['query']['results']['channel']['item']['condition']['temp']
		self.current_condition = self.data['query']['results']['channel']['item']['condition']['text']
		self.today_high = self.data['query']['results']['channel']['item']['forecast'][0]['high']
		self.today_low = self.data['query']['results']['channel']['item']['forecast'][0]['low']
		print "temp:",self.current_temp," condition: ",self.current_condition," today high: ",self.today_high," today low: ",self.today_low
		return self.current_temp, self.current_condition, self.today_high, self.today_low

		# Register intervals
	def postWeatherFeed(self):

		while(True):
			currenttemp, condition, today_high, today_low = self.getCurrentTemp()
			self.changeVariable("currenttemp",str(currenttemp)+"°C","text","Layout")
			self.changeVariable("condition",condition,"text","Layout")
			self.changeVariable("location",self.location,"text","Layout")
			self.changeVariable("highlow","H "+str(today_high)+"°C    L "+str(today_low)+"°C","text","Layout")
			self.refreshScreen()
			
			time.sleep(5)

	def getForLocation(self,location):
		# print "Inside next command handler"
		# self.i += 1
		# if(self.i == len(self.tweets)): i=0
		self.location = location
		# self.changeVariable("tweet",self.tweets[self.i],"text","Layout")
		# self.changeVariable("tweet",self.tweets[self.i%len(self.tweets)],"text","Layout")
		# self.changeVariable("tweetname",self.tweetnames[self.i%len(self.tweets)][:10],"text","Layout")
		self.refreshScreen()
		



	# a function which cal be called at an interval 



# if __name__ == '__main__':
	# TwitterFeed().start()
