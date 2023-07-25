import streamlit as st
import pyttsx3
import time, os
from threading import Thread
from deep_translator import GoogleTranslator
from audio_download import get_audio, summarize_huggingface, transcribe, get_minimum_size

st.title("Be my time saver")
langs_dict = GoogleTranslator().get_supported_languages(as_dict=True)

def talk_output(content):
    converter = pyttsx3.init()
    converter.setProperty('rate', 200)
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
    targetLang = targetLang.lower()
    translated_text = GoogleTranslator(source='auto', target=targetLang).translate(content)
    return translated_text

with st.form("my_form"):
    url = st.text_input(label="Enter the youtube video link", help="Enter the youtube video link")
    st.write("Choose preferences")
    toSummarize = st.checkbox("Summarize the content to the desired length")
    summarization_length = st.slider("Summarization Length: ", min_value=150, max_value=350, value=200)
    selected_language = st.selectbox("Choose the language you want to translate to", ["English"] + [label.capitalize() for label in langs_dict])
    submitted = st.form_submit_button("Transcribe")

while not submitted:
    pass

def show_progress(request, length = 502161): 
    # talk_output(request) 
    my_bar = st.progress(0, text=request)
    for percent_complete in range(100):
        time.sleep(0.01)
        my_bar.progress(percent_complete + 1, text=request)

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

if selected_language != 'English':
    translated_content = translate(summarized_content, selected_language)
    st.write(summarized_content)
    type_output(f"Voice over is currently not supported for {selected_language}.\nOriginal version: \n"+ translated_content)
    st.divider()
else:
    type_output(summarized_content)
    talk_output(summarized_content)

# talkThread = Thread(target = talk_output, args=(summarized_content,))
# talkThread.start()
# talkThread.join()

type_output("\nThank you for using", 0.3)
# st.balloons()

# typeThread = Thread(target = type_output, args=(summarized_content,))
# typeThread.start()
# typeThread.join()

# st.download_button("Download the output file as text", data="news.webm")
# st.success('🤗')


# Token indices sequence length is longer than the specified maximum sequence length for this model (2246 > 1024). Running this sequence through the model will result in indexing errors