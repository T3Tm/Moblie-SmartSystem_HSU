import distance
import illumination
import camera
import paho.mqtt.client as mqtt
def onConnect(client, userdata, flag, rc):
  print('정상 연결 되었습니다.')
  client.subscribe('startdistance')
  client.subscribe('stopdistance')
  client.subscribe('Sensor')
  client.subscribe('takePicture')
  
def onMessage(client, userdata, msg):
  global mapArr
  print(msg.topic,msg.payload)
  command = str(msg.payload.decode("utf-8"))
  if msg.topic == "startdistance": #메세지의 토픽이 거리 재기 일 때
    if command== "Entrance": #현관까지 거리 재기
      distance.distanceEntranceOn(mapArr)
    elif command== "Door":#문까지 거리 재기
      distance.distanceDoorOn(mapArr)
  elif msg.topic == "stopdistance":
    if command== "Entrance": 
      distance.distanceEntranceOff(mapArr)
    elif command== "Door":
      distance.distanceDoorOff(mapArr)
  elif msg.topic == "Sensor": #조도센서
    if command == "startsensor":
      illumination.senserOn(mapArr)
    elif command == "stopsensor":
      illumination.senserOff(mapArr)
  elif msg.topic == "takePicture":
    if command == "startPicture":
      camera.startPicture(mapArr)
    elif command == "stopPicture":
      camera.stopPicture(mapArr)

broker_address = "192.168.137.223"

client = mqtt.Client()
client.on_connect = onConnect
client.on_message = onMessage

client.connect(broker_address, 1883)
client.loop_start()

mapArr={'pictureOnOff':False,
        'illuminationOnOff':False,
        'distanceEntranceOnOff':False,
        'distanceDoorOnOff':False}
topic={'pictureOnOff':"video",
      'illuminationOnOff':"sensor",
      'distanceEntranceOnOff':"distanceEntrance",
      'distanceDoorOnOff':"distanceDoor"}
while(True):
  for key,value in mapArr.items():
    if(value==True):
      if 'picture' in key:
        client.publish(topic[key],camera.takePhoto())
      elif 'illumi' in key:
        value=illumination.checksensor()
        print(value)
        client.publish(topic[key],value)
      elif 'Entrance' in key:
        client.publish(topic[key],distance.measureDistance(20,16))
      elif 'Door' in key:
        client.publish(topic[key],distance.measureDistance(6,5))
client.loop_stop()
client.disconnect()