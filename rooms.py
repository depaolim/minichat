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


################################################################################
# TESTS
################################################################################

import unittest


class TestAcceptance(unittest.TestCase):

    def setUp(self):
        self.USERS = {}
        self.ROOMS = {'python': Room(), 'django': Room()}

    def join(self, room, uid):
        user = self.USERS.get(uid, None)

        if not user:
            self.USERS[uid] = user = User()

        active_room = self.ROOMS[room]
        active_room.subscribe(user)
        print 'subscribe', active_room, user

        messages = active_room.backlog()
        return messages

    def put(self, uid, room_name, message):
        self.USERS[uid]
        room = self.ROOMS[room_name]
        room.add(':'.join([uid, message]))

    def poll(self, uid):
        return self.USERS[uid].get()

    def test(self):
        self.assertFalse(self.join("python", "me"))
        self.assertFalse(self.join("python", "io"))
        self.put("me", "python", "ciao")
        self.assertEqual(self.poll("io"), "me:ciao")
        self.assertEqual(self.join("python", "you"), ["me:ciao"])


if __name__ == '__main__':
    unittest.main()
