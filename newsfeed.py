from blox import BLOX
import feedparser
import time

class NewsFeed(BLOX):
	def __init__(self):
		BLOX.__init__(self)

	def start(self):
		BLOX.start(self)
		# Register all the shit like the layouts and the callbacks
		self.newLayout("Welcome","welcome.xml")
		feed = feedparser.parse('http://www.news.yahoo.com/rss')
		self.titles = map(lambda x:x.title,feed.entries)
		# Call layouts 
		self.registerCommand("next",self.next,parellel=True)
		# self.renderLayout("Welcome") 
		self.i = 0
		# self.doJob(self.postNewsFeed)
		self.doJob(self.print_a)
		self.doJob(self.print_b)
		# time.sleep(50)
		print "-"*40

		# self.postNewsFeed()
	def print_a(self):
		for i in range(30):
			print "a"
			time.sleep(0.1)
	def print_b(self):
		for i in range(16):
			print "b"
			time.sleep(0.2)
		self.doJob(self.fail)

	def fail(self):
			print "+"*5
		# Register intervals
	def postNewsFeed(self):
		# for i in self.titles:
		while(True):
			if(self.i == len(self.titles)): i=0
			self.changeVariable("displayMesssage",self.titles[self.i],"span","Welcome")
			self.refreshScreen()
			time.sleep(3)

	def next(self):
		print "Inside next command handler"
		self.i += 1
		if(self.i == len(self.titles)): i=0
		self.changeVariable("displayMesssage",self.titles[self.i],"span","Welcome")
		self.refreshScreen()
		



	# a function which cal be called at an interval 



if __name__ == '__main__':
	NewsFeed().start()
