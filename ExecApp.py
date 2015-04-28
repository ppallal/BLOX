from threading import *
import importlib
import sys
import Image, ImageFont, ImageDraw
import json
import time
import pickle





class workerPool():
	"""docstring for workerPool"""
	def __init__(self, limit):
		self.limit = limit
		self.pool = {}
		self.freePool = set(range(self.limit))
		self.exectutionQueue = []
		self.semaphore = BoundedSemaphore(self.limit)
		self.syncLock = BoundedSemaphore(1)
		self.syncLock.acquire()
		for i in range(self.limit):
			self.pool[i] = WorkerThread(i, self.exectutionQueue, self.syncLock, self.semaphore, self.freePool)
			self.pool[i].daemon = True

	def done(self):    # what is this doing ??
		pass
		# if(self.exectutionQueue):
		# 	funcset = self.exectutionQueue.pop()
		# 	self.pool[threadId].setFunc(funcset[0],funcset[1])
		# 	self.pool.start()

	# Improvement -- Scheduler can make preemption of jjob etc to avoid deadlocks and starvations 
	def scheduler(self):
		while True:
			# print " -- syncLock Waiting"
			self.syncLock.acquire()
			# print " -- syncLock Acquired"
			self.semaphore.acquire()
			# print " -- thread semaphore Acquired"
			# print "--old --",self.exectutionQueue
			args = False
			job = self.exectutionQueue.pop()
			if( type(job) == type((1,2)) ):
				args = job[1]
				job = job[0]

			# print "--new --",self.exectutionQueue
			freeThreadId = self.freePool.pop()
			self.pool[freeThreadId].setFunc(job)
			self.pool[freeThreadId].setArgs(args)

			self.pool[freeThreadId].start()
			if(len(self.exectutionQueue) <> 0):
				try:
					self.syncLock.release()
				except ValueError:
					pass
				# self.syncLock.release()



	def doJob(self,job):
		self.exectutionQueue.append(job)
		try:
			self.syncLock.release()
		except ValueError:
			pass



	def execFunc(self,func,funcScope=None):
		for i in self.pool:
			if(i.status == False):
				i.setFunc(func,funcScope)
				i.start()
				return
		self.exectutionQueue.append((func,funcScope))

		

class WorkerThread(Thread):
	def __init__(self,threadId, exectutionQueue, syncLock, semaphore = None , freePool = None):
		Thread.__init__(self)
		self.status = False
		# self.done = done
		self.threadId = threadId
		self.semaphore = semaphore
		self.syncLock = syncLock
		self.freePool = freePool
		# self.daemon = True
		self.args = False
		self.exectutionQueue = exectutionQueue
		# self.daemon = True

	def setFunc(self,func):
		self.func = func

	def setArgs(self,args):
		self.args = args

	def doJob(self,job):
		self.exectutionQueue.append(job)
		# self.syncLock.release()
		try:
			self.syncLock.release()
		except ValueError:
			pass

	def done(self):
		if(self.freePool <> None): 
			self.freePool.add(self.threadId)
		if(self.semaphore <> None):
			self.semaphore.release()

	def run(self):
		self.status = True
		func = getattr(self,'func')
		# print "Handling in " + str(self.threadId)
		if(not self.args): 
			func()
		else:
			func(self.args)
		# print "Returning from Func " + str(self.threadId) 
		self.status = False
		Thread.__init__(self)
		self.done()            # ??

		


class ExecApp():
	"""docstring for ExecApp"""
	def __init__(self, appName, sendImage):
		print appName
		self.chui = 0

		self.appName = appName
		# sys.path.insert(0, 'apps/'+self.appName)
		sys.path.insert(0, 'apps/'+self.appName+"/")
		sys.path.insert(0, '/'+self.appName)
		app = __import__(self.appName.lower())
		self.threadLimit = 5
		self.tPool = workerPool(self.threadLimit)
		self.mainThread = WorkerThread("MainThread",self.tPool.exectutionQueue,self.tPool.syncLock)
		self.mainThread.daemon = True
		self.schedulerThread = WorkerThread("schedulerThread",self.tPool.exectutionQueue,self.tPool.syncLock)
		self.schedulerThread.daemon = True
		self.sendImage = sendImage
		# import from the app
		# self.app = app
		# print app.modules[self.appName]
		self.app = getattr(app,self.appName)()
		self.app.setRenderImage(self.renderImage)
		self.app.setDoJob(self.mainThread.doJob)
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
		print "switchIn",self.appName
		if(self.status):
			return
		self.status = True
		self.app.switchIn();
		self.sendImage(self.tempImg)

	def switchOut(self):
		"onPause"
		print "switchOut",self.appName
		if(not self.status):
			return
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
		callBack = self.app.commands.get(command.lower(),False)
		args = False
		if(not callBack):
			for i in self.app.commands:
				if(command.lower().startswith(i)):
					cmd = i
					break

			# return # Command Not UnderStood
			else :
				return 
			
			args = command.split(cmd)[1].strip()
			callBack = self.app.commands[cmd.lower()]


		print " inside commandin exec"
		if(callBack[0]):
			print "calling if"
			# self.tPool.execFunc(callBack[1])
			self.tPool.doJob((callBack[1],args))
		else:
			print "calling else"
			callBack[1](args)

	def start(self):
		self.mainThread.setFunc(self.app.start)
		self.mainThread.start()
		self.schedulerThread.setFunc(self.tPool.scheduler)
		self.schedulerThread.start()
		pass		

	def doInBackground(func):
		pass

	def renderImage(self,layout):
		self.draw(layout)
		# self.tempImg = image
		self.tempImg = self.getStringCharArray(list(self.img.getdata()))
		if(self.status):
			self.sendImage(self.tempImg)
			# self.sendImage(image)

	def getStringCharArray(self,monochrome,width=128,height=64): #monochrome is a list of 255 and 0s #GLCD 8 bits
		finalStringHexArray = list()
		v = 0;
		for r in range(0,height/8):  # 8 rows
			for c in range(0,width):
				tempStringHex = ""
				for for8 in range(0,8):
					v = monochrome[(r*8*width)+c+(for8*width)]
					if(v == 255):
						tempStringHex += '0'
					else: # v is 0
						tempStringHex += '1'

				finalStringHexArray.append(int(tempStringHex[::-1],2))
		# print finalStringHexArray
		return finalStringHexArray

	def getSplitTexts(self,text,txtsize,(parentwidth,parentheight),SPACING_CONST=2):
		parentwidth = parentwidth - SPACING_CONST
		returnText = []
		lines = 1
		txtwidth = txtsize/2
		temptext = text
		if(len(text)*txtwidth<=parentwidth):
			return list([text])
		while((len(temptext)*txtwidth)>parentwidth):
			returnText.append(temptext[:int(parentwidth/txtwidth)])
			# print temptext
			temptext = temptext[int(parentwidth/txtwidth):]
			if(parentheight<(lines*txtsize)):
				break;
			lines += 1
		print returnText
		return returnText

	def getTextSize(self,text,txtsize):
		height = txtsize
		width = (txtsize/2)*len(text)
		return width,height



	def drawme(self,node,(parentwidth,parentheight),parentx = 0,parenty = 0,SPACING_CONST = 2):
			
		#border
		if hasattr(node, 'border'):
			borders = map(lambda x:int(x), node.border.split(',')) #top, right, bottom, left
			print "borders ",borders
			print "parentx:",parentx," parenty:",parenty," node.width:",node.width," node.height:",node.height," borders:",borders
			for i in range(0,4):
				if borders[i]>0:
					if i==0:
						self.drawC.line((parentx,parenty,parentx+node.width,parenty),"black",borders[i])
					elif i==1:
						self.drawC.line((parentx+node.width,parenty,parentx+node.width,parenty+node.height),"black",borders[i])
					elif i==2:
						self.drawC.line((parentx,parenty+node.height,parentx+node.width,parenty+node.height),"black",borders[i])
					elif i==3:
						self.drawC.line((parentx,parenty,parentx,parenty+node.height),"black",borders[i])

		#placing text and images
		placex,placey = 0,0
		if(node.type == 'text' or node.type == 'img'):

			if(node.type == 'text'):
				self.font = ImageFont.truetype("small5x3.ttf", node.size)
				# node.ewidth, node.eheight = self.drawC.textsize(node.text, font=self.font)
				node.ewidth, node.eheight = self.getTextSize(node.text, node.size)

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
			
			# print "placex = "+str(placex)+" placey = "+str(placey)+";\n"

		if(node.type == "text"):
			if hasattr(node,'wraparound'):
				ply = placey
				for i in self.getSplitTexts(node.text,node.size,(parentwidth,parentheight),SPACING_CONST):
					self.drawC.text((placex,ply),i,font=self.font)
					ply+=8
			else:	
				self.drawC.text((placex,placey),node.text,font=self.font)
		elif(node.type == "img"):
			img2 = Image.open("apps/"+self.appName+"/"+node.src)
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
					i.height = (node.percentages[num]*node.height)/100

				elif(node.split == 1):	#vertical split
					i.width = (node.percentages[num]*node.width)/100
					i.height = node.height
				# print "num = "+str(num)+";i.width="+str(i.width)+";i.height="+str(i.height)+";pushxy="+str(pushxy);

				if(num == 0):
					self.drawme(i,(node.width,node.height),parentx,parenty)
				else:
					if(node.split == 0): #horizontal split
						self.drawme(i,(node.width,node.height),parentx,parenty+pushxy)
					elif(node.split == 1): #vertical split
						self.drawme(i,(node.width,node.height),parentx+pushxy,parenty)

				#pushxy
				if(node.split == 0):	#horizontal split
					pushxy = ((node.percentages[num]*parentheight)/100)+pushxy
				elif(node.split == 1):	#vertical split
					pushxy = ((node.percentages[num]*parentwidth)/100)+pushxy

				num+=1



	def draw(self,layout,height=64,width=128):
		# Chukka's Logic 
		self.img = Image.new('1',(width, height),'white')
		# self.img = Image.open('photo.pbm')
		self.drawC = ImageDraw.Draw(self.img)
		self.lineheight = 0
		# print layout.rootNode.__dict__
		layout.printLayout()
		self.drawme(layout.rootNode,(width,height))
		self.img.show()
		self.img.save("news.jpg","JPEG")

		# self.sendThisString = self.getStringCharArray(list(self.img.getdata()),width,height); #for GLCD
		
		#self.img.save("crap.ppm", "PPM");
		# del self.drawC
		if(self.chui==4):
			# exit()
			pass
		self.chui+=1
		
		pass

	# def draw(self,layout,height=480,width=800):
	# 	# Chukka's Logic 
	# 	self.img = Image.new('L',(width, height),'white')
	# 	self.drawC = ImageDraw.Draw(self.img)
	# 	self.lineheight = 2

	# 	self.drawme(layout.rootNode,(width,height))
	# 	print "Showing Image"
	# 	time.sleep(20)
	# 	del self.drawC
	# 	# exit()
	# 	pass


if __name__ == '__main__':
	if(len(sys.argv)==2):
		App = ExecApp(sys.argv[1],lambda x:x)
		App.mainThread.daemon = False
		App.start()
		time.sleep(100)
	else:
		App = ExecApp('twitter',lambda x:x)
		App.mainThread.daemon = False
		App.start()


# File Handling Capabalities Like Memory and stuff.