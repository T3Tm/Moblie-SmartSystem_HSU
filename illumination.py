import time
import RPi.GPIO as GPIO
import Adafruit_MCP3008

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

mcp = Adafruit_MCP3008.MCP3008(clk=11, cs=8, miso=9, mosi=10)

def senserOn(data):#조도 센서 측정하기
  data['illuminationOnOff']=True

def senserOff(data):
  data['illuminationOnOff']=False

def checksensor():
  time.sleep(1)
  return mcp.read_adc(0)