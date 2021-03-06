# importing libraries
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL)
import speech_recognition as sr 
import os
import contextlib
import wave
import pandas as pd
import datetime
from pydub import AudioSegment
from pydub.silence import split_on_silence
from google.cloud import storage
import moviepy.editor as mp
from pydub import AudioSegment

'''mp4 to wav code'''

clip = mp.VideoFileClip("descendent.mp4")
clip.audio.write_audiofile("audio.mp3")
AudioSegment.from_mp3("audio.mp3").export("test.wav", format="wav", bitrate="44100")

#AudioSegment.from_mp3("test.wav_vocals.mp3").export("test.wav", format="wav", bitrate="44100")

sound = AudioSegment.from_wav("test.wav")
sound = sound.set_channels(1)
sound.export("test.wav", format="wav")

os.system("spleeter separate -p spleeter:2stems -o output audio.mp3")

sound2 = AudioSegment.from_wav("./output/audio/vocals.wav")
sound2 = sound2.set_channels(1)
sound2.export("./output/audio/vocals.wav", format="wav")

''' ~~~~~~~~~~~~~~'''



# create a speech recognition object
r = sr.Recognizer()
path = './output/audio/vocals.wav'

file = open('script.srt','w')

'''***'''
'''stt'''
'''***'''
def run_quickstart(i):
    from google.cloud import speech
    client = speech.SpeechClient()
	
    gcs_uri = "gs://capstone2bucket/chunk"+str(i)+".wav"
#gcs_uri = "gs://capstone2/chunk"+str(i)+".wav"

    audio = speech.RecognitionAudio(uri=gcs_uri)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=44100,
        language_code="ko-KR",
        speech_contexts=[{"phrases":["동만이", "애라"]}]
    )

    # Detects speech in the audio file
    response = client.recognize(config=config, audio=audio)
    txt=""
    for result in response.results:
        print(i)
        txt += " {}".format(result.alternatives[0].transcript)
    return txt
# a function that splits the audio file into chunks
# and applies speech recognition



''' 구글 클라우드 스토리지에 올리기'''	
def updateStorage(i):
#length = len(os.listdir('./audio-chunks'))
    bucket_name = 'capstone2bucket'    # 서비스 계정 생성한 bucket 이름 입력

#for i in range(1, length):
    source_file_name = './audio-chunks/chunk' + str(i) + '.wav'    # GCP에 업로드할 파일 절대경로
    destination_blob_name = 'chunk' + str(i) + '.wav'    # 업로드할 파일을 GCP에 저장할 때의 이름


    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

def cuttingWav(): 

    chunks = list()
    song = AudioSegment.from_mp3("./output/audio/vocals.wav")

    with contextlib.closing(wave.open("./output/audio/vocals.wav",'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)
        print(duration)

    duration = duration * 1000
    five_seconds = 5 * 1000
    one_min = five_seconds * 6 * 2

    i = 0
    f = song[:five_seconds]
    beginning = f
    path = os.path.join("./audio-chunks", f"chunk0.wav")
    beginning.export(path, format='wav', parameters=["-q:a", "10", "-ac", "1"])
    next_five_seconds = five_seconds

    while next_five_seconds <= duration:
        i = i + 1
        now = next_five_seconds
        next_five_seconds = next_five_seconds + five_seconds
        f = song[now:next_five_seconds]
        beginning = f
        path = os.path.join("./audio-chunks", f"chunk{i}.wav")
        beginning.export(path, format='wav', parameters=["-q:a", "10", "-ac", "1"])
        if next_five_seconds + five_seconds > duration:
            i = i + 1
            now = next_five_seconds
            next_five_seconds = next_five_seconds + five_seconds
            f = song[now:duration]
            beginning = f
            path = os.path.join("./audio-chunks", f"chunk{i}.wav")
            beginning.export(path, format='wav', parameters=["-q:a", "10", "-ac", "1"])
    return i


def get_large_audio_transcription(path):
    """
    Splitting the large audio file into chunks
    and apply speech recognition on each of these chunks
    """
    '''
    length = 0 #the length of wav file
    start = 0
    end = 0
    # open the audio file using pydub
    sound = AudioSegment.from_wav(path)  
    # split audio sound where silence is 700 miliseconds or more and get chunks
	'''
    start = 0
    end = 0
    wavNum = 0
    '''
    chunks = split_on_silence(sound,
        # experiment with this value for your target audio file
        min_silence_len = 280,
        # adjust this per requirement
        silence_thresh = sound.dBFS-14,
        # keep the silence for 1 second, adjustable as well
        keep_silence=240,
    )'''
    folder_name = "audio-chunks"
    # create a directory to store the audio chunks
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    whole_text = ""
    wavNum = cuttingWav()
    # process each chunk 
    for i in range(0, wavNum):
        # export audio chunk and save it in
        # the `folder_name` directory.
        chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
        tmpSong = AudioSegment.from_wav(chunk_filename)
        tmpSong.export(chunk_filename, format="wav")
        # recognize the chunk
		#jiseo add code
        
        updateStorage(i)
        with contextlib.closing(wave.open(f"audio-chunks/chunk{i}.wav",'r')) as f:
            frames=f.getnframes()
            rate = f.getframerate()
            duration = frames / float(rate) 
            start = end
            end += duration #누적값
            start_time = str(datetime.timedelta(microseconds= start * 1000000))
            end_time = str(datetime. timedelta(microseconds = end * 1000000))
            start_time = '0' + start_time.replace('.',',')[:11]
            end_time = '0' + end_time.replace('.',',')[:11]
            if (len(start_time) == 8):
                start_time += ',000'
            if (len(end_time) == 8):
                end_time += ',000'
            file.write(str(i) +'\n'+ start_time +' --> ' +  end_time)


        with sr.AudioFile(chunk_filename) as source:
            audio_listened = r.record(source)
            # try converting it to text
            try:
                text = run_quickstart(i)
                file.write('\n' + text + '\n\n')
            except sr.UnknownValueError as e:
                print("Error:", str(e))
                file.write('\n\n')
            else:
                text = f"{text.capitalize()}. "
                print(text)
                whole_text += text
    # return the text for all chunks detected
    return whole_text
get_large_audio_transcription(path)
file.close()


