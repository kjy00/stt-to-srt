# -*- coding: utf-8 -*-
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


sound = AudioSegment.from_wav("test.wav")
sound = sound.set_channels(1)
sound.export("test.wav", format="wav")


''' ~~~~~~~~~~~~~~'''



# create a speech recognition object
r = sr.Recognizer()
path = './test.wav'

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
        speech_contexts=[{"phrases":["참다", "크기", "고기", "남기다", "서양", "주요", "지나치다", "가져오다", "냄새", "부드럽다", "여기다", "이", "공연", "남녀", "내놓다", "떼다", "만들어지다", "속도", "심각하다", "준비", "계속되다", "구월", "맑다", "소년", "소식", "유월", "작용", "허리", "골", "공업", "그중", "노인", "벌다", "살리다", "새", "영어", "출신", "결정", "경향", "기록", "나름", "대답하다", "반면", "썰다", "움직임", "이미지", "터지다", "특성", "교장", "벗다", "업무", "입시", "준비하다", "청소년", "돕다", "응", "이기다", "찾아보다", "취하다", "다루다", "달", "사장", "삼월", "그렇지만", "선배", "업체", "키", "구하다", "국회", "그러므로", "포함하다", "걱정", "결혼하다", "만약", "바르다", "세월", "숨", "행사", "깨닫다", "누나", "신", "왕", "점점", "질문", "특별", "판단", "해결하다", "거리", "계속하다", "그치다", "근처", "너무나", "높이다", "부정", "사정", "도대체", "막", "부모님", "수출", "계시다", "그", "자르다", "데리다", "마리", "무척", "비용", "비행기", "옳다", "원래", "처리", "최초", "꼴", "놀이", "뜨겁다", "뿌리", "수입", "초", "그리하여", "낮", "일찍", "직원", "찍다", "가볍다", "내부", "다소", "상대", "오전", "피부", "가게", "가득", "그저", "도", "벽", "장군", "무역", "부담", "약속", "인사", "줄", "쳐다보다", "충분히", "대", "신체", "에너지", "위원", "정리하다", "집안", "배경", "죽이다", "단순하다", "반대", "법칙", "빠지다", "소금", "오염", "자전거", "참여하다", "탓", "푸르다", "그래", "목", "발표", "범죄", "위", "흔들다", "기초", "논리", "드라마", "뽑다", "피우다", "감각", "미리", "부족하다", "인사", "저희", "진행되다", "교통", "기구", "법", "오랜", "젊은이", "후보", "거리", "과제", "근거", "기록하다", "다가오다", "불다", "시각", "이끌다", "종합", "한글", "가을", "개발하다", "내일", "떨다", "매일", "손가락"]}])

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
    song = AudioSegment.from_mp3("./test.wav")
    rttm = open("./descendent.rttm", 'r')
    i = 0
    global spk 
    spk = list()
    line = rttm.readline()

    if line: 
        s_time = float(line.split()[3]) * 1000
        spk.append(line.split()[7])
        f = song[0:s_time]
        beginning = f
        path = os.path.join("./audio-chunks", f"chunk{i}.wav")
        beginning.export(path, format='wav', parameters=["-q:a", "10", "-ac", "1"])
        while True:
            line = rttm.readline()
            if not line: break
            spk.append(line.split()[7])
            n_time = float(line.split()[3]) * 1000
            print(s_time, n_time)
            i = i + 1
            f = song[s_time:n_time]
            beginning = f
            path = os.path.join("./audio-chunks", f"chunk{i}.wav")
            beginning.export(path, format='wav', parameters=["-q:a", "10", "-ac", "1"])
            s_time = n_time - 400
        rttm.close()
    return i+1
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
                file.write('\n' + spk[i] + ' ' + text + '\n\n')
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


