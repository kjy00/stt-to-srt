import moviepy.editor as mp
from pydub import AudioSegment

clip = mp.VideoFileClip("conan2.mp4") #따옴표 안에 영상파일 이름을 넣는다
clip.audio.write_audiofile("audio.mp3") #mp4파일을 mp3로 바꾼다.
AudioSegment.from_mp3("audio.mp3").export("test.wav", format="wav", bitrate="44100") #mp3를 wav파일로 바꾼다.
sound = AudioSegment.from_wav("test.wav")
sound = sound.set_channels(1)
sound.export("test.wav", format="wav")

