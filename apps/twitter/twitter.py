import sys
sys.path.append('../..')
from blox import BLOX
import feedparser
import time
from TwitterAPI import TwitterAPI


# TO INSTALL DEPENDENCIES #
# pip install TwitterAPI #

class twitter(BLOX):
	def __init__(self):
		BLOX.__init__(self)

	def start(self):
		BLOX.start(self)
		# Register all the shit like the layouts and the callbacks
		self.newLayout("Layout","welcome.xml")
		self.api = TwitterAPI('K9WyKRZkSv1piH99YGa1r8v7E','bnoWuT5segvhCb64MX1rXyHXr6d5NKThp0wfIqiYEVLVN4dDT1', '69908245-bh8asTTeVVFxJM7isoPasVatElUmvSQjK78NIz79u', 'Qa4wd9U8wSIhJccqtNo5sB9GuoyqxmNGc1SPuZqu6hQvY')
		#feed = feedparser.parse('http://www.news.yahoo.com/rss')
		r = self.api.request('statuses/home_timeline')
		#self.titles = map(lambda x:x.title,feed.entries)
		# print r#response._content['user']['name']#.__dict__.keys()
		# print r.json()[0]['user']['name']
		self.tweets = map(lambda x:x['text'],r)
		self.tweetnames = map(lambda x:x['user']['name'],r.json())
		# Call layouts 
		self.registerCommand("on",self.tweetsOn,parellel=True)
		self.renderLayout("Layout")
		self.i = 0
		self.postTwitterFeed()

		# Register intervals
	def postTwitterFeed(self):
		# for i in self.titles:
		while(True):
			if(self.i == len(self.tweets)): i=0
			self.changeVariable("tweet",self.tweets[self.i%len(self.tweets)],"text","Layout")
			self.changeVariable("tweetname",self.tweetnames[self.i%len(self.tweets)][:10],"text","Layout")
			self.refreshScreen()
			self.i+=1
			time.sleep(3)

	# def next(self):
	# 	# print "Inside next command handler"
	# 	self.i += 1
	# 	if(self.i == len(self.tweets)): i=0
	# 	# self.changeVariable("tweet",self.tweets[self.i],"text","Layout")
	# 	self.changeVariable("tweet",self.tweets[self.i%len(self.tweets)],"text","Layout")
	# 	self.changeVariable("tweetname",self.tweetnames[self.i%len(self.tweets)][:10],"text","Layout")
	# 	self.refreshScreen()

	def tweetsOn(self,args):
		r = self.api.request('search/tweets',{'q':args})
		#self.titles = map(lambda x:x.title,feed.entries)
		# print r#response._content['user']['name']#.__dict__.keys()
		# print r.json()[0]['user']['name']
		self.tweets = map(lambda x:x['text'],r)
		self.tweetnames = map(lambda x:x['user']['name'],r.json())
		



	# a function which cal be called at an interval 



# if __name__ == '__main__':
	# TwitterFeed().start()
