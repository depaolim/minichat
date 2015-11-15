# Micro gevent chatroom.
# ----------------------
from app import app
from gevent.pywsgi import WSGIServer


if __name__ == "__main__":
    http = WSGIServer(('', 5000), app)
    http.serve_forever()
