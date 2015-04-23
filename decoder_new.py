import json
import sys
import threading
import time
import fuzzy
from ExecApp import ExecApp
from socket_server import SocketPicture
import traceback


soundex = fuzzy.Soundex(4)
sys.path.insert(1,'/home/Desktop/BLOX/apps/')
#blox_commands = ["install newsfeed_links in 1","install newsfeed in 2","stop app_name"]
blox_commands = ["install","stop","start"]
apps = {"NewsFeed":0,"newsfeed":1}     # app_name = key , screen_no = value , screen_no = 0 for stopped apps 
screen_ip = {'0':'','1':'192.166.168.199','2':'192.166.168.200'}   # screen no = key , ip : value
priority_app = {}
Appi = {}
command_list = ["next newsfeed","next NewsFeed","next"]
last_app = "some app"
fuzzy_app = {}
app_fuzzy_command = {}

def command_router(command):  #if command = app specefic , redirect it
    print command

    if(command.split(' ',1)[0] == "blocks"):
        try:
            command_wo_blocks = command.split(' ',1)[1]
        except:
            print "Yeah i know i am blox, what shall i do ??"
        else:
            app,cmd = categorize(command_wo_blocks)
            print app + "\t" + str(cmd)
            if(app == "invalid"):
                pass#print "invalid"#give error message
            elif(app == "blox"): #call the blox command handler or input function of blox app(spcl app)
                print "calling blox command handler ",cmd
                command_handler(cmd)
            else:
                print "sending to app cmd handler ",cmd
                print app,cmd
            	Appi[app].commandIn(cmd.lower())
                for i in apps:          # check if some app is already running in that scree, if yes stop it.   
                    if (apps[i] == apps[app]):
                        Appi[i].switchOut()
                        # break
                            
                # Appi[i].switchOut()

                Appi[app].switchIn()
                last_app = app
    else:
        pass#print "do nothing"#do nothing

def categorize(cmd):#return app_name if app specific cmmand,block if blox command , null if invalid
    keyword = cmd.split(' ',1)[0]             # assuming block command
    if(keyword in blox_commands):
        return ("blox",cmd)
    else: 
        try:                                        # assuming app command and has app name . blox "command" app_name
            app_name = cmd.rsplit(' ',1)[1]
            app_name_soundex = soundex(app_name)
        except:
            pass
        else:
            command = cmd.rsplit(' ',1)[0]
            command_soundex = soundex(command)
            if(app_name_soundex in fuzzy_app):
                app_name_actual = fuzzy_app[app_name_soundex]
                if(command_soundex in app_fuzzy_command[app_name_actual]):   # in that particular app
                    # print command_soundex,app_name_actual[command_soundex]
                    command_actual = app_fuzzy_command[app_name_actual][command_soundex]
                    return(app_name_actual,command_actual)
    cmd_soundex = soundex(cmd)
    if(cmd_soundex in app_fuzzy_command[last_app]): # command list of last app
        command_actual = app_fuzzy_command[last_app[cmd_soundex]]
        return (last_app,command_actual)
    for i in sorted(priority_app,key=priority_app.get,reverse = True):
        if(i != last_app):
            if(cmd_soundex in app_fuzzy_command[i]):
                command_actual = app_fuzzy_command[i[cmd_soundex]]
                return (i,command_actual)
    print "returning invalid"
    return ("invalid",0)

	
def install_app(app_name,screen_no,dont_download = 0):  # the app will register itself with decoder, will get callback when command for that app comes
    sys.path.insert(1,"apps/"+app_name.lower()+"/")
    if(not dont_download):
        pass # temporary
		#download the app's code and keep it in apps folder
        apps[app_name] = screen_no
        with open('data.txt','w') as outfile:
            json.dump(apps,outfile)
    Appi[app_name] = ExecApp(app_name,server.changePicture)
    print "Installing - ",app_name
    start_app(app_name,screen_no)
'''	 
def delete_app():
	pass# uninstall app,delete app's code from the app folder
'''
def start_app(app_name,screen_no):	# start the stopped app,can take time as parameter to get started automatically after sometime
    for i in apps:			# check if some app is already running in that scree, if yes stop it.	
        if (apps[i] == screen_no):
            Appi[i].switchOut()
            break
    apps[app_name] = screen_no
    appnameCopy = app_name[0:]
    appn = list(app_name)
    fuzzy_app[soundex(appnameCopy)] = appnameCopy
    fname = "apps/"+"".join(appn)+"/"+"".join(appn)+'.txt'
    print fuzzy_app
    with open(fname) as f:
        command_list = f.readlines()
        print(type(command_list))
    app_fuzzy_command[app_name]= {}
    for command in command_list:
        print command,app_fuzzy_command
        # app_fuzzy_command[app_name[soundex(command)]] = command
        app_fuzzy_command[app_name][soundex(command)] = command
    Appi[app_name].start()
		
	


def stop_app(app_name):   # stop temporarily but dont uninstall, can take time as parameter to get stopped automatically after sometime
    Appi[app_name].stop()
    apps[app_name] = 0
    del Appi[app_name]
    del fuzzy_app[soundex(app_name)]
    del app_fuzzy_command[app_name]

      
	

#======================== BLOX command handlers ==============================================================#

def command_handler(cmd):
    keyword = cmd.split(' ',1)[0]
    try:
        tail = cmd.split(' ',1)[1]
    except:
        print "seems you have entered an incomplete command"
    else:             
        if(keyword == "install"):
            install_handler(tail)
        if(keyword == "start"):
            start_handler(tail)
        if(keyword == "stop"):
            stop_handler(tail)


def install_handler(cmd):
    screen_no = '0'
    app_name = cmd.split(' ',1)[0]
    try:    
        screen_no = cmd.rsplit(' ',1)[1]              # last word of the command
    except:
        print "screen no not provided, selecting randomly"
        for i in screen_ip:
            if(screen_ip[i] == '0'):
                screen_no = i
                break
    print screen_no
    if screen_no not in screen_ip:
        print "invalid screen no provided"
    else:
        if(screen_no != '0'):
            print "calling inastaal"
            install_app(app_name,screen_no,"dont download")
        else:
            print "No screens available, please provide screen no."

def start_handler(cmd):
    start_app(app_name, screen_no)

def stop_handler(cmd):
    stop_app(app_name)
	

	

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

'''
======to dos======
fix blox_commands
last app_name and priority
error handling everywhere
put apps in apps folder, fix the import problem
'''

#pm = __import__("praf_newsfeed")
#newsfeed = getattr(pm,"NewsFeed")
#nf = newsfeed()
#nf.start()







# command_router("blocks install NewsFeed in 2")
# print "SENDING NEXT COMMAND"
# command_router("blocks next NewsFeed")
# print "SENDING NEXT INSTALL COMMAND "
# command_router("blocks install NewsFeed_links in 1")
# print "came back"

# # command tests cases .
# command_router("blocks install NewsFeed in 2")
# command_router("blocks install NewsFeed")
# command_router("blocks install NewsFeed 2")
# command_router("blocks install in 2")
# command_router("blocks install 2")
# command_router("blocks NewsFeed in 2")
# command_router("blocks NewsFeed 2")
# command_router("blocks in 2")
# command_router("blocks 2")
# command_router("blocks next NewsFeed")
# command_router("blocks next")
# command_router("blocks NewsFeed")
# command_router("blocks noxt NewsFeed")
# command_router("blocks text NewsFeed")
# command_router("blocks next NewsFead")
# command_router("blocks next newsfeed")

# command_router("blocks start NewsFeed")
# start_decoder()

#block specific command :
    #blocks "keyword" app_name (some connector) screen no
    #screen no = optional (if not provided randomly chooses a non-working screen)

#app specific
    #blocks "command" app_name
if __name__ == '__main__':
    # NOTE: this requires PyAudio because it uses the Microphone class
    import speech_recognition as sr
    r = sr.Recognizer()
    # print r.energy_threshold
    r.energy_threshold = 4500
    server = SocketPicture()
    server.daemon = True
    server.start()
    while(1):
        # print "start"
        with sr.Microphone() as source: # use the default microphone as the audio source
            # print "b4aud"
            # audio = r.listen(source,timeout = 5) # listen for the first phrase and extract it into audio data
            audio = r.listen(source) # listen for the first phrase and extract it into audio data
            # print "afteraud"
        # print "Audio done"
        # r.recognize(audio)
        # print 'recon'
        try:
            print "="*60
            s = r.recognize(audio) # recognize speech using Google Speech Recognition
            print s 
            command_router(s)
            print "="*60
        except LookupError: # speech is unintelligible
            traceback.print_exc(file=sys.stdout)
            # print("Could not understand audio")
