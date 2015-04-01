from threading import *
import importlib
import sys
import Image, ImageFont, ImageDraw


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

	def drawme(self,node,(parentwidth,parentheight)):
	
		#place point
		placex,placey = 0,0
		if(node.alignment == "left"):
			if(hasattr(node,'x')):
				placex = node.x+2
			else:
				placex = 2
		elif(node.alignment=="center"):
			placex = (parentwidth-node.width)/2
		elif(node.alignment=='right'):
			placex = parentwidth-2-node.width
		
		# placey = parentheight+node['y']+2
		placey = parentheight+2

		print str(placex)+" "+str(placey)+"\n"

		if(node.type == "span"):
			# font = ImageFont.truetype("TNR.ttf", node['size'])
			font = ImageFont.truetype("TNR.ttf", 16)
			self.drawC.text((placex,placey),node.text,font=font)
		elif(node.type == "img"):
			img2 = Image.open(node.src)
			#region = img2.crop(0,0,node.width,node.height) cropping
			self.drawC.paste(img,(placex,placey))
		elif(node.type == "div"):
			for i in node.children:
				self.img.show()
				self.drawme(i,(node.width,self.lineheight))
			self.lineheight+= node.height


	def draw(self,layout,height=480,width=800):
		# Chukka's Logic 
		print "chukk "
		self.img = Image.new('L',(width, height),'white')
		self.drawC = ImageDraw.Draw(self.img)
		self.lineheight = 2

		self.drawme(layout.rootNode,(2,2))
		self.img.show()
		del self.drawC
		pass


if __name__ == '__main__':
	if(len(sys.argv)==2):
		App = ExecApp(sys.argv[1],lambda x:x)
		App.start()
	else:
		App = ExecApp('NewsFeed',lambda x:x)
		App.start()