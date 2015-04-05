# NOTE: this requires PyAudio because it uses the Microphone class
import speech_recognition as sr
r = sr.Recognizer()
while(1):
	print "start"
	with sr.Microphone() as source: # use the default microphone as the audio source
		print "b4aud"
		audio = r.listen(source) # listen for the first phrase and extract it into audio data
		print "afteraud"
	print "Audio done"
	r.recognize(audio)
	print 'recon'
	try:
		print("You said " + r.recognize(audio)) # recognize speech using Google Speech Recognition
	except LookupError: # speech is unintelligible
		print("Could not understand audio")
