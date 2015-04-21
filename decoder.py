
import json
import sys
import threading
import time
from ExecApp import ExecApp
sys.path.insert(1,'/home/Desktop/BLOX/apps/')
app_commands = []    # pointer to apps start function , or file name or pointer to class ????
#blox_commands = ["install newsfeed_links in 1","install newsfeed in 2","stop app_name"]
blox_commands = ["install","install","stop","start"]
apps = {}     # app_name = key , screen_no = value , screen_no = 0 for stopped apps 
screen_ip = {'1':'192.166.168.199','2':'192.166.168.200'}   # screen no = key , ip : value
priority_app = {}
threadi = {}   # key : app_name , value : respective thread class object
importi = {}   #key : app_name , value : import object
instancei = {}  #key : app_name , value : instance of app class
Appi = {}

class myThread (threading.Thread):
    def __init__(self, threadID, name,app_instance,ip):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.app_instance = app_instance
	#self.func = func
        #self.func1 = func1
        self.ip = ip
        self.cmd = ""
    def run(self):
        print "Starting " + self.name
	(self.app_instance).start(self.ip)
        print "Exiting " + self.name
    def command_in(self,cmd):
        self.cmd = cmd
	(self.app_instance).input_command(self.cmd)
        #self.func1(self.cmd)
        	






def command_router(command):  #if command = app specefic , redirect it
	if(command.split(' ',1)[0] == "blocks"):
		app,cmd = categorize(command.split(' ',1)[1])
		print app + "\t" + str(cmd)
		if(app == "invalid"):
			pass#print "invalid"#give error message
		elif(app == "blox"): #call the blox command handler or input function of blox app(spcl app)
			command_handler(cmd)
		else:
			#app.command_in(cmd) #app should implement input_command method.
			Appi[app].commandIn(cmd)
			#priority_app[app]+=1
			last_app = app
			
	else:
		pass#print "do nothing"#do nothing
	
def install_app(app_name,screen_no,dont_download = 0):  # the app will register itself with decoder, will get callback when command for that app comes
	if(not dont_download):
		pass # temporary
		#download the app's code and keep it in apps folder
		apps[app_name] = screen_no
		with open('data.txt','w') as outfile:
			json.dump(apps,outfile)
	Appi[app_name] = ExecApp(app_name,lambda x:x)
	Appi[app_name].start()
	time.sleep(5)
	print "printing registered cmds"
	print Appi[app_name].app.commands
	print "decoder" + app_name
	print screen_no
	 
def delete_app():
	pass# uninstall app,delete app's code from the app folder

def start_app(app_name,screen_no):	# start the stopped app,can take time as parameter to get started automatically after sometime
	for i in apps:			# check if some app is already running in that scree, if yes stop it.	
		if (apps[i] == screen_no):
			Appi[i].stop()
			break
	apps[app_name] = screen_no
	Appi[app_name].start()
		
	


def stop_app(app_name):   # stop temporarily but dont uninstall, can take time as parameter to get stopped automatically after sometime
	Appi[app_name].stop()
	apps[app_name] = 0
	del Appi[app_name]

def categorize(cmd):#return app_name if app specific cmmand,block if blox command , null if invalid
	app_name = cmd.rsplit(' ',1)[1]
	print cmd
	cmd1 = cmd.rsplit(' ',1)[0]
	if(app_name in apps):
		if (cmd1 in Appi[app_name].app.commands):
			print "command found"
			return (app_name,cmd1)
	else:
		keyword = cmd.split(' ')[0]
		if(keyword in blox_commands):
			return ("blox",cmd)
		else:
			if(cmd in Appi[last_app].app.commands):
				return (last_app,cmd)
			for i in sorted(priority_app,key=priority_app.get,reverse = True):
				if(i != last_app):
					if(cmd in Appi[i].app.commands):
						return (i,cmd)
			return ("invalid",0)
			

	

#======================== BLOX command handler ==============================================================#

def command_handler(cmd):
	cmd_list = cmd.split(' ')
	if("install" in cmd_list):
		install_app(cmd_list[1],cmd_list[3])
	if("start" in cmd_list):
		start_app(cmd_list[1],cmd_list[3])
	if("stop" in cmd_list):
		stop_app(cmd_list[1])
	

	

def start_decoder():
	#install_app("newsfeed",1)
	#install_app("newsfeed_links",2)
	#i = input("enter command")
	#command_router(i)
	if bool(apps):
		for app,screen in apps.iteritems():
			install_app(app,screen,1)
	
	last_app = ""
	# command_router("blocks install newsfeed_links in 1")
	command_router("blocks install NewsFeed in 2")
	time.sleep(10)
	# command_router("blocks next feed newsfeed_links")
	apps['3']="some_app"
	#threadi["newsfeed_links"].command_in("some cmd")


'''======to dos======
fix blox_commands
last app_name and priority
error handling everywhere
put apps in apps folder, fix the import problem
'''

#pm = __import__("praf_newsfeed")
#newsfeed = getattr(pm,"NewsFeed")
#nf = newsfeed()
#nf.start()

command_router("blocks install NewsFeed in 2")
print "SENDING NEXT COMMAND"
command_router("blocks next NewsFeed")
print "SENDING NEXT INSTALL COMMAND "
command_router("blocks install NewsFeed_links in 1")
print "came back"

# command_router("blocks start NewsFeed")
# start_decoder()
	
# Essential -- Niraj, During installation you need to take the source code of the person and replace his "import Blox" to give your copy of BLOX 
# i.e. Either copy Blox.py on to his folder or modify his source code.