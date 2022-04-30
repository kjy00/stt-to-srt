# -*- coding: utf-8 -*-

import os
import re

path = os.path.split(os.path.realpath("C:/Users/User/Desktop/react_app/build"))

def getFileName(key):
    FileName = []
    for getFile in os.listdir(path[0]):
        if os.path.splitext(getFile)[1] == '.srt':
            FileName.append(os.path.splitext(getFile)[0])
    return FileName

def srt2vtt(inFileName):
    subNo = 1
    outFileName = "C:/Users/User/Desktop/react_app/build/script.vtt"
    inFileName = "C:/Users/User/Desktop/react_app/build/script.srt"#inFileName + '.srt'
    with open(inFileName, 'r', encoding='utf-8') as procFile:
        outFile = open(outFileName, 'w+', encoding='utf-8')
        outFile.write('WEBVTT\n')
        for lineContent in procFile.readlines():
            if lineContent.strip() == str(subNo):
                subNo += 1
                pass
            else:
                if re.match('(\d{2}:\d{2}:\d{2}),(\d{3})', lineContent):
                    lineContent = re.sub('(\d{2}:\d{2}:\d{2}),(\d{3})', lambda m: m.group(1) + '.' + m.group(2), lineContent)
                outFile.write(lineContent)
    outFile.close()
    print('[' + inFileName + '] transform completed!')

def main():
      allFileName = getFileName(key)
      if allFileName == []:
          print('There are no srt files here.')
      else:
          for fileName in allFileName:
              print(fileName)
              srt2vtt(fileName)
      main()

if __name__ == '__main__':
    print('\n[Notice] Current directory: ' + path[0])
    print('\nPlease select the method of subtitle transforming.')
    main()
    input("\nMission Completed.\nPress any key to exit.")
