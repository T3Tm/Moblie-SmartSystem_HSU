var ctx = null
var chart = null
var label_size=20;
var count=0;
var config = {
  type : 'line',
  data:{
    labels: ['0초','1초','2초'],
    datasets:[{
      label: '막대 그래프 사례',
      backgroundColor : 'rgb(255,99,132)',
      borderColor : 'yellow',
      data : [], // 기준치를 0으로 잡아야 한다.
      fill:false,
    }],
    
  },
  options: {
    responsive : false, // 크기 조절 불가
    scales :{
      xAxes: [{
        display:true,
        scaleLabel:{display:true,labelString:'시간' },
      }],
      yAxes:[{
        display:true,
        scaleLabel: {display:true,labelString:'거리(cm)'}
      }]
    }
  }
};
function drawChart(){
  ctx = document.getElementById('canvas').getContext('2d');
  //캔버스 2d로 받기
  //chart 만들기
  chart = new Chart(ctx,config);
  init();
}

function init(){
  for(let i=0;i<label_size;i++){
    chart.data.labels[i]=i;
  }
  chart.update();
}
function addChartData(value){
  count++;
  count%=100;
  let n = chart.data.datasets[0].data.lenth;
  //데이터 갯수

  if(n < label_size){//갯수가 안되면 그냥 넣어줌
    chart.data.datasets[0].data.push(value);
  }else{
    chart.data.datasets[0].data.push(value);
    chart.data.datasets[0].data.shift();
    chart.data.labels.push(count);
    chart.data.labels.shift();
  }
  chart.update();
}
window.addEventListener("load",drawChart);

function startsensor(){
  //sensor토픽에 붙음
  subscribe("sensor");
  publish("Sensor","startsensor");
}
function stopsensor(){
  unsubscribe("sensor");
  publish("Sensor","stopsensor");
}