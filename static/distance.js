//거리 측정해서 바꾸기
var count=0;
var arr=[];
function Entrancedist(dist){
  var distance=document.getElementById("distance");
  distance.innerHTML="";
  arr.push("현관까지 거리는 : " + dist +"입니다." +"<br>");
  count++;
  if(count>40){//40개 넘어가면 맨 위에 있던 데이터 사라지고 다음 데이터가 보여짐.
    arr.shift();
    count=40;
  }
  for(let i=0;i<count;i++){
    distance.innerHTML+=arr[i];
  }
}
function Doordist(dist){
  var distance=document.getElementById("distance");
  distance.innerHTML="";
  arr.push("문까지 거리는 : " + dist +"입니다."+"<br>");
  count++;
  if(count >40){//40개 넘어가면 맨 위에 있던 데이터 사라지고 다음 데이터가 보여짐.
    arr.shift();
    count=40;
  }
  for(let i=0;i<count;i++){
    distance.innerHTML+=arr[i];
  }
}


function startEntrance(){
  subscribe("distanceEntrance");
  publish("startdistance","Entrance");
}
function stopEntrance(){
  unsubscribe("distanceEntrance");
  publish("stopdistance","Entrance");
}
function startDoor(){
  subscribe("distanceDoor");
  publish("startdistance","Door");
}
function stopDoor(){
  unsubscribe("distanceDoor");
  publish("stopdistance","Door");
}