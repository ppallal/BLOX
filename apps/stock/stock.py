from blox import BLOX
import time 
import urllib2

class stock(BLOX):
	"""docstring for stock"""
	def __init__(self):
		# self.arg = arg
		BLOX.__init__(self)
		self.symbols = {} # GEt this shit from a stored file 
		self.displayItems = {}
		self.i = 0

	def start(self):
		BLOX.start(self)
		self.fetchSymbols()
		self.doJob(self.keepFetching)
		self.doJob(self.change)
		print "Started"


	def send(self,addr):
		# dat=json.dumps(data)
		request = urllib2.Request(addr)
		request.add_header('Content-type', 'text/csv')
		response = urllib2.urlopen(request)
		#print response,type(response)
		ret = response.read()
		# retv = json.loads(ret)
		retv = ret.split(",")
		return retv


	def change(self):
		while(True):
			try:
				for i in self.displayItems:
					print i,self.displayItems[i]
					time.sleep(1)
			except:
				pass

		



	def fetchSymbols(self):


		# Logic to read from a stored file and populate self.symbols 
		self.symbols = {"apple":"AAPL","google":"GOOG","microsoft":"MSFT","infosys" : "INFY"}

		pass


	def keepFetching(self):
		print "Fetching"
		while True:
			self.fetch()
			time.sleep(5)

	def fetch(self):
		# self.displayItems = []
		for i in self.symbols.values():
			# print "for : ",i
			data = self.send("http://finance.yahoo.com/d/quotes.csv?s="+i+"&f=snd1lyr")
			# print data[1],data[3]
			name = data[1]
			value = data[3].split('>')[1].split('<')[0]
			# print name,value
			self.displayItems[name] = value


# http://finance.yahoo.com/d/quotes.csv?s=AAPL&f=snd1lyr