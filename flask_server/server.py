from flask import Flask, render_template, request, session
from flask_socketio import SocketIO,emit
import redis
import json
from time import time

app = Flask(
    __name__,
    static_url_path="",
    static_folder="static"
)
app.config['SECRET_KEY'] = 'secret!'

socketio = SocketIO(
    app, 
    logger=True, 
    path="socket.io", 
    cookie='testcookie',
)

# set up the redis connection
r = redis.StrictRedis(host='redis', port=6379, db=0)

# clear the redis database
r.flushall()

# set the panic flag to 0
r.set("panic_flag", 0)

# start timeseries
ts = r.ts()
retention = 10*60*1000
ts.create("history", retention_msecs=retention)



# start a background thread to write to the timeseries
def write_to_timeseries():
    #TODO: implement this
    return
    starttime = None
    while True:
        # get the total speed
        total_speed = r.get("total_speed")
        if total_speed is None:
            total_speed = 0
        else:
            total_speed = int(total_speed)

        # get the number of sessions
        num_sessions = r.hlen("speeds")

        # write the data to the timeseries
        ts.add("history", "*", total_speed)
        if starttime is None:
            starttime = int(time())

        # send the data to all clients of the last 10 seconds
        
        socketio.emit('update_timeseries', {
            'timeseries': ts.range("history", max(int(time())-10, starttime), "+")
        })


        # sleep for 1 second
        socketio.sleep(1)
# start the background thread
socketio.start_background_task(write_to_timeseries)


@app.route('/')
def index():
    return render_template('feedback.html', async_mode = socketio.async_mode)

@socketio.on('send_to_server')
def send_to_server(data):
    print(data)

# Gets the update from the client as a json string
@socketio.on('feedback_update')
def feedback_update(data):
    # get session id
    sid = request.sid

    #parse the json string into a dictionary

    #get the speed value
    speed = data['speed']
    if speed is None:
        speed = 0
    speed = int(speed)

    ### Speed ###

    # get previous speed from redis
    previous_speed = r.hget(f"speeds", sid)
    if not previous_speed:
        previous_speed = 0
    previous_speed = int(previous_speed)

    r.hset(f"speeds", sid, speed)

    # update the total speed
    total_speed = r.incrby("total_speed", speed - previous_speed)
    # get number of sessions
    num_sessions = r.hlen("speeds")

    # get panic
    panic_flag = r.get("panic_flag")
    if panic_flag is None:
        panic_flag = 0
    else:
        panic_flag = int(panic_flag)
    

    # emit the update to all clients
    socketio.emit('feedback_update_answer', {
        'total_speed': total_speed,
        'num_sessions': num_sessions,
        'panic_flag': panic_flag
    })

@socketio.on('panic')
def panic_button():
    print('panic button pressed')
    # set the panic flag to 1
    r.set("panic_flag", 1)

@app.route('/api/reset_panic')
def reset_panic():
    r.set("panic_flag", 0)
    print('Panic flag reset')
    return "Panic flag reset"
    
# Handle disconnects
@socketio.on('disconnect')
def disconnect():
    sid = request.sid

    my_speed = r.hget(f"speeds", sid)
    if my_speed is None:
        my_speed = 0
    my_speed = int(my_speed)

    # update the total speed
    r.incrby("total_speed", -my_speed)
    # remove the speed from the redis database
    r.hdel(f"speeds", sid)

    # emit new total speed to all clients
    total_speed = r.get("total_speed")
    num_sessions = r.hlen("speeds")

    socketio.emit('feedback_update_answer', {
        'total_speed': total_speed,
        'num_sessions': num_sessions,
    })
    print('client disconnected')


#Rest api
@app.route('/api/avg_speed')
def avg_speed():
    total_speed = r.get("total_speed")
    num_sessions = r.hlen("speeds")
    if total_speed is None:
        total_speed = 0
    else:
        total_speed = int(total_speed)

    if num_sessions == 0:
        avg_speed = 0
    else:
        avg_speed = total_speed / num_sessions

    panic_flag = r.get("panic_flag")
    if panic_flag is None:
        panic_flag = 0
    else:
        panic_flag = int(panic_flag)

    return json.dumps({
        'total_speed': total_speed,
        'num_sessions': num_sessions,
        'avg_speed': avg_speed,
        'panic_flag': panic_flag 
    })

# admin page
@app.route('/admin')
def admin():
    return render_template('admin.html',async_mode = socketio.async_mode)
