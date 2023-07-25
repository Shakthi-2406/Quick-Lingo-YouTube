def change_voice(engine, language, gender='VoiceGenderFemale'):
    for voice in engine.getProperty('voices'):
        print(voice.languages)
        if language in voice.languages and gender == voice.gender:
            engine.setProperty('voice', voice.id)
            return True

    raise RuntimeError("Language '{}' for gender '{}' not found".format(language, gender))

import pyttsx3

engine = pyttsx3.init()

for voice in engine.getProperty('voices'):
    print(voice)

# change_voice(engine, "nl_BE", "VoiceGenderFemale")
engine.say("Hello World")
engine.runAndWait()