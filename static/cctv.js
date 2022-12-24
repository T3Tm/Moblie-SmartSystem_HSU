//카메라 js파일

var canvas;
var context;
var img;
window.addEventListener("load",function(){
  canvas = document.getElementById("canvas");
  context = canvas.getContext("2d");
  img = new Image();
  img.onload = function(){
    context.drawImage(img,0,0);
  }
});
function mqtt_Camera(){
  //사진 찍어달라고 보내줌. //video 토픽으로 붙음
  subscribe("video");
  publish("takePicture","startPicture");
}
//img부분에 사진을 바꾼다.
function changecanvas(imgfile){
  img.src=imgfile;
}
function mqtt_CameraOff(){
  //그만 찍어달라고 요청을 보낸다.
  //video 토픽에서 떨어진다.
  unsubscribe("video");
  publish("takePicture","stopPicture");
}