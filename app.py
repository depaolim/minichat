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
        'main.html', uid=uid, rooms=SERVER.names())


@app.route('/<room_id>/<uid>')
def join(room_id, uid):
    messages = SERVER.join(room_id, uid)
    return render_template(
        'room.html', room_id=room_id, uid=uid, messages=messages)


@app.route("/put/<room_id>/<uid>", methods=["POST"])
def put(room_id, uid):
    message = request.form['message']
    SERVER.put(room_id, uid, message)
    return ''


@app.route("/poll/<uid>", methods=["POST"])
def poll(uid):
    msg = SERVER.poll(uid)
    return json.dumps(msg)
