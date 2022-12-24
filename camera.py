import io
import os
import time
import cv2
from PIL import Image,ImageFilter
import numpy as np

fileName = ""
stream = io.BytesIO()

camera = cv2.VideoCapture(0, cv2.CAP_V4L) # 0번 카메라
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
camera.set(cv2.CAP_PROP_BUFFERSIZE, 1) # 버퍼크기는 1~10까지 유효함
buffersize = camera.get(cv2.CAP_PROP_BUFFERSIZE)

def takePhoto():
  global fileName
  global stream
  global camera
  global buffersize
  time.sleep(5)
  # 이전에 만들어둔 사진 파일이 있으면 삭제
  if len(fileName) != 0:
          os.unlink(fileName)

  stream.seek(0) # 파일 포인터를 스트림 맨 앞으로 위치시킴. 이곳에서부터 >이미지 데이터 저장
  stream.truncate()

  for i in range(int(buffersize)+1):ret, frame = camera.read() # 프레임 읽기
  
  pilim = Image.fromarray(frame)
  pilim.save(stream, 'jpeg') # 프레임을 jpeg 형태로 바꾸기
  data = np.frombuffer(stream.getvalue(), dtype=np.uint8) # stream에 저장된 프레임을 unit8 타입으로 변환
  image = cv2.imdecode(data, 1)

  takeTime = time.time() # 현재 시간 알아내기
  fileName = "./static/%d.jpg" % (takeTime * 10) # 현재 시간으로 파일 이름 생성
  cv2.imwrite(fileName, image) # 사각형이 그려진 프레임 이미지를 파일에 저장
  return fileName

def startPicture(data):#카메라 이제 찍기
  data['pictureOnOff']=True

def stopPicture(data):
  data['pictureOnOff']=False
