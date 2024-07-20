
const avg_speed = document.querySelector('#avg_speed')
const no_participants = document.querySelector('#no_participants')
const speed_instruction = document.querySelector('#speed_instruction')
const panic_display = document.querySelector('#panic_display')
const reset_button = document.querySelector('#reset_button')

panic_display.style.display = "none"

function set_speed_instruction(speed){
    speed_instruction.style.color = color_gradient_from_speed(speed)
    if(speed >= 75){
        speed_instruction.textContent = "slower!"
        return;
    }
    else if(speed <= 25){
        speed_instruction.textContent = "faster!"
        return;
    }
    speed_instruction.textContent = "ok"
}


//start loop to fetch data from server every second
setInterval(function() {
    // fetch data using ajax from server on address: /api/avg_speed
    fetch('api/avg_speed').then(response => response.json()).then(data => {
        avg_speed.textContent = "average speed: " + String(data['avg_speed']);
        avg_speed.style.color = color_gradient_from_speed(data['avg_speed']);

        set_speed_instruction(data['avg_speed'])

        no_participants.textContent = data['num_sessions']
        
        // set panic display if panic_flag is set
        if(data['panic_flag']){
            panic_display.style.display = "block"
        }
        

        
    });
}, 1000);

//add button event listener
reset_button.addEventListener("click", function(){
    fetch('/feedback/api/reset_panic').then(response => response.json()).then(data => {
        panic_display.style.display = "none"
    });
});