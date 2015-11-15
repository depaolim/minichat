# Micro gevent chatroom.
# ----------------------
# Make things as simple as possible, but not simpler.
from gevent import monkey
monkey.patch_all()

from flask import Flask, render_template, request, json

import rooms

app = Flask(__name__)
app.debug = True


SERVER = rooms.Server()


@app.route('/')
def choose_name():
    return render_template('choose.html')


@app.route('/<uid>')
def main(uid):
    return render_template(
        'main.html', uid=uid, rooms=SERVER.rooms())


@app.route('/<room>/<uid>')
def join(room, uid):
    messages = SERVER.join(room, uid)
    return render_template(
        'room.html', room=room, uid=uid, messages=messages)


@app.route("/put/<room>/<uid>", methods=["POST"])
def put(room, uid):
    message = request.form['message']
    SERVER.put(room, uid, message)
    return ''


@app.route("/poll/<uid>", methods=["POST"])
def poll(uid):
    msg = SERVER.poll(uid)
    return json.dumps(msg)
