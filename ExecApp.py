from threading import *
import importlib
import sys
import Image, ImageFont, ImageDraw
import json
import pickle


class workerPool():
	"""docstring for workerPool"""
	def __init__(self, limit):
		self.limit = limit
		self.pool = []
		self.exectutionQueue = []
		for i in range(self.limit):
			self.pool.append(WorkerThread(i,self.done)) 

	def done(self,threadId):    # what is this doing ??
		if(self.exectutionQueue):
			funcset = self.exectutionQueue.pop()
			self.pool[threadId].setFunc(funcset[0],funcset[1])
			self.pool.start()

	def execFunc(self,func,funcScope=None):
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
		print "Returning from Func " + str(self.threadId) 
		self.status = False
		self.done(self.threadId)            # ??


class ExecApp():
	"""docstring for ExecApp"""
	def __init__(self, appName, sendImage):
		print appName
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
		self.status = True
		self.tempImg = None

	def install(self):
		f = open(self.appName+".json","w")
		f.write(json.dumps(self.app.commands.keys()))
		f.close()

	def dumpConfig():
		
		self.restoreFile = open(self.appName+".restore","w")
		self.restoreThreadFile = open(self.appName+"-threads.restore","w")
		self.restoremThreadFile = open(self.appName+"-mthread.restore","w")
		
		pickle.dump(self.app,self.restoreFile)
		pickle.dump(self.tPool,self.restoreThreadFile)
		pickle.dump(self.mainThread,self.restoremThreadFile)
		
		self.restoreFile.close()
		self.restoreThreadFile.close()
		self.restoremThreadFile.close()
		

		# pass


	def switchIn(self):
		"onResume()"
		self.status = True
		self.app.switchIn();
		self.sendImage(self.tempImg)

	def switchOut(self):
		"onPause"
		self.status = False
		self.app.switchOut();


	def onRestore(self):
		self.restoreFile = open(self.appName+".restore","r")
		self.restoreThreadFile = open(self.appName+"-threads.restore","r")
		self.restoremThreadFile = open(self.appName+"-mthread.restore","r")
		
		self.app = pickle.load(self.restoreFile)
		self.tPool = pickle.load(self.restoreThreadFile)
		self.mainThread = pickle.load(self.restoremThreadFile)
		
		self.mainThread.run()
		for i in self.tPool.pool:
			i.run()

		self.restoreFile.close()
		self.restoreThreadFile.close()
		self.restoremThreadFile.close()

	def commandIn(self,command):
		callBack = self.app.commands[command]
		print " inside commandin exec"
		if(callBack[0]):
			print "calling if"
			self.tPool.execFunc(callBack[1])
		else:
			print "calling else"
			callBack[1]()

	def start(self):
		self.mainThread.setFunc(self.app.start,self.app)
		self.mainThread.start()
		pass		

	def doInBackground(func):
		pass

	def renderImage(self,layout):
		image = self.draw(layout)
		self.tempImg = image
		if(self.status):
			self.sendImage(image)

	def drawme(self,node,(parentwidth,parentheight),parentx = 0,parenty = 0,SPACING_CONST = 2):
			
		placex,placey = 0,0

		if(node.type == 'text' or node.type == 'img'):

			if(node.type == 'text'):
				self.font = ImageFont.truetype("TNR.ttf", node.size)
				node.ewidth, node.eheight = self.drawC.textsize(node.text, font=self.font)

			#placex
			if(node.alignmentx == 'left'):
				placex = parentx + SPACING_CONST
			elif(node.alignmentx=='center'):
				placex = parentx + (parentwidth / 2) - (node.ewidth/2)
			elif(node.alignmentx=='right'):
				placex = parentx + parentwidth - SPACING_CONST - node.ewidth

			#placey
			if(node.alignmenty =='top'):
				placey = parenty + SPACING_CONST
			elif(node.alignmenty == 'bottom'):
				placey = parenty + parentheight - SPACING_CONST - node.eheight
			elif(node.alignmenty == 'center'):
				placey = parenty + (parentheight / 2) - (node.eheight/2)
			
			print "placex = "+str(placex)+" placey = "+str(placey)+";\n"

		if(node.type == "text"):
			self.drawC.text((placex,placey),node.text,font=self.font)
		elif(node.type == "img"):
			img2 = Image.open(node.src)
			#region = img2.crop(0,0,node.width,node.height) #cropping
			self.img.paste(img2,(placex,placey))
		elif(node.type == "div"):

			#if root node
			if(node.width == 0 and node.height == 0):
				node.width = parentwidth
				node.height = parentheight

			# splitting
			num = 0
			pushxy = 0
			for i in node.children:

				#setting width and height

				if(node.split == 0):	#horizontal split
					i.width = node.width
					i.height = (node.percentages[num]*node.height)/100;

				elif(node.split == 1):	#vertical split
					i.width = (node.percentages[num]*node.width)/100;
					i.height = node.height
				print "num = "+str(num)+";i.width="+str(i.width)+";i.height="+str(i.height)+";pushxy="+str(pushxy);

				if(num == 0):
					self.drawme(i,(node.width,node.height),parentx,parenty)
				else:
					if(node.split == 0): #horizontal split
						self.drawme(i,(node.width,node.height),parentx,parenty+pushxy)
					elif(node.split == 1):
						self.drawme(i,(node.width,node.height),parentx+pushxy,parenty)

				#pushxy
				if(node.split == 0):	#horizontal split
					pushxy = ((node.percentages[num]*parentheight)/100)+pushxy
				elif(node.split == 1):	#vertical split
					pushxy = ((node.percentages[num]*parentwidth)/100)+pushxy

				num+=1

	def draw(self,layout,height=480,width=800):
		# Chukka's Logic 
		self.img = Image.new('L',(width, height),'white')
		self.drawC = ImageDraw.Draw(self.img)
		self.lineheight = 2

		self.drawme(layout.rootNode,(width,height))
		self.img.show()
		del self.drawC
		exit()
		pass


if __name__ == '__main__':
	if(len(sys.argv)==2):
		App = ExecApp(sys.argv[1],lambda x:x)
		App.start()
	else:
		App = ExecApp('NewsFeed',lambda x:x)
		App.start()
