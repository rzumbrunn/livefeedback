function color_gradient_from_speed(speed){
  // make the color gradient symmetric around 0.5
  speed = Math.abs((speed - 50) * 2);


  var r = speed * 2;
  var g = 255-speed * 2;
  var b = 0;
  return "rgb(" + r + "," + g + "," + b + ")";
}