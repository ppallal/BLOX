import sys
sys.path.append('../..')
from blox import BLOX
import feedparser
import time
import urllib2, urllib,json


# TO INSTALL DEPENDENCIES #
# pip install TwitterAPI #

class stocks(BLOX):
	def __init__(self):
		BLOX.__init__(self)

	def start(self):
		BLOX.start(self)
		# Register all the shit like the layouts and the callbacks
		self.newLayout("Layout","welcome.xml")
		self.symbols = {"apple":"AAPL","google":"GOOG","microsoft":"MSFT","infosys" : "INFY"}
		
		#feed = feedparser.parse('http://www.news.yahoo.com/rss')
		# r = api.request('statuses/home_timeline')
		# #self.titles = map(lambda x:x.title,feed.entries)
		# # print r#response._content['user']['name']#.__dict__.keys()
		# # print r.json()[0]['user']['name']
		# self.tweets = map(lambda x:x['text'],r)
		# self.tweetnames = map(lambda x:x['user']['name'],r.json())
		# # Call layouts 
		self.registerCommand("of",self.getStockData,parellel=True)
		self.renderLayout("Layout")
		# self.i = 0
		self.postStockFeed()

	def getStockData(self,companyname = "microsoft"):
		self.company = self.symbols[companyname]
		self.baseurl = "https://query.yahooapis.com/v1/public/yql?"
		self.yql_query = 'select * from yahoo.finance.quotes where symbol="MSFT"'
		self.yql_url = self.baseurl + urllib.urlencode({'q':self.yql_query}) + "&format=json&diagnostics=true&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys&callback="
		self.result = urllib2.urlopen(self.yql_url).read()
		self.data = json.loads(self.result)
		# print self.data['query']['results']
		print self.data['query']['results']['quote']['Ask']
		print self.data['query']['results']['quote']['ChangeinPercent']
		print self.data['query']['results']['quote']['DaysHigh']
		print self.data['query']['results']['quote']['DaysLow']
		print self.data['query']['results']['quote']['LastTradeTime']
		self.ask_price = self.data['query']['results']['quote']['Ask']
		self.perc = self.data['query']['results']['quote']['ChangeinPercent']
		self.today_high = self.data['query']['results']['quote']['DaysHigh']
		self.today_low = self.data['query']['results']['quote']['DaysLow']
		self.year_high = self.data['query']['results']['quote']['YearHigh']
		self.year_low = self.data['query']['results']['quote']['YearLow']
		self.last_trade_time = self.data['query']['results']['quote']['LastTradeTime']
		print "ask price:",self.ask_price," percentage: ",self.perc," today high: ",self.today_high," today low: ",self.today_low
		return self.ask_price, self.perc, self.today_high, self.today_low, self.last_trade_time,self.year_high, self.year_low

		# Register intervals
	def postStockFeed(self):

		while(True):
			ask_price, perc, today_high, today_low, last_trade_time,year_high, year_low = self.getStockData()
			self.changeVariable("ask_price","$ "+str(ask_price),"text","Layout")
			self.changeVariable("perc",str(perc),"text","Layout")
			self.changeVariable("highlow","MON H $"+str(today_high)+" L $"+str(today_low),"text","Layout")
			self.changeVariable("yearhighlow","YEAR H $"+str(year_high)+" L $"+str(year_low),"text","Layout")
			self.changeVariable("last_trade_time",str(last_trade_time),"text","Layout")
			if(float(perc.strip('%'))<0.0):
				self.changeVariable("conditionimg","down_arrow.pbm","text","Layout")
			else:
				self.changeVariable("conditionimg","up_arrow.pbm","text","Layout")
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
