# importing libraries 
import speech_recognition as sr 
import os
import contextlib
import wave
import pandas as pd
import datetime
from pydub import AudioSegment
from pydub.silence import split_on_silence

# create a speech recognition object
r = sr.Recognizer()
path = './test.wav'

file = open('script.srt','w')


# a function that splits the audio file into chunks
# and applies speech recognition
def get_large_audio_transcription(path):
    """
    Splitting the large audio file into chunks
    and apply speech recognition on each of these chunks
    """
    length = 0 #the length of wav file
    start = 0
    end = 0
    # open the audio file using pydub
    sound = AudioSegment.from_wav(path)  
    # split audio sound where silence is 700 miliseconds or more and get chunks
    chunks = split_on_silence(sound,
        # experiment with this value for your target audio file
        min_silence_len = 240,
        # adjust this per requirement
        silence_thresh = sound.dBFS-14,
        # keep the silence for 1 second, adjustable as well
        keep_silence=240,
    )
    folder_name = "audio-chunks"
    # create a directory to store the audio chunks
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    whole_text = ""
    # process each chunk 
    for i, audio_chunk in enumerate(chunks, start=1):
        # export audio chunk and save it in
        # the `folder_name` directory.
        chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
        audio_chunk.export(chunk_filename, format="wav")
        # recognize the chunk
		#jiseo add code
        with contextlib.closing(wave.open(f"audio-chunks/chunk{i}.wav",'r')) as f:
            frames=f.getnframes()
            rate = f.getframerate()
            duration = frames / float(rate) 
#print(duration)i
            start = end
            end += duration #누적값
            start_time = str(datetime.timedelta(microseconds= start * 1000000))
            end_time = str(datetime. timedelta(microseconds = end * 1000000))
            start_time = start_time.replace('.',',')[:11] + " --> "
            end_time = end_time.replace('.',',')[:11]
            file.write(str(i) +'\n'+ start_time + end_time)


        with sr.AudioFile(chunk_filename) as source:
            audio_listened = r.record(source)
            # try converting it to text
            try:
                text = r.recognize_google(audio_data=audio_listened,language='ko-KR')
                file.write('\n' + text + '\n\n')
            except sr.UnknownValueError as e:
                print("Error:", str(e))
                file.write('\n\n')
            else:
                text = f"{text.capitalize()}. "
                print(chunk_filename, ":", text)
                whole_text += text
    # return the text for all chunks detected
    return whole_text
whole_text = get_large_audio_transcription(path)
file.write(whole_text)
file.close()
