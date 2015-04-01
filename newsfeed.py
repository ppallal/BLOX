from blox import BLOX
import feedparser
import time

class NewsFeed(BLOX):
	def __init__(self,renderImage):
		BLOX.__init__(self,renderImage)

	def start(self):
		BLOX.start(self)
		# Register all the shit like the layouts and the callbacks
		self.newLayout("Welcome","welcome.xml")
		feed = feedparser.parse('http://www.news.yahoo.com/rss')
		self.titles = map(lambda x:x.title,feed.entries)
		# Call layouts 
		self.renderLayout("Welcome") 
		self.postNewsFeed()

		# Register intervals
	def postNewsFeed(self):
		for i in self.titles:
			self.changeVariable("displayMesssage",i,"span","Welcome")
			self.refreshScreen()
			time.sleep(1)
		


	# a function which cal be called at an interval 



if __name__ == '__main__':
	NewsFeed().start()
