from blox import BLOX
import feedparser
import time

class NewsFeed_links(BLOX):
	def __init__(self,renderImage):
		BLOX.__init__(self,renderImage)

	def start(self):
		BLOX.start(self)
		# Register all the shit like the layouts and the callbacks
		self.newLayout("Welcome1","welcome.xml")
		feed = feedparser.parse('http://www.news.yahoo.com/rss')
		self.titles = map(lambda x:x.link,feed.entries)
		# Call layouts 
		self.registerCommand("next",self.next,parellel=True)
		self.renderLayout("Welcome1") 
		self.i = 0
		self.postNewsFeed()

		# Register intervals
	def postNewsFeed(self):
		# for i in self.titles:
		while(True):
			if(self.i == len(self.titles)): i=0
			self.changeVariable("displayMesssage",self.titles[self.i],"span","Welcome1")
			self.refreshScreen()
			time.sleep(3)

	def next(self):
		print "Inside next command handler"
		self.i += 1
		if(self.i == len(self.titles)): i=0
		self.changeVariable("displayMesssage",self.titles[self.i],"span","Welcome1")
		self.refreshScreen()
		



	# a function which cal be called at an interval 



if __name__ == '__main__':
	NewsFeed().start()
