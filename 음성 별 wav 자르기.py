from pydub import AudioSegment
import wave
import contextlib
import os

song = AudioSegment.from_mp3("C:/Users/User/Documents/카카오톡 받은 파일/test.wav")

rttm = open("C:/Users/User/Documents/카카오톡 받은 파일/file.rttm", 'r')
i = 0
line = rttm.readline()
spk = list()

if line: 
    s_time = float(line.split()[3]) * 1000
    spk.append(line.split()[7])
    f = song[0:s_time]
    beginning = f
    path = os.path.join("C:/Users/User/Desktop/2022_4학년_1학기/캡스톤2", f"res{i}.wav")
    beginning.export(path, format='wav', parameters=["-q:a", "10", "-ac", "1"])
    while True:
        line = rttm.readline()
        if not line: break
        spk.append(line.split()[7])
        n_time = float(line.split()[3]) * 1000
        #r_time = n_time - s_time
        print(s_time, n_time)
        i = i + 1
        f = song[s_time:n_time]
        beginning = f
        path = os.path.join("C:/Users/User/Desktop/2022_4학년_1학기/캡스톤2", f"res{i}.wav")
        #path = "C:/Users/User/Desktop/2022_4학년_1학기/캡스톤2/result"+i+".wav"
        beginning.export(path, format='wav', parameters=["-q:a", "10", "-ac", "1"])
        s_time = n_time
    rttm.close()
