import streamlit as st
import pyttsx3
import time, os
from threading import Thread
from deep_translator import GoogleTranslator
from audio_download import get_audio, summarize_huggingface, transcribe, get_minimum_size, generate_timestamp
import gtts, base64
from io import BytesIO
from functools import lru_cache
from make_pdf import make_pdf


st.set_page_config(
    page_title="QuickLingoYouTube",
    page_icon="🚀"
)

st.write("<div style='display:flex; align-items: center;letter-spacing: 2px;margin-left:2px;'><h1>QuickLingoYouTube</h1></div>", unsafe_allow_html=True)
st.write("<p style='font-size:small;margin-left:5px;margin-top:-5px;margin-bottom:-5px;'>From  <a style='text-decoration:none;' href='https://www.linkedin.com/in/shakthi-s-a0b44a211/'>Shakthi</a></p>", unsafe_allow_html=True)
st.write("<div><p style='letter-spacing:2px; font-weight:light; margin-left:5px;'>Empowering the Blind, Engaging the Deaf, and Time-Saving Translations</p></div>", unsafe_allow_html=True)
langs_dict = GoogleTranslator().get_supported_languages(as_dict=True)

talking_languages = gtts.lang.tts_langs()

def get_tts_lang_code(language):
    for code in talking_languages:
        if language in talking_languages[code]:
            return code
    return 'Not Supported'

@lru_cache(maxsize=16)
def google_tts_talk(content, language):
    if get_tts_lang_code(language) == 'Not supported':
        return f"<p>Speech is not yet implemented for {language}</p>"
    
    sound_file = BytesIO()
    tts = gtts.gTTS(content, lang='en', slow=False)
    tts.write_to_fp(sound_file)
    # st.audio(sound_file)
    audio_base64 = base64.b64encode(sound_file.getvalue()).decode()
    return f'<audio autoplay="true" src="data:audio/wav;base64,{audio_base64}">'


def streamlit_talk(audio_file_name):
    audio_tag = f'<audio autoplay="true" src="{audio_file_name}">'
    return audio_tag
    st.markdown(audio_tag, unsafe_allow_html=True)
    st.write("Audio successful")

def talk_output(content, streamlit=False):
    converter = pyttsx3.init()
    converter.setProperty('rate', 150)
    converter.setProperty('volume', 1)
    if not streamlit:
        for sentence in content.split('\n'):
            converter.say(sentence)
    else:
        audio_file_name = "pyttsx3" + generate_timestamp() + '.mp3'
        converter.save_to_file(content, audio_file_name)
    converter.runAndWait()
    if streamlit:
        return streamlit_talk(audio_file_name)

def type_output(content, delay = 0.0002):
    placeholder = st.empty()
    intermediate = ""
    for letter in content:
        intermediate += letter
        placeholder.write(intermediate+'|')
        time.sleep(delay)

def translate(content, targetLang):
    show_progress(f"Translating in {targetLang} for you....")
    if len(content) > 5000:
        st.warning("Text size exceeds 5000 characters. Truncating to meet the limit.")
        content = content[:5000]
    targetLang = targetLang.lower()
    translated_text = GoogleTranslator(source='auto', target=targetLang).translate(content)
    return translated_text

def show_progress(request, length = 502161): 
    # talk_output(request) 
    my_bar = st.progress(0, text=request)
    for percent_complete in range(100):
        time.sleep(0.01)
        my_bar.progress(percent_complete + 1, text=request)

with st.form("my_form"):
    url = st.text_input(label="Enter the youtube video link", help="supported languages: English, Spanish, French, German, Italian, Portuguese, Dutch, Hindi, Japanese")
    st.write("Choose preferences")
    toSummarize = st.checkbox("Summarize the content to the desired length")
    summarization_length = st.slider("Summarization Length: ", min_value=150, max_value=500, value=200)
    selected_language = st.selectbox("Choose the language you want to translate to", ["Original"] + [label.capitalize() for label in langs_dict])
    submitted = st.form_submit_button("Transcribe")

while not submitted:
    pass

st.toast("Process initiated")
minimum_size_file = get_minimum_size(url)
minimum_size = minimum_size_file.get_filesize()

show_progress("Preparing for Extracting content", minimum_size)
filename, contentname = get_audio(minimum_size_file)

show_progress("Preparing for Transcription", minimum_size)
content = transcribe(filename)
os.remove(filename)

summarized_content = content
if toSummarize:
    show_progress("Shortening content")
    summarized_content = summarize_huggingface(content, summarization_length)
st.divider()

st.subheader(contentname + '\n')
pdf_text = ""

if selected_language != 'Original':
    translated_content = translate(summarized_content, selected_language)
    translated_content.replace('. ', '\n')
    st.write(selected_language + ": ")
    type_output(translated_content)
    # pdf_text += f"{selected_language}\n {translated_content}\n\n"
    st.divider()
    st.markdown(google_tts_talk(translated_content, selected_language), unsafe_allow_html=True)

summarized_content.replace('. ', '\n')
type_output(summarized_content)
pdf_text += f"{summarized_content}"

pdf = make_pdf(title = contentname, url = url, text = pdf_text)
download = st.download_button(
    label="Download for reference",
    data=pdf.output(dest='S').encode('latin-1'),
    file_name=f"{contentname}.pdf",
    mime="application/pdf",
)

show_progress("Voice over initialization", minimum_size)

st.markdown(google_tts_talk(summarized_content, "English"), unsafe_allow_html=True)


type_output("\nThank you for using", 0.3)
st.markdown("Developed by [Shakthi](https://www.linkedin.com/in/shakthi-s-a0b44a211/)", unsafe_allow_html=True)









# print(audio_tag)
# st.markdown(audio_tag, unsafe_allow_html=True)

# talkThread = Thread(target = talk_output, args=(summarized_content,))
# talkThread.start()
# talkThread.join()
# st.balloons()
# typeThread = Thread(target = type_output, args=(summarized_content,))
# typeThread.start()
# typeThread.join()
# st.download_button("Download the output file as text", data="news.webm")
# Token indices sequence length is longer than the specified maximum sequence length for this model (2246 > 1024). Running this sequence through the model will result in indexing errors
