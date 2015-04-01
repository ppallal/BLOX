from blox import BLOX

class NewsFeed(BLOX):
	def __init__(self,renderImage):
		BLOX.__init__(self,renderImage)

	def start(self):
		BLOX.start(self)
		# Register all the shit like the layouts and the callbacks
		self.newLayout("Welcome","welcome.xml")

		# Call layouts 
		self.renderLayout("Welcome") 
		# Register intervals 

	# a function which cal be called at an interval 



if __name__ == '__main__':
	NewsFeed().start()
