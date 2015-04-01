from threading import *
import importlib
import sys

class workerPool():
	"""docstring for workerPool"""
	def __init__(self, limit):
		self.limit = limit
		self.pool = []
		self.exectutionQueue = []
		for i in range(self.limit):
			self.pool.append(WorkerThread(self.done,i))

	def done(threadId):
		if(self.exectutionQueue):
			funcset = self.exectutionQueue.pop()
			self.pool[threadId].setFunc(funcset[0],funcset[1])
			self.pool.start()

	def execFunc(func,funcScope=None):
		for i in self.pool:
			if(i.status == False):
				i.setFunc(func,funcScope)
				i.start()
				return
		self.exectutionQueue.append((func,funcScope))



		

class WorkerThread(Thread):
	def __init__(self,threadId,done):
		Thread.__init__(self)
		self.status = False
		self.done = done
		self.threadId = threadId

	def setFunc(self,func,app):
		self.funcScope = app
		self.func = func

	def run(self):
		self.status = True
		func = getattr(self,'func')
		func()
		self.status = False
		self.done(self.threadId)


class ExecApp():
	"""docstring for ExecApp"""
	def __init__(self, appName, sendImage):
		self.appName = appName
		sys.path.insert(0, '/'+self.appName)
		app = __import__(self.appName.lower())
		self.threadLimit = 5
		self.mainThread = WorkerThread("MainThread",lambda x:True)
		self.sendImage = sendImage
		self.tPool = workerPool(self.threadLimit)
		# import from the app
		# self.app = app
		# print app.modules[self.appName]
		self.app = getattr(app,self.appName)(self.renderImage)

	def commandIn(self,command):
		callBack = self.app.commands[command]
		if(callBack[0]):
			self.tPool.execFunc(callBack)
		else:
			callBack[1]()

	def start(self):
		self.mainThread.setFunc(self.app.start,self.app)
		self.mainThread.start()
		pass		

	def doInBackground(func):
		pass

	def renderImage(self,layout):
		image = self.draw(layout)
		self.sendImage(image)
		pass

	def draw(self,layout,height=480,width=800):
		# Chukka's Logic 
		print "chukk "
		pass


if __name__ == '__main__':
	if(len(sys.argv)==2):
		App = ExecApp(sys.argv[1],lambda x:x)
		App.start()
	else:
		App = ExecApp('NewsFeed',lambda x:x)
		App.start()