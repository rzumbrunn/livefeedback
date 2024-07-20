

const value = document.querySelector("#value");
const input = document.querySelector("#speed");
const avg_speed = document.querySelector("#avg_speed");

value.textContent = input.value;
var socket = io.connect('/', {
  'path': '/feedback/socket.io'
});
var previousSpeed = 0;

function panic(){
  socket.emit('panic');
}
//add panic button event listener
document.querySelector("#panic_button").addEventListener("click", panic);


function send_feedback_to_server(speed){
  value.textContent = speed;
  socket.emit('feedback_update', {speed: speed, previousSpeed: previousSpeed});
  previousSpeed = speed;
}



//setup update on fetch_timeseries
socket.on('update_timeseries', function(data){
  //console.log(data);
  var timeseries = data['timeseries'];
  var times = timeseries.map(function(x) {return x[0]});
  var speeds = timeseries.map(function(x) {return x[1]});
  //console.log(times);
  //console.log(speeds);
});



//setup update on client answer
socket.on('feedback_update_answer', function(data){
  //console.log(data);
  var total_speed = data['total_speed'];
  var num_sessions = data['num_sessions'];
  //console.log(total_speed);
  //console.log(num_sessions);
  avg_speed.textContent = total_speed/num_sessions;

  //set text color based on average speed
  avg_speed.style.color = color_gradient_from_speed(total_speed/num_sessions);

});
input.addEventListener("input", (event) => {
  send_feedback_to_server(input.value);
  //set text color based on speed
  value.style.color = color_gradient_from_speed(input.value);
});


//send initial value to server
send_feedback_to_server(value.textContent);
//set text color based on speed initially
value.style.color = color_gradient_from_speed(input.value);

