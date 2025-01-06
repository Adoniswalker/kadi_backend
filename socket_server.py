import socketio
from django.conf import settings

from kadi_backend import asgi

sio = socketio.Server()


@sio.event
def connect(sid, environ):
    print('Client connected:', sid)


@sio.event
def my_event(sid, data):
    print(sid, data)
    return 'OK', 123


@sio.event
def disconnect(sid):
    print('Client disconnected:', sid)


if __name__ == '__main__':
    import eventlet
    import eventlet.wsgi

    # from  import asgi

    app = socketio.WSGIApp(sio, asgi.application)
    eventlet.wsgi.server(eventlet.listen(('', 8000)), app)
