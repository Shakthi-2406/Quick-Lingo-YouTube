import streamlit as st
import pyttsx3
import time, os
from threading import Thread
from deep_translator import GoogleTranslator
from audio_download import get_audio, summarize_huggingface, transcribe, get_minimum_size

os.system('sudo apt install -y espeak')
os.system('sudo apt-get -y update')
os.system('sudo apt-get install -y alsa-utils')
os.system('sudo apt-get install -y software-properties-common')
os.system('sudo apt-get install -y ffmpeg')


st.write("<div style='display:flex; align-items: center;letter-spacing: 2px;margin-left:2px;'><h1>QuickLingoYouTube</h1></div>", unsafe_allow_html=True)
st.write("<p style='font-size:small;margin-left:5px;margin-top:-5px;margin-bottom:-5px;'>From  <a style='text-decoration:none;' href='https://www.linkedin.com/in/shakthi-s-a0b44a211/'>Shakthi</a></p>", unsafe_allow_html=True)
st.write("<div><p style='letter-spacing:2px; font-weight:light; margin-left:5px;'>Empowering the Blind, Engaging the Deaf, and Time-Saving Translations</p></div>", unsafe_allow_html=True)
langs_dict = GoogleTranslator().get_supported_languages(as_dict=True)

def talk_output(content):
    converter = pyttsx3.init()
    converter.setProperty('rate', 130)
    converter.setProperty('volume', 1)
    for sentence in content.split('\n'):
        converter.say(sentence)
    converter.runAndWait()

def type_output(content, delay = 0.001):
    placeholder = st.empty()
    intermediate = ""
    for letter in content:
        intermediate += letter
        placeholder.write(intermediate)
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
if selected_language != 'Original':
    translated_content = translate(summarized_content, selected_language)
    st.write(selected_language + ": ")
    st.write(translated_content)
    st.write(summarized_content)
    if(selected_language == 'English'):
        talk_output(translated_content)
    else:
        st.write(f"Voice over is currently not supported for {selected_language}.")
        talk_output(summarized_content)
    st.divider()
else:
    type_output(summarized_content)
    talk_output(summarized_content)

type_output("\nThank you for using", 0.3)
st.markdown("Developed by [Shakthi](https://www.linkedin.com/in/shakthi-s-a0b44a211/)")

# talkThread = Thread(target = talk_output, args=(summarized_content,))
# talkThread.start()
# talkThread.join()
# st.balloons()
# typeThread = Thread(target = type_output, args=(summarized_content,))
# typeThread.start()
# typeThread.join()
# st.download_button("Download the output file as text", data="news.webm")
# st.success('🤗')
# Token indices sequence length is longer than the specified maximum sequence length for this model (2246 > 1024). Running this sequence through the model will result in indexing errors
