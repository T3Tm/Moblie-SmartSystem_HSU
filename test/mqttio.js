var client=null;
var clinetID=null;
function Start(){
  clientID = "clientID-" + parseInt(Math.random() * 100); // 랜덤한 사용자 ID 생성

    // 사용자가 입력한 브로커의 IP 주소와 포트 번호 알아내기
    broker = document.getElementById("broker").value; // 브로커의 IP 주소
    port = document.getElementById("port").value; // 브로커의 포트 번호

    // MQTT 메시지 전송 기능을 모두 가징 Paho client 객체 생성
    client = new Paho.MQTT.Client(broker, Number(port), clientID);

    // client 객체에 콜백 함수 등록
    client.onConnectionLost = onConnectionLost; // 접속이 끊어졌을 때 실행되는 함수 등록
    client.onMessageArrived = onMessageArrived; // 메시지가 도착하였을 때 실행되는 함수 등록

    // 브로커에 접속. 매개변수는 객체 {onSuccess : onConnect}로서, 객체의 프로퍼틴느 onSuccess이고 그 값이 onConnect.
    // 접속에 성공하면 onConnect 함수를 실행하라는 지시

    // 메세지가 도착했을 때
  var options = {
    timeout:3,
    onSuccess:onConnect,  // 접속 성공 했을 때 실행될 콜백함수 등록
    onFailure:onFailure,
  }
  client.connect(options);
  // document.getElementById("empty").value=clientID;
}

//성공했을 때 호출되는 함수
function onConnect(){
  console.log("연결 성공하였습니다.");
  console.log(clientID+"이거입니다.");
  isconnected=true;
}
function onFailure(){
  console.log("접속실패");
}
function disconnect(){
  alert("연결이 끊겼습니다.");
  client.disconnect();
  isconnected=false;
}

//연결 끊길 때 객체한테서 비이상적으로 연결이 끊겼는지 로그 찍어보기.
function onConnectionLost(responseObject){
  //연결이 끊겼을 때도 알림으로 연결이 끊겼다고 알려준다.
  alert("연결이 끊겼습니다.");
  if(responseObject.errorCode!=0){
    console.log("오류 발생" + responseObject.errorMessage);
  }
}

//메세지 도착시 호출되는 함수
function onMessageArrived(msg){
  if(msg.destinationName == "video"){//영상이 왔음
    changecanvas(msg.payloadString);
  }else if(msg.destinationName == "distanceEntrance"){//거리가 왔음
    change(msg.payloadString);
  }else if(msg.destinationName == "distanceDoor"){//거리가 왔음
    change(msg.payloadString);
  }else if(msg.destinationName=="sensor"){
    addChartData(parseFloat(msg.payloadString)); 
  }
}
//연결 됐는지 확인하는 함수
var isconnected = false;

//publish 함수
function publish(topic,msg){
  if(client==null)return;
  client.send(topic,msg,0,false);
}
function unsubscribe(topic){
  if(client == null || isconnected!=true)return;
  client.unsubscribe(topic);
}
//subscribe 함수
function subscribe(topic){
  if(client==null)return;
  client.subscribe(topic);
} 