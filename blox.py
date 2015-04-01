import xml.etree.ElementTree as ET

class Element:
	def __init__(self,node,layout):
		self.type = node.tag
		if(self.type == 'span'):
			self.text = node.text.strip()
		elif(self.type == 'img'):
			self.src = node.get('src')
		# if(self.type in ['div','span']):
		self.children = []

		self.width = node.get("width",default = False)
		if(not self.width): self.width = '100'
		self.height = node.get("height",default = False)
		if(not self.height): self.height = '100'
		self.alignment = node.get("align",default = False) 
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
		elif(self.type == 'span'): self.text = value


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
	def __init__(self,renderImage):
		self.commands = {}
		self.layouts = {}
		self.activeLayoutID = ""
		self.scopes = {}
		self.renderImage = renderImage
		# Create json of all commands


 
	def registerCommand(self,command,callback,parellel=False):
		if(not type(command) == type("")):
			print "command not registered"
			return False

		self.commands[command] = (parellel,callback)
		return True


	def newLayout(self,layoutId,layoutFileName):
		if(not type(layoutId) == type("")):
			print "command not registered"
			return False
		layoutFile = open(layoutFileName,"r")
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
		print "\t\t\t\t",self.activeLayoutID 		
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

	def pause(self):
		# take care of max size of program and shit
		print "Moving to background"