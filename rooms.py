from gevent import queue


class Room(object):
    def __init__(self):
        self.users = set()
        self.messages = []

    def backlog(self, size=25):
        return self.messages[-size:]

    def subscribe(self, user):
        self.users.add(user)

    def add(self, message):
        for user in self.users:
            print user
            user.put(message)
        self.messages.append(message)


class User(object):
    def __init__(self):
        self.queue = queue.Queue()

    def put(self, message):
        self.queue.put_nowait(message)

    def get(self):
        try:
            return self.queue.get(timeout=10)
        except queue.Empty:
            return []


class Server(object):
    def __init__(self):
        self.users = {}
        self.rooms = {'python': Room(), 'django': Room()}

    def names(self):
        return self.rooms.keys()

    def join(self, room_id, user_id):
        user = self.users.get(user_id, None)

        if not user:
            self.users[user_id] = user = User()

        room = self.rooms[room_id]
        room.subscribe(user)
        print 'subscribe', room, user

        messages = room.backlog()
        return messages

    def put(self, room_id, user_id, message):
        self.users[user_id]
        room = self.rooms[room_id]
        room.add(':'.join([user_id, message]))

    def poll(self, user_id):
        return self.users[user_id].get()


################################################################################
# TESTS
################################################################################

import unittest


class TestAcceptance(unittest.TestCase):

    def setUp(self):
        self.server = Server()

    def test_list(self):
        self.assertEqual(self.server.names(), ["python", "django"])

    def test_interaction(self):
        self.assertFalse(self.server.join("python", "me"))
        self.assertFalse(self.server.join("python", "io"))
        self.server.put("python", "me", "ciao")
        self.assertEqual(self.server.poll("io"), "me:ciao")
        self.assertEqual(self.server.join("python", "you"), ["me:ciao"])


if __name__ == '__main__':
    unittest.main()
