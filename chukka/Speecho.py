# NOTE: this requires PyAudio because it uses the Microphone class
import speech_recognition as sr
r = sr.Recognizer()
# print r.energy_threshold
r.energy_threshold = 4500
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
		print r.recognize(audio) # recognize speech using Google Speech Recognition
		print "="*60
	except LookupError: # speech is unintelligible
		print("Could not understand audio")
