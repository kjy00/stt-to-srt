import moviepy.editor as mp
from pydub import AudioSegment

clip = mp.VideoFileClip("conan2.mp4")
clip.audio.write_audiofile("audio.mp3")
AudioSegment.from_mp3("audio.mp3").export("test.wav", format="wav", bitrate="44100")
sound = AudioSegment.from_wav("test.wav")
sound = sound.set_channels(1)
sound.export("test.wav", format="wav")

