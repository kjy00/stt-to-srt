from pydub import AudioSegment
import wave
import contextlib
import os

song = AudioSegment.from_mp3("C:/Users/User/Desktop/2022_4학년_1학기/캡스톤2/test.wav")

with contextlib.closing(wave.open("C:/Users/User/Desktop/2022_4학년_1학기/캡스톤2/test.wav",'r')) as f:
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
path = os.path.join("C:/Users/User/Desktop/2022_4학년_1학기/캡스톤2", f"result{i}.wav")
next_five_seconds = five_seconds

while next_five_seconds <= duration:
    i = i + 1
    now = next_five_seconds
    next_five_seconds = next_five_seconds + five_seconds
    f = song[now:next_five_seconds]
    beginning = f
    path = os.path.join("C:/Users/User/Desktop/2022_4학년_1학기/캡스톤2", f"result{i}.wav")
    #path = "C:/Users/User/Desktop/2022_4학년_1학기/캡스톤2/result"+i+".wav"
    beginning.export(path, format='wav', parameters=["-q:a", "10", "-ac", "1"])
    #now = next_five_seconds
    #next_five_seconds = next_five_seconds + five_seconds
    #i = i + 1
    if next_five_seconds + five_seconds > duration:
        i = i + 1
        now = next_five_seconds
        next_five_seconds = next_five_seconds + five_seconds
        f = song[now:duration]
        beginning = f
        path = os.path.join("C:/Users/User/Desktop/2022_4학년_1학기/캡스톤2", f"result{i}.wav")
        beginning.export(path, format='wav', parameters=["-q:a", "10", "-ac", "1"])
