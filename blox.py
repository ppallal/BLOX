#parentx,parenty,parentwidth,parentheight

#FOR ALL
#node.width
#node.height

#FOR BOTH
#node.alignmentx
#node.alignmenty

#TEXT
#node.size
#node.text
#node.ewidth #element width and height
#node.eheight

#IMAGE
#node.src
#node.ewidth #element width and height
#node.eheight

#DIV
#children = []
#split #0 - horizontal 1 - vertical
#node.percentages #(children's percentages) #(50,50) #(30,30,40)

import xml.etree.ElementTree as ET

class Element:
	def __init__(self,node,layout):
		self.type = node.tag
		if(self.type =='text' or self.type == 'img'):
			self.alignmentx = node.get('alignmentx',default='center')
			self.alignmenty = node.get('alignmenty',default='center')
		if(self.type == 'text'):
			self.text = node.text.strip()
			self.ewidth = 0
			self.eheight = 0
			self.size = int(node.get('size',default=12))
		elif(self.type == 'img'):
			self.src = node.get('src')
			self.ewidth = int(node.get('ewidth'))
			self.eheight = int(node.get('eheight'))
		elif(self.type == 'div'):
			self.children = []
			if(node.get('split') == "vertical"):
				self.split = 1
			elif(node.get('split') == "horizontal"):
				self.split = 0
			self.percentages= [int(i) for i in node.get('perc').strip().split(',')]
			print self.percentages
		self.width = 0;
		self.height = 0;
		# self.width = int(node.get("width",default = False))
		# if(not self.width): self.width = 100
		# self.height = int(node.get("height",default = False))
		# if(not self.height): self.height = 100
		#self.alignment = node.get("align",default = False) 
		variables = node.get("var",default = False)
		if(variables <> False):
			variables = variables.split()
			if(type(variables) == type("")):
				variables = [variables]
			variables = filter(lambda x:x,map(lambda x:x.strip(),variables))
			for i in variables:
				if(not layout.scope.get(i,False)):
					layout.scope[i]=[self]
				else: 
					layout.scope[i].append(self)
			

	def addClild(self,child):
		self.children.append(child)

	def setValue(self,value):	
		if(self.type == 'img'): self.src = value
		elif(self.type == 'text'): self.text = value


class Layout:
	def __init__(self,xml):
		self.xml = xml
		self.rootNode = None
		self.variablesUsed = {}
		self.scope = {}
		self.parse()
	
	def parse(self):
		rootNode = ET.fromstring(self.xml)
		self.rootNode = Element(rootNode,self)
		self.parseNode(rootNode,self.rootNode)
		# build tree and initialize scope

	def parseNode(self,ETnode,Node):
		for i in ETnode.getchildren():
			# need to make sure that if text node doesn't have children.
			childNode = Element(i,self)
			Node.addClild(childNode)
			self.parseNode(i,childNode)

	def changeVariable(self,varName,value,varType):
		nodes = self.scope.get(varName,[])
		for i in nodes:
			if(i.type == varType):
				i.setValue(value)

	




	
# Same app running as different screen


class BLOX:
	def __init__(self):
		self.commands = {}
		self.layouts = {}
		self.activeLayoutID = ""
		self.scopes = {}
		# self.renderImage = renderImage
		# self.doJob = doJob
		# Create json of all commands

	def setRenderImage(self,renderImage):
		self.renderImage = renderImage

	def setDoJob(self,doJob):
		self.doJob = doJob

	def switchIn(self):
		pass

	def switchOut(self):
		pass

	def onRestore(self):
		pass

	# def doJob(self):
		
 
	def registerCommand(self,command,callback,parellel=False):
		if(not type(command) == type("")):
			print "command not registered"
			return False
		self.commands[command] = (parellel,callback)
		print command + "command registered"
		#print self.commands
		return True


	def newLayout(self,layoutId,layoutFileName):
		if(not type(layoutId) == type("")):
			print "command not registered"
			return False
		print __name__
		layoutFile = open("apps/"+self.__class__.__name__.lower()+"/"+layoutFileName,"r")
		layoutXml = layoutFile.read()
	 # create layout and scope and assign to scopes
	 	newLayout = Layout(layoutXml)
	 	self.layouts[layoutId] = newLayout 	
		return True

	def changeVariable(self,varName,value,varType,layoutId = False):
		if(not layoutId):
			for i in self.layouts:
				self.layouts[i].changeVariable(varName,value,varType)
		else:
			self.layouts[layoutId].changeVariable(varName,value,varType)


	def renderLayout(self,layoutId = False):
		if(not layoutId):
			layoutId = self.activeLayoutID
		# build tree and show on screen. also use caching mechanism to avoid building tree again and again.

		self.activeLayoutID = layoutId
		self.refreshScreen()

	def refreshScreen(self):
		# Change Variable values and render screen , No tree building
		self.renderImage(self.layouts[self.activeLayoutID])
		
		# self.sendImage()
		print  '-'*70
		print "\t\tThe screen is now being displayed"
		print "\t\t\t\t", self.activeLayoutID, self.__class__.__name__		
		print  '-'*70

	def setInterval():
		pass

	def setTimeout():
		pass

	def clearTimeout():
		pass

	def clearInterval():
		pass

	def start(self):
		print self.__class__,"Starting ..."
		self.registerCommand("show",lambda : True,parellel=True)


	def pause(self):
		# take care of max size of program and shit
		print "Moving to background"
