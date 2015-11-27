from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.index),
    url(r'^room/(?P<room_id>\w+)$', views.room),
    url(r'^put_message/(?P<room_id>\w+)$', views.put_message),
    url(r'^poll_message$', views.poll_message),
]
