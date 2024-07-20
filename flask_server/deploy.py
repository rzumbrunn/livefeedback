from gevent.pywsgi import WSGIServer
from server import app
from server import socketio

#http_server = WSGIServer(('', 5000), app)
#http_server.serve_forever()

#this is a development server TODO: change to production server later
socketio.run(app, host='0.0.0.0', port=5000, debug=True)