from django.test import Client, TestCase
from django.contrib.auth.models import User

import mock


@mock.patch("chat.views.SERVER")
class AjaxTest(TestCase):

    def setUp(self):
        User.objects.create_superuser("admin", "admin@example.com", "pass")
        self.c = Client(enforce_csrf_checks=True)
        r = self.c.get("/admin/login/")
        csrf_token = self.c.cookies['csrftoken'].value
        r = self.c.post("/admin/login/", {
            "username": "admin", "password": "pass",
            "csrfmiddlewaretoken": csrf_token})
        self.assertEqual(r.status_code, 302)

    def test_put(self, server):
        csrf_token = self.c.cookies['csrftoken'].value
        r = self.c.post(
            "/chat/put_message/my_room", {
                'message': 'ciao', "csrfmiddlewaretoken": csrf_token},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(
            server.mock_calls, [mock.call.put("my_room", "admin", u'ciao')])

    def test_poll(self, server):
        csrf_token = self.c.cookies['csrftoken'].value
        server.poll.return_value = "ciao"
        r = self.c.post(
            "/chat/poll_message", {"csrfmiddlewaretoken": csrf_token},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.content, '"ciao"')
        self.assertEqual(server.mock_calls, [mock.call.poll("admin")])
