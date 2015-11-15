# Micro gevent chatroom.
# ----------------------
# Make things as simple as possible, but not simpler.
from gevent import monkey
monkey.patch_all()

from flask import Flask, render_template, request, json

import rooms

app = Flask(__name__)
app.debug = True


ROOMS = {
    'python': rooms.Room(),
    'django': rooms.Room(),
}

USERS = {}


@app.route('/')
def choose_name():
    return render_template('choose.html')


@app.route('/<uid>')
def main(uid):
    return render_template(
        'main.html', uid=uid, rooms=ROOMS.keys())


@app.route('/<room>/<uid>')
def join(room, uid):
    user = USERS.get(uid, None)

    if not user:
        USERS[uid] = user = rooms.User()

    active_room = ROOMS[room]
    active_room.subscribe(user)
    print 'subscribe', active_room, user

    messages = active_room.backlog()

    return render_template(
        'room.html', room=room, uid=uid, messages=messages)


@app.route("/put/<room>/<uid>", methods=["POST"])
def put(room, uid):
    USERS[uid]
    room = ROOMS[room]
    message = request.form['message']
    room.add(':'.join([uid, message]))
    return ''


@app.route("/poll/<uid>", methods=["POST"])
def poll(uid):
    msg = USERS[uid].get()
    return json.dumps(msg)
