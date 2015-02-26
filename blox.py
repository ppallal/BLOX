

class Layout:
	def __init__(self,xml):
		self.xml = xml
		self.rootNode = None
		self.variablesUsed = {}
		self.scope = {}
	
	def parse():
		# build tree and initialize scope 	


class BLOX:
	def __init__(self):
		self.commands = {}
		self.layouts = {}
		self.activeLayoutID = ""
		self.scopes = {}

 
	def registerCommand(self,command,callback):
		if(not type(command) == type("")):
			print "command not registered"
			return False

		self.commands[command] = callback
		return True

	def newLayout(self,layoutId,layout):
		if(not type(layoutId) == type("")):
			print "command not registered"
			return False
	 # create layout and scope and assign to scopes
	 	newLayout = Layout(layout)
	 	self.layouts[layoutId] = newLayout 	
		return True

	def renderLayout(self):
		# build tree and show on screen. also use caching mechanism to avoid building tree again and again.
		pass 

	def refreshScreen(self):
		# Change Variable values and render screen , No tree building
		pass

	def setInterval():
		pass

	def setTimeout():
		pass

	def clearTimeout():
		pass

	def clearInterval():
		pass

