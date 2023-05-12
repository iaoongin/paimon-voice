import pyttsx3

engine = pyttsx3.init()
rate = engine.getProperty('rate')
engine.setProperty('rate', rate+50)

voices = engine.getProperty('voices')
for voice in voices:
    
    print(voice.name)

    if voice.name == 'Microsoft Zira Desktop - English (United States)':
        engine.setProperty('voice', voice.id)


text = "bu cuo ma"
engine.say(text)

engine.runAndWait()