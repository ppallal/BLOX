import speech_recognition as sr
r = sr.Recognizer()


def callback(self, audio):
    try:
        print("You said " + self.recognize(audio))
    except LookupError:
        print("Oops! Didn't catch that")
r.listen_in_background(sr.Microphone(), callback)
# help(r.listen_in_background)

import time
while True: time.sleep(0.1)