import sys
import os
import io
import time
import picamera
import RPi.GPIO as GPIO
from PIL import Image, ImageFilter
import paho.mqtt.client as mqtt
import cv2
import numpy as np

# 전역 변수 선언 및 초기화
fileName = ""
stream = io.BytesIO()


isStarted = False

camera = cv2.VideoCapture(0, cv2.CAP_V4L) # 0번 카메라
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
camera.set(cv2.CAP_PROP_BUFFERSIZE, 1) # 버퍼크기는 1~10까지 유효함
buffersize = camera.get(cv2.CAP_PROP_BUFFERSIZE) #버퍼 못 읽음. < 
print("버퍼 개수는 %d " % buffersize)

def takePicture() :
        global fileName
        global stream
        global camera
        global buffersize

        # 이전에 만들어둔 사진 파일이 있으면 삭제
        if len(fileName) != 0:os.unlink(fileName)

        stream.seek(0) # 파일 포인터를 스트림 맨 앞으로 위치시킴. 이곳에서부터 >이미지 데이터 저장
        stream.truncate()
        # cv2의 버퍼에 저장된 프레임 제거하고 최신 프레임을 읽기 위한코드
        for i in range(int(buffersize)+1): #프레임 안 읽음 ;
                ret, frame = camera.read() # 프레임 읽기

        if not(ret):    # 프레임정보를 정상적으로 읽지 못하면
                print("사진 촬영 실패")       
        
        pilim = Image.fromarray(frame)#Nonetype
        pilim.save(stream, 'jpeg') # 프레임을 jpeg 형태로 바꾸기
        data = np.frombuffer(stream.getvalue(), dtype=np.uint8) # stream에 저장된 프레임을 unit8 타입으로 변환
        image = cv2.imdecode(data, 1)

        takeTime = time.time() # 현재 시간 알아내기
        fileName = "./static/%d.jpg" % (takeTime * 10) # 현재 시간으로 파일 이름 생성
        cv2.imwrite(fileName, image) # 사각형이 그려진 프레임 이미지를 파일에 저장
        return fileName


def onConnect(client, userdata, flag, rc):
        print("Connect with result code:"+ str(rc))
        client.subscribe("command", qos = 0)
        pass

def onMessage(client, userdata, msg):
        global isStarted
        command = str(msg.payload.decode("utf-8"))
        print("receive message =%s" % command)
        if(command == 'start'):
                isStarted = True
        elif(command == 'stop'):
                isStarted = False
        pass

trig = 6
echo = 5
GPIO.setmode(GPIO.BCM) # BCM 모드로 작동
GPIO.setwarnings(False) # 경고글이 출력되지 않게 설정
GPIO.setup(trig, GPIO.OUT) #trig에서 초음파 나가게 함
GPIO.setup(echo, GPIO.IN) #echo에서 초음파 받음
GPIO.output(trig, False) #처음에는 초음파를 안쏨

def measureDistance(trig, echo):
  time.sleep(0.5)
  GPIO.output(trig, True) # 신호 1
  time.sleep(0.00001) # 짧은 시간을 나타내기 위함
  GPIO.output(trig, False) # 신호가 1-> 0으로 떨어질 때 초음파발생
  
  while(GPIO.input(echo) == 0):
      pass
  pulse_start = time.time() # echo 신호가 1인 경우, 초음파 발사된 순간 
  while(GPIO.input(echo) == 1):
      pass
  pulse_end = time.time() # 초음파 신호가 도착한 순간
  # echo 신호가 1->0으로 되면 보낸 초음파 수신 완료

  pulse_duration = pulse_end - pulse_start #시간
  return 340*100/2*pulse_duration #거리 출력

def led(distance):
  if (distance<=20 and distance>10): #거리가 10초과 20이하면 빨간 등만 켜지게 함
    GPIO.output(ledA,1) #ledA 켜짐
    GPIO.output(ledB,0) #ledB 꺼짐
  elif (distance <= 10): #거리가 10이하면 led 2개 모두 켜지게 함
    GPIO.output(ledB,1) #ledB 켜짐
    GPIO.output(ledA,1) #ledA 켜짐
    
    client.publish('picture', takePicture())
        
  elif (distance >=20): #거리가 20이상이면 둘 다 꺼지게 함
    GPIO.output(ledA,0) #ledA 꺼짐
    GPIO.output(ledB,0) #ledB 꺼짐
def ledOnOff(led, onOff): # led 번호의 핀에 onOff(0/1) 값 출력하는 함수
  GPIO.output(led, onOff)

ledA = 27 # 핀 번호 GPIO27 의미. 빨간 led
GPIO.setup(ledA, GPIO.OUT) # GPIO 5번 핀을 출력 선으로 지정.

ledB = 22 # 핀 번호 GPIO22 의미. 녹색 led
GPIO.setup(ledB, GPIO.OUT) # GPIO 6번 핀을 출력 선으로 지정.

onOff = 1 # 1은 디지털 출력 값. 1 = 5V

broker_address = "192.168.137.19" #내 IP 주소

client = mqtt.Client()
client.on_connect = onConnect
client.on_message = onMessage

client.connect(broker_address, 1883)
client.loop_start()


while(True):#사진 토픽 계속 보냄.
  distance = measureDistance(trig, echo)
  client.publish('ultrasonic',distance)
  led(distance)
  

client.loop_stop()
client.disconnect()