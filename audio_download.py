from threading import Thread
import time
import sys
import os
import pafy
import assemblyai as aai
import pyttsx3
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import transformers
import datetime

def generate_timestamp():
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y%m%d_%H%M%S")
    return timestamp


def summarize_huggingface(text, desired_output_length = 150):
  if len(text) > 1024:
      text = text[:1024]
  summarizer = transformers.pipeline("summarization", model="sshleifer/distilbart-cnn-12-6", revision="a4f8f3e")
  summary = summarizer(text)[0]["summary_text"]
  return summary

def get_minimum_size(url):
    video = pafy.new(url)
    audiostreams = video.audiostreams
    minimumsize = audiostreams[0]
    for i in audiostreams:
        if minimumsize.get_filesize() > i.get_filesize():
            minimumsize = i
    print(minimumsize.get_filesize())
    return minimumsize  

def get_audio(minimumsize):
    print("Extracting audio")
    timestamp = generate_timestamp()
    filename = f"audio_{timestamp}.{minimumsize.extension}"
    contentname = minimumsize.generate_filename().split('.')[0]
    minimumsize.download(filename) 
    return filename, contentname   

def transcribe(filename):
    aai.settings.api_key = "a7723b7c7765451a9ad0d36e27a13ffe"
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(filename)
    print(transcript.text)
    return transcript.text

def talk_output(content):
    converter = pyttsx3.init()
    converter.setProperty('rate', 200)
    converter.setProperty('volume', 1)
    for sentence in content.split('\n'):
        converter.say(sentence)
    converter.runAndWait()

def type_output(content):
    for letter in content:
        print(letter, end = "", flush=True)
        time.sleep(0.03)

def summarize(content):
    text = content
    stopWords = set(stopwords.words("english"))
    words = word_tokenize(text)

    freqTable = dict()
    for word in words:
        word = word.lower()
        if word in stopWords:
            continue
        if word in freqTable:
            freqTable[word] += 1
        else:
            freqTable[word] = 1
    
    sentences = sent_tokenize(text)
    sentenceValue = dict()
    
    for sentence in sentences:
        for word, freq in freqTable.items():
            if word in sentence.lower():
                if sentence in sentenceValue:
                    sentenceValue[sentence] += freq
                else:
                    sentenceValue[sentence] = freq
    sumValues = 0
    for sentence in sentenceValue:
        sumValues += sentenceValue[sentence]
    
    average = int(sumValues / len(sentenceValue))
    summary = ''
    for sentence in sentences:
        if (sentence in sentenceValue) and (sentenceValue[sentence] > (1.2 * average)):
            summary += " " + sentence
    # if len(summary) > 10:
    #     return summary
    return content


def load_animation(action):
    load_str = action
    ls_len = len(load_str)
    animation = "|/-\\"
    anicount = 0
    counttime = 0        
    i = 0                     
    while (counttime != 100):
        time.sleep(0.075) 
        load_str_list = list(load_str) 
        x = ord(load_str_list[i])
        y = 0                             
        if x != 32 and x != 46:             
            if x>90:
                y = x-32
            else:
                y = x + 32
            load_str_list[i]= chr(y)
        res =''             
        for j in range(ls_len):
            res = res + load_str_list[j]
        sys.stdout.write("\r"+res + animation[anicount])
        sys.stdout.flush()
        load_str = res
        anicount = (anicount + 1)% 4
        i =(i + 1)% ls_len
        counttime = counttime + 1
    if os.name =="nt":
        os.system("cls")


if __name__ =="__main__":
    url = input("Enter youtube url to summarize: ")
    filename, contentname = get_audio(get_minimum_size(url))
    load_animation("fetching " + contentname)

    content = transcribe(filename)
    os.remove(filename)
    # summarized_content = summarize(content)
    summarized_content = summarize_huggingface(content, 100)
    print(contentname + '\n')

    typeThread = Thread(target = type_output, args=(summarized_content,))
    talkThread = Thread(target = talk_output, args=(summarized_content,))
 
    typeThread.start()
    talkThread.start()
 
    typeThread.join()
    talkThread.join()

 