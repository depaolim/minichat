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


@app.route('/<user_id>')
def main(user_id):
    return render_template(
        'main.html', user_id=user_id, rooms=SERVER.names())


@app.route('/<room_id>/<user_id>')
def join(room_id, user_id):
    messages = SERVER.join(room_id, user_id)
    return render_template(
        'room.html', room_id=room_id, uid=user_id, messages=messages)


@app.route("/put/<room_id>/<user_id>", methods=["POST"])
def put(room_id, user_id):
    message = request.form['message']
    SERVER.put(room_id, user_id, message)
    return ''


@app.route("/poll/<user_id>", methods=["POST"])
def poll(user_id):
    msg = SERVER.poll(user_id)
    return json.dumps(msg)
