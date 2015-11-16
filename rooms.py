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
            user.queue.put_nowait(message)
        self.messages.append(message)


class User(object):
    def __init__(self):
        self.queue = queue.Queue()

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

    def join(self, room, uid):
        user = self.users.get(uid, None)

        if not user:
            self.users[uid] = user = User()

        active_room = self.rooms[room]
        active_room.subscribe(user)
        print 'subscribe', active_room, user

        messages = active_room.backlog()
        return messages

    def put(self, room, uid, message):
        self.users[uid]
        room = self.rooms[room]
        room.add(':'.join([uid, message]))

    def poll(self, uid):
        return self.users[uid].get()


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
