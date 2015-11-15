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
