import streamlit as st
from QuickLingoYoutube import *
import gtts
talking_languages = gtts.lang.tts_langs()

def get_tts_lang_code(language):
    for code in talking_languages:
        if language in talking_languages[code]:
            return code
    return 'Not Supported'

@__cached__
def google_tts_talk(content, language):
    if get_tts_lang_code(language) == 'Not supported':
        return f"<p>Speech is not yet implemented for {language}</p>"
    
    sound_file = BytesIO()
    tts = gtts.gTTS(content, lang='en', slow=False)
    tts.write_to_fp(sound_file)
    st.audio(sound_file)
    # audio_base64 = base64.b64encode(sound_file).decode("utf-8")
    audio_base64 = base64.b64encode(sound_file.getvalue())
    return f'<audio autoplay="true" src="data:audio/wav;base64,{audio_base64}">'
st.header("sggggggggggg")
st.markdown(google_tts_talk("Hi i am america", 'English'), unsafe_allow_html = True)