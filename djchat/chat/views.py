import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

import rooms


SERVER = rooms.Server()


def index(request):
    return render(request, "chat/index.html", {"rooms": SERVER.names()})


def room(request, room_id):
    messages = SERVER.join(room_id, request.user.username)
    return render(request, "chat/room.html", {
        "room_id": room_id, "messages": messages})


@login_required
def put_message(request, room_id):
    assert request.is_ajax()
    SERVER.put(room_id, request.user.username, request.POST["message"])
    return HttpResponse()


@login_required
def poll_message(request):
    assert request.is_ajax()
    msg = SERVER.poll(request.user.username)
    return HttpResponse(json.dumps(msg))
