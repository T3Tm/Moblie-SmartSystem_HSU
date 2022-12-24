import time
import RPi.GPIO as GPIO
def distanceEntranceOn(data):#초음파 센서 측정하는지 판단.
  data['distanceEntranceOnOff']=True

def distanceEntranceOff(data):
  data['distanceEntranceOnOff']=False
  
def distanceDoorOn(data):
  data['distanceDoorOnOff']=True
  
def distanceDoorOff(data):
  data['distanceDoorOnOff']=False


trig1 = 20
echo1 = 16
trig2 = 6
echo2 = 5
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(trig1, GPIO.OUT)
GPIO.setup(echo1, GPIO.IN)
GPIO.output(trig1, False)

GPIO.setup(trig2, GPIO.OUT)
GPIO.setup(echo2, GPIO.IN)
GPIO.output(trig2, False)

def measureDistance(trig,echo):
  time.sleep(0.5)
  GPIO.output(trig, True) # 신호 1
  time.sleep(0.00001) # 짧은 시간을 나타내기 위함
  GPIO.output(trig, False) # 신호가 1-> 0으로 떨어질 때 초음파발생

  while(GPIO.input(echo) == 0):pass
  pulse_start = time.time() # echo 신호가 1인 경우, 초음파 발사된 순간 	
  while(GPIO.input(echo) == 1):pass
  pulse_end = time.time() # 초음파 신호가 도착한 순간
  # echo 신호가 1->0으로 되면 보낸 초음파 수신 완료

  pulse_duration = pulse_end - pulse_start
  return 340*100/2*pulse_duration

